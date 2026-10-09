'''
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
'''
"""Freehand Cut, stage A: non-destructive stroke and section preview."""

# ops_freehand.py

import hashlib
import math

from array import array
from datetime import datetime

import bpy
import bmesh
import gpu

from bpy.props import FloatProperty
from bpy.types import Operator
from bpy_extras import view3d_utils
from gpu_extras.batch import batch_for_shader
from mathutils import Vector

from .utils import report_user
from .ops_split import warn_if_unapplied_transforms
from .seam_data import write_freehand_seams



# The brush remains an operator property rather than a persistent scene property.
DEFAULT_BRUSH_RADIUS = 10.0
SAMPLE_SPACING = 6.0
MAX_SAMPLES = 200
MAX_STROKE_POINTS = 4096

PARTS_COLLECTION_NAME = "SnapSplit_Parts"

ORANGE = (1.0, 0.35, 0.04, 1.0)
GRAY = (0.48, 0.52, 0.58, 0.75)
INVALID_COLOR = (1.0, 0.15, 0.12, 0.9)

_ACTIVE_OPERATORS = []


# ---------------------------------------------------------------------------
# Source validation
# ---------------------------------------------------------------------------

def _geometry_signature(mesh):
    """Hash vertex coordinates and topology independently of element counts."""
    digest = hashlib.sha256()

    specifications = (
        (mesh.vertices, "co", "f", 3),
        (mesh.edges, "vertices", "i", 2),
        (mesh.loops, "vertex_index", "i", 1),
        (mesh.polygons, "loop_start", "i", 1),
        (mesh.polygons, "loop_total", "i", 1),
    )

    for collection, attribute, typecode, width in specifications:
        values = array(typecode, [0]) * (len(collection) * width)
        collection.foreach_get(attribute, values)
        digest.update(len(values).to_bytes(8, "little"))
        digest.update(values.tobytes())

    return digest.digest()


# ---------------------------------------------------------------------------
# Stroke and plane utilities
# ---------------------------------------------------------------------------

def _resample_stroke(points):
    """Resample the complete stroke uniformly, including both endpoints."""
    if len(points) < 2:
        return list(points)

    lengths = [0.0]
    for a, b in zip(points, points[1:]):
        lengths.append(lengths[-1] + (b - a).length)

    total = lengths[-1]
    if total <= 1e-8:
        return [points[0].copy()]

    count = min(
        MAX_SAMPLES,
        max(2, math.ceil(total / SAMPLE_SPACING) + 1),
    )
    result = []
    segment = 0

    for i in range(count):
        distance = total * i / (count - 1)

        while (
            segment < len(points) - 2
            and lengths[segment + 1] < distance
        ):
            segment += 1

        span = lengths[segment + 1] - lengths[segment]
        factor = (
            (distance - lengths[segment]) / span
            if span > 1e-8
            else 0.0
        )
        result.append(
            points[segment].lerp(points[segment + 1], factor)
        )

    return result


def _fit_line(points):
    """Return the centroid and endpoint pair of the dominant 2D PCA axis."""
    if len(points) < 2:
        raise ValueError("Draw a longer stroke.")

    center = sum(points, Vector((0.0, 0.0))) / len(points)

    xx = yy = xy = 0.0
    for point in points:
        delta = point - center
        xx += delta.x * delta.x
        yy += delta.y * delta.y
        xy += delta.x * delta.y

    trace = xx + yy
    difference = math.hypot(xx - yy, 2.0 * xy)

    if trace <= 1e-8 or difference <= trace * 1e-6:
        raise ValueError(
            "The stroke has no clear direction. Draw a straighter line."
        )

    angle = 0.5 * math.atan2(2.0 * xy, xx - yy)
    direction = Vector((math.cos(angle), math.sin(angle)))
    positions = [
        (point - center).dot(direction)
        for point in points
    ]

    low = min(positions)
    high = max(positions)

    if high - low < 8.0:
        raise ValueError("Draw a stroke at least 8 pixels long.")

    return (
        center,
        center + direction * low,
        center + direction * high,
    )


def _plane_basis(normal):
    """Build an orthonormal basis on a plane."""
    helper = Vector((0.0, 0.0, 1.0))
    if abs(normal.dot(helper)) > 0.9:
        helper = Vector((0.0, 1.0, 0.0))

    u = normal.cross(helper).normalized()
    v = normal.cross(u).normalized()
    return u, v


def _point_segment_distance(point, a, b):
    """Return the Euclidean distance from a point to a segment."""
    delta = b - a
    denominator = delta.length_squared

    if denominator <= 1e-20:
        return (point - a).length

    factor = max(
        0.0,
        min(1.0, (point - a).dot(delta) / denominator),
    )
    return (point - (a + factor * delta)).length


def _polygon_distance(point, polygon):
    """Return the distance to the boundary of a closed 2D polygon."""
    return min(
        _point_segment_distance(
            point,
            polygon[i],
            polygon[(i + 1) % len(polygon)],
        )
        for i in range(len(polygon))
    )


def _point_in_polygon(point, polygon):
    """Test containment using an odd-even horizontal ray."""
    inside = False
    previous = polygon[-1]

    for current in polygon:
        if (current.y > point.y) != (previous.y > point.y):
            x_crossing = (
                (previous.x - current.x)
                * (point.y - current.y)
                / (previous.y - current.y)
                + current.x
            )

            if point.x < x_crossing:
                inside = not inside

        previous = current

    return inside


# ---------------------------------------------------------------------------
# Preview geometry
# ---------------------------------------------------------------------------

def _extract_sections(
    mesh,
    matrix_world,
    plane_point,
    plane_normal,
    tolerance,
    keep_bmesh=False,
):
    """Bisect a world-space BMesh and extract closed section loops.

    No scene object or mesh datablock is modified.

    Edges are accepted only when adjacent faces extend to both plane sides.
    This excludes unrelated pre-existing coplanar face interiors.

    When keep_bmesh is True, ownership of the BMesh and its section edge
    references passes to the caller. Otherwise, the temporary BMesh is freed.
    """
    bm = bmesh.new()
    transferred = False

    try:
        bm.from_mesh(mesh)
        bm.transform(matrix_world)

        bmesh.ops.bisect_plane(
            bm,
            geom=list(bm.verts) + list(bm.edges) + list(bm.faces),
            dist=tolerance,
            plane_co=plane_point,
            plane_no=plane_normal,
            use_snap_center=False,
            clear_inner=False,
            clear_outer=False,
        )

        candidates = []
        edge_tolerance = tolerance * 2.0

        for edge in bm.edges:
            if len(edge.link_faces) != 2:
                continue

            if any(
                abs(
                    (vertex.co - plane_point).dot(plane_normal)
                ) > edge_tolerance
                for vertex in edge.verts
            ):
                continue

            has_positive = False
            has_negative = False

            for face in edge.link_faces:
                for vertex in face.verts:
                    distance = (
                        vertex.co - plane_point
                    ).dot(plane_normal)
                    has_positive |= distance > tolerance
                    has_negative |= distance < -tolerance

            if has_positive and has_negative:
                candidates.append(edge)

        adjacency = {}
        for edge in candidates:
            for vertex in edge.verts:
                adjacency.setdefault(vertex, []).append(edge)

        remaining = set(candidates)
        loops = []
        loop_edges = []
        invalid_segments = []
        invalid_count = 0

        while remaining:
            seed = remaining.pop()
            component_edges = {seed}
            component_vertices = set(seed.verts)
            stack = list(seed.verts)

            while stack:
                vertex = stack.pop()

                for edge in adjacency.get(vertex, ()):
                    if edge not in component_edges:
                        component_edges.add(edge)
                        remaining.discard(edge)

                        other = edge.other_vert(vertex)
                        if other not in component_vertices:
                            component_vertices.add(other)
                            stack.append(other)

            valid = (
                len(component_vertices) >= 3
                and all(
                    len(adjacency[vertex]) == 2
                    for vertex in component_vertices
                )
            )

            if not valid:
                invalid_count += 1
                for edge in component_edges:
                    invalid_segments.extend((
                        edge.verts[0].co.copy(),
                        edge.verts[1].co.copy(),
                    ))
                continue

            start = seed.verts[0]
            vertex = start
            previous_edge = None
            ordered = []
            ordered_edges = []

            for _ in range(len(component_edges)):
                ordered.append(vertex.co.copy())

                edge = next(
                    edge
                    for edge in adjacency[vertex]
                    if edge is not previous_edge
                )

                ordered_edges.append(edge)
                vertex = edge.other_vert(vertex)
                previous_edge = edge

            if (
                vertex is start
                and len(ordered) == len(component_vertices)
            ):
                loops.append(ordered)
                loop_edges.append(ordered_edges)
            else:
                invalid_count += 1
                for edge in component_edges:
                    invalid_segments.extend((
                        edge.verts[0].co.copy(),
                        edge.verts[1].co.copy(),
                    ))

        if keep_bmesh:
            # Transfer ownership only after successful extraction.
            transferred = True
            return (
                loops,
                invalid_segments,
                invalid_count,
                bm,
                loop_edges,
            )

        return loops, invalid_segments, invalid_count

    finally:
        if not transferred:
            bm.free()


# ---------------------------------------------------------------------------
# Local separation and conservative caps
# ---------------------------------------------------------------------------

def _face_components(bm, blocked_edges=()):
    """Find face islands without crossing the specified section edges."""
    blocked = set(blocked_edges)
    remaining = set(bm.faces)
    components = []

    while remaining:
        seed = remaining.pop()
        component = {seed}
        stack = [seed]

        while stack:
            face = stack.pop()

            for edge in face.edges:
                if edge in blocked:
                    continue

                for neighbor in edge.link_faces:
                    if neighbor in remaining:
                        remaining.remove(neighbor)
                        component.add(neighbor)
                        stack.append(neighbor)

        components.append(component)

    return components


def _boundary_cycles(edges):
    """Order simple boundary cycles and reject open or branched boundaries."""
    adjacency = {}

    for edge in edges:
        for vertex in edge.verts:
            adjacency.setdefault(vertex, []).append(edge)

    if any(
        len(linked) != 2
        for linked in adjacency.values()
    ):
        raise ValueError(
            "The new cut boundary is open or branched."
        )

    remaining = set(edges)
    cycles = []

    while remaining:
        seed = next(iter(remaining))
        start = seed.verts[0]
        vertex = start
        previous = None
        vertices = []
        cycle_edges = []

        while True:
            vertices.append(vertex)

            edge = next(
                candidate
                for candidate in adjacency[vertex]
                if candidate is not previous
            )

            if edge not in remaining:
                raise ValueError(
                    "The cut boundary could not be ordered."
                )

            remaining.remove(edge)
            cycle_edges.append(edge)
            vertex = edge.other_vert(vertex)
            previous = edge

            if vertex is start:
                break

        if len(vertices) < 3:
            raise ValueError(
                "A cut boundary has fewer than three vertices."
            )

        cycles.append((vertices, cycle_edges))

    return cycles


def _signed_polygon_area(polygon):
    """Return the signed area of a closed 2D polygon."""
    return 0.5 * sum(
        polygon[index].x * polygon[(index + 1) % len(polygon)].y
        - polygon[(index + 1) % len(polygon)].x * polygon[index].y
        for index in range(len(polygon))
    )


def _segments_touch(a, b, c, d, epsilon):
    """Detect crossing or nearly touching planar segments."""
    if (
        max(a.x, b.x) < min(c.x, d.x) - epsilon
        or max(c.x, d.x) < min(a.x, b.x) - epsilon
        or max(a.y, b.y) < min(c.y, d.y) - epsilon
        or max(c.y, d.y) < min(a.y, b.y) - epsilon
    ):
        return False

    if min(
        _point_segment_distance(a, c, d),
        _point_segment_distance(b, c, d),
        _point_segment_distance(c, a, b),
        _point_segment_distance(d, a, b),
    ) <= epsilon:
        return True

    def cross(first, second):
        return first.x * second.y - first.y * second.x

    ab = b - a
    cd = d - c
    return (
        cross(ab, c - a) * cross(ab, d - a) < 0.0
        and cross(cd, a - c) * cross(cd, b - c) < 0.0
    )


def _section_groups(loops, plane_point, plane_normal, epsilon):
    """Group simple planar contours into material regions and their holes."""
    u, v = _plane_basis(plane_normal)
    polygons = [
        [
            Vector((
                (point - plane_point).dot(u),
                (point - plane_point).dot(v),
            ))
            for point in loop
        ]
        for loop in loops
    ]

    areas = []

    for polygon in polygons:
        count = len(polygon)
        if count < 3:
            raise ValueError("A section contour has fewer than three vertices.")

        area = abs(_signed_polygon_area(polygon))
        if area <= epsilon * epsilon:
            raise ValueError("A section contour has a degenerate area.")
        areas.append(area)

        for index in range(count):
            a = polygon[index]
            b = polygon[(index + 1) % count]

            if (b - a).length <= epsilon:
                raise ValueError(
                    "A section contour contains an extremely short edge."
                )

            # Adjacent edges share an endpoint and must not double back.
            previous = polygon[(index - 1) % count]
            if (
                _point_segment_distance(previous, a, b) <= epsilon
                or _point_segment_distance(b, previous, a) <= epsilon
            ):
                raise ValueError(
                    "A section contour contains overlapping adjacent edges."
                )

            for other in range(index + 1, count):
                if (
                    other == index + 1
                    or (index == 0 and other == count - 1)
                ):
                    continue

                c = polygon[other]
                d = polygon[(other + 1) % count]

                if _segments_touch(a, b, c, d, epsilon):
                    raise ValueError(
                        "A section contour intersects or touches itself."
                    )

    # Distinct contours must have an unambiguous nesting relationship.
    for first in range(len(polygons)):
        polygon = polygons[first]

        for second in range(first + 1, len(polygons)):
            other = polygons[second]

            for index, a in enumerate(polygon):
                b = polygon[(index + 1) % len(polygon)]

                for other_index, c in enumerate(other):
                    d = other[(other_index + 1) % len(other)]

                    if _segments_touch(a, b, c, d, epsilon):
                        raise ValueError(
                            "Section contours intersect or touch. "
                            "Move the cutting stroke slightly."
                        )

    parents = []

    for index, polygon in enumerate(polygons):
        containers = [
            other
            for other, candidate in enumerate(polygons)
            if other != index
            and areas[other] > areas[index]
            and _point_in_polygon(polygon[0], candidate)
        ]

        parents.append(
            min(containers, key=lambda other: areas[other])
            if containers
            else None
        )

    depths = []

    for index in range(len(polygons)):
        depth = 0
        parent = parents[index]

        while parent is not None:
            depth += 1
            if depth > len(polygons):
                raise ValueError("Section nesting contains a cycle.")
            parent = parents[parent]

        depths.append(depth)

    groups = []

    for index, depth in enumerate(depths):
        if depth % 2:
            continue

        holes = [
            other
            for other, parent in enumerate(parents)
            if parent == index
        ]

        expected_area = areas[index] - sum(
            areas[other] for other in holes
        )

        if expected_area <= epsilon * epsilon:
            raise ValueError("A section material region has no usable area.")

        groups.append({
            "outer": index,
            "holes": tuple(holes),
            "indices": (index, *holes),
            "expected_area": expected_area,
        })

    return polygons, groups


def _expand_section_selection(selected, groups):
    """Select every boundary belonging to a touched material region."""
    expanded = set()

    for group in groups:
        if selected.intersection(group["indices"]):
            expanded.update(group["indices"])

    return expanded


def _edge_side_faces(edge, plane_point, plane_normal, epsilon):
    """Return the negative and positive adjacent faces of a section edge."""
    sides = {}

    if len(edge.link_faces) != 2:
        raise ValueError("A selected section edge is not manifold.")

    for face in edge.link_faces:
        distances = [
            (vertex.co - plane_point).dot(plane_normal)
            for vertex in face.verts
        ]

        positive = max(distances) > epsilon
        negative = min(distances) < -epsilon

        if positive == negative:
            raise ValueError(
                "A section face cannot be assigned to one plane side."
            )

        side = 1 if positive else -1

        if side in sides:
            raise ValueError(
                "The adjacent section faces are not on opposite plane sides."
            )

        sides[side] = face

    return sides


def _section_winding(loop, edges, positive_face, polygon, epsilon):
    """Get the directed contour winding from the positive-side wall face."""
    edge = edges[0]
    face_loop = next(
        face_loop
        for face_loop in positive_face.loops
        if face_loop.edge == edge
    )

    # Extracted contours and their edge lists use the same traversal order.
    same_direction = (
        face_loop.vert.co - loop[0]
    ).length <= epsilon

    signed_area = _signed_polygon_area(polygon)
    return signed_area if same_direction else -signed_area


def _section_partitions(operator):
    """Join wall components through selected ring caps on each plane side."""
    bm = operator._cut_bm
    point = operator._plane_point
    normal = operator._plane_normal
    epsilon = operator._cut_tolerance * 2.0

    polygons, groups = _section_groups(
        operator._cut_loops,
        point,
        normal,
        epsilon,
    )

    selected_groups = [
        group
        for group in groups
        if operator._cut_selected.intersection(group["indices"])
    ]

    for group in selected_groups:
        if not set(group["indices"]).issubset(operator._cut_selected):
            raise ValueError(
                "The selected material region is incomplete. Redraw the preview."
            )

    selected_edges = {
        edge
        for group in selected_groups
        for index in group["indices"]
        for edge in operator._cut_loop_edges[index]
    }

    components = _face_components(bm, selected_edges)
    component_of = {
        face: index
        for index, component in enumerate(components)
        for face in component
    }

    source_components = _face_components(bm)
    source_component_of = {
        face: index
        for index, component in enumerate(source_components)
        for face in component
    }

    parents = list(range(len(components)))
    source_parents = list(range(len(source_components)))

    def find(table, item):
        while table[item] != item:
            table[item] = table[table[item]]
            item = table[item]
        return item

    def join(table, items):
        items = list(items)
        if not items:
            return

        root = find(table, items[0])
        for item in items[1:]:
            table[find(table, item)] = root

    side_records = []

    for group in selected_groups:
        side_components = {-1: set(), 1: set()}
        shell_components = set()
        windings = {}

        for index in group["indices"]:
            loop_edges = operator._cut_loop_edges[index]
            loop_sides = {-1: set(), 1: set()}
            positive_face = None

            for edge in loop_edges:
                sides = _edge_side_faces(
                    edge, point, normal, epsilon,
                )

                for side, face in sides.items():
                    loop_sides[side].add(component_of[face])
                    shell_components.add(source_component_of[face])

                if positive_face is None:
                    positive_face = sides[1]

            if any(len(items) != 1 for items in loop_sides.values()):
                raise ValueError(
                    "A section loop does not have a unique component on each side."
                )

            if loop_sides[-1] == loop_sides[1]:
                raise ValueError(
                    "A selected section loop does not separate the surface."
                )

            for side in (-1, 1):
                side_components[side].update(loop_sides[side])

            windings[index] = _section_winding(
                operator._cut_loops[index],
                loop_edges,
                positive_face,
                polygons[index],
                epsilon,
            )

        # Nested solid shells must not be mistaken for cavity walls.
        outer_winding = windings[group["outer"]]

        for hole in group["holes"]:
            if outer_winding * windings[hole] >= 0.0:
                raise ValueError(
                    "Outer and inner wall orientations are inconsistent. "
                    "Check the source mesh normals."
                )

        for side in (-1, 1):
            join(parents, side_components[side])

        # A cavity shell may be disconnected before caps are created.
        join(source_parents, shell_components)
        side_records.append(side_components)

    # Do not silently distribute unrelated solids or untouched cavity shells.
    if len({
        find(source_parents, index)
        for index in range(len(source_components))
    }) != 1:
        raise ValueError(
            "The source contains unrelated or uncut separate surface shells. "
            "This B3 version cannot safely assign them to result parts."
        )

    for record in side_records:
        negative = {
            find(parents, index)
            for index in record[-1]
        }
        positive = {
            find(parents, index)
            for index in record[1]
        }

        if negative.intersection(positive):
            raise ValueError(
                "The selected material regions do not produce a valid separation."
            )

    partitions = {}

    for index, component in enumerate(components):
        root = find(parents, index)
        partitions.setdefault(root, set()).update(component)

    if len(partitions) < 2:
        raise ValueError(
            "The selected regions do not separate the mesh into distinct parts."
        )

    return list(partitions.values())


def _fill_section_caps(bm, plane_point, plane_normal, tolerance):
    """Fill new boundaries as planar material regions, preserving holes."""
    epsilon = tolerance * 2.0
    boundaries = [
        edge for edge in bm.edges if edge.is_boundary
    ]

    if not boundaries:
        raise ValueError("A result part has no expected cut boundary.")

    cycles = _boundary_cycles(boundaries)
    loops = [
        [vertex.co.copy() for vertex in vertices]
        for vertices, _edges in cycles
    ]

    if any(
        abs((point - plane_point).dot(plane_normal)) > tolerance * 8.0
        for loop in loops
        for point in loop
    ):
        raise ValueError("A new boundary is not on the stored cutting plane.")

    polygons, groups = _section_groups(
        loops, plane_point, plane_normal, epsilon,
    )
    u, v = _plane_basis(plane_normal)

    for group in groups:
        edges = [
            edge
            for index in group["indices"]
            for edge in cycles[index][1]
        ]
        faces_before = set(bm.faces)

        # Use the same ring-aware operation as the existing planar cap path.
        # Any failure aborts the entire disposable result BMesh.
        bmesh.ops.triangle_fill(
            bm,
            edges=edges,
            use_beauty=True,
            use_dissolve=False,
            normal=plane_normal,
        )

        caps = [
            face for face in bm.faces
            if face not in faces_before
        ]

        if not caps or any(len(face.verts) != 3 for face in caps):
            raise ValueError("A material region could not be triangulated.")

        outer = polygons[group["outer"]]
        holes = [
            polygons[index] for index in group["holes"]
        ]

        def belongs_to_material(point):
            if _polygon_distance(point, outer) <= epsilon:
                inside_outer = True
            else:
                inside_outer = _point_in_polygon(point, outer)

            if not inside_outer:
                return False

            return not any(
                _point_in_polygon(point, hole)
                and _polygon_distance(point, hole) > epsilon
                for hole in holes
            )

        for face in caps:
            projected = [
                Vector((
                    (vertex.co - plane_point).dot(u),
                    (vertex.co - plane_point).dot(v),
                ))
                for vertex in face.verts
            ]

            if abs(_signed_polygon_area(projected)) <= epsilon * epsilon:
                raise ValueError("The cap contains a degenerate triangle.")

            center = sum(
                projected, Vector((0.0, 0.0)),
            ) / len(projected)

            samples = [center] + [
                (projected[index] + projected[(index + 1) % 3]) * 0.5
                for index in range(3)
            ]

            if not all(belongs_to_material(point) for point in samples):
                raise ValueError(
                    "The generated cap covers a hole or leaves the material region."
                )

            face.smooth = False

        actual_area = sum(face.calc_area() for face in caps)
        expected_area = group["expected_area"]
        allowed_error = max(
            expected_area * 1e-5,
            epsilon * epsilon * 16.0,
        )

        if abs(actual_area - expected_area) > allowed_error:
            raise ValueError(
                "The generated cap area does not match the material region."
            )

        cap_set = set(caps)

        # Every original boundary must now meet exactly one cap face.
        for edge in edges:
            if (
                len(edge.link_faces) != 2
                or sum(face in cap_set for face in edge.link_faces) != 1
            ):
                raise ValueError(
                    "A cap did not correctly connect to its wall boundary."
                )

        # New internal triangulation edges must meet two cap faces.
        internal_edges = {
            edge
            for face in caps
            for edge in face.edges
            if edge not in set(edges)
        }

        if any(
            len(edge.link_faces) != 2
            or any(face not in cap_set for face in edge.link_faces)
            for edge in internal_edges
        ):
            raise ValueError("The cap has an invalid internal triangulation.")

    if any(len(edge.link_faces) != 2 for edge in bm.edges):
        raise ValueError("A result part has open or non-manifold edges.")

    # Ring caps must connect inner and outer walls into one result surface.
    if len(_face_components(bm)) != 1:
        raise ValueError(
            "The capped result still contains disconnected surface shells."
        )


def _prepare_freehand_seam_regions(operator, component_indices):
    """Associate each selected material region with its sorted result parts."""
    bm = operator._cut_bm
    point = operator._plane_point
    normal = operator._plane_normal
    epsilon = operator._cut_tolerance * 2.0

    face_to_part = {
        face_index: part_index
        for part_index, indices in enumerate(component_indices)
        for face_index in indices
    }

    if len(face_to_part) != len(bm.faces):
        raise ValueError(
            "The Freehand partitions do not cover every source face."
        )

    _polygons, groups = _section_groups(
        operator._cut_loops,
        point,
        normal,
        epsilon,
    )

    regions = []

    for group in groups:
        if not operator._cut_selected.intersection(group["indices"]):
            continue

        if not set(group["indices"]).issubset(operator._cut_selected):
            raise ValueError("A selected seam region is incomplete.")

        partners = {-1: set(), 1: set()}

        for loop_index in group["indices"]:
            for edge in operator._cut_loop_edges[loop_index]:
                sides = _edge_side_faces(
                    edge,
                    point,
                    normal,
                    epsilon,
                )

                for side, face in sides.items():
                    partners[side].add(face_to_part[face.index])

        if any(len(indices) != 1 for indices in partners.values()):
            raise ValueError(
                "A material region has ambiguous result partners."
            )

        negative = next(iter(partners[-1]))
        positive = next(iter(partners[1]))

        if negative == positive:
            raise ValueError(
                "Both sides of a seam belong to the same result part."
            )

        regions.append({
            "negative_part": negative,
            "positive_part": positive,
            "outer": [
                point.copy()
                for point in operator._cut_loops[group["outer"]]
            ],
            "holes": [
                [
                    point.copy()
                    for point in operator._cut_loops[loop_index]
                ]
                for loop_index in group["holes"]
            ],
        })

    if not regions:
        raise ValueError("No selected Freehand seam regions were found.")

    return regions



def _build_freehand_meshes(operator, cap_seams):
    """Build parts and optionally close their selected material regions."""

    bm = operator._cut_bm
    source = operator._mesh

    if bm is None or not operator._cut_selected:
        raise ValueError("No valid cutting preview is available.")

    if getattr(operator, "_cut_invalid_count", 0):
        raise ValueError(
            "The preview contains open or branched sections. "
            "Move the cutting stroke and try again."
        )

    # Open-ended tubes with a complete wall rim are manifold surfaces.
    # Actual missing wall faces or uncapped wall thickness remain unsupported.
    if any(len(edge.link_faces) != 2 for edge in bm.edges):
        raise ValueError(
            "Freehand B3 requires a closed manifold material surface."
        )

    if any(not vertex.link_faces for vertex in bm.verts):
        raise ValueError("Loose vertices are not supported.")

    components = _section_partitions(operator)

    bm.faces.index_update()
    component_indices = [
        {face.index for face in component}
        for component in components
    ]
    component_indices.sort(key=len, reverse=True)

    # Bind seams to the exact order used for mesh creation and publication.
    seam_regions = _prepare_freehand_seam_regions(
        operator,
        component_indices,
    )

    inverse = operator._matrix_world.inverted()

    meshes = []

    try:
        for number, indices in enumerate(component_indices, start=1):
            part_bm = bm.copy()

            try:
                part_bm.faces.ensure_lookup_table()
                remove_faces = [
                    face
                    for index, face in enumerate(part_bm.faces)
                    if index not in indices
                ]

                bmesh.ops.delete(
                    part_bm,
                    geom=remove_faces,
                    context='FACES_ONLY',
                )

                unused_vertices = [
                    vertex for vertex in part_bm.verts
                    if not vertex.link_faces
                ]
                if unused_vertices:
                    bmesh.ops.delete(
                        part_bm,
                        geom=unused_vertices,
                        context='VERTS',
                    )

                unused_edges = [
                    edge for edge in part_bm.edges
                    if not edge.link_faces
                ]
                if unused_edges:
                    bmesh.ops.delete(
                        part_bm,
                        geom=unused_edges,
                        context='EDGES',
                    )

                # Preserve open cut boundaries when automatic capping is disabled.
                if cap_seams:
                    _fill_section_caps(
                        part_bm,
                        operator._plane_point,
                        operator._plane_normal,
                        operator._cut_tolerance,
                    )


                part_bm.transform(inverse)
                bmesh.ops.recalc_face_normals(
                    part_bm,
                    faces=list(part_bm.faces),
                )

                mesh = source.copy()
                meshes.append(mesh)
                mesh.name = (
                    f"{operator._obj.name}_Freehand_{number:02d}"
                )

                part_bm.to_mesh(mesh)
                mesh.update()

            finally:
                part_bm.free()

        return meshes, seam_regions


    except Exception:
        for mesh in meshes:
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)
        raise



# ---------------------------------------------------------------------------
# Transactional scene publication
# ---------------------------------------------------------------------------

def _publish_freehand_parts(
    context,
    operator,
    meshes,
    seam_regions,
    cap_seams,
):
    """Publish prepared parts and hide the unchanged source only on success."""
    source = operator._obj
    selected_before = list(context.selected_objects)
    active_before = context.view_layer.objects.active
    hidden_before = source.hide_get()
    render_before = source.hide_render

    root = bpy.data.collections.get(PARTS_COLLECTION_NAME)
    root_created = False
    root_linked = False
    job = None
    objects = []

    try:
        if root is None:
            root = bpy.data.collections.new(
                PARTS_COLLECTION_NAME
            )
            root_created = True

        if not any(
            child == root
            for child in context.scene.collection.children
        ):
            context.scene.collection.children.link(root)
            root_linked = True

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        job = bpy.data.collections.new(
            f"{source.name}_Freehand_{stamp}"
        )
        root.children.link(job)

        for number, mesh in enumerate(meshes, start=1):
            obj = bpy.data.objects.new(
                f"{source.name}_Freehand_{number:02d}",
                mesh,
            )
            objects.append(obj)

            obj.matrix_world = operator._matrix_world.copy()
            obj.color = source.color[:]
            job.objects.link(obj)

        # Keep metadata creation inside the existing publication transaction.
        tangent, _bitangent = _plane_basis(operator._plane_normal)

        write_freehand_seams(
            objects=objects,
            regions=seam_regions,
            plane_point=operator._plane_point,
            plane_normal=operator._plane_normal,
            tangent=tangent,
            capped=cap_seams,
            tolerance=operator._cut_tolerance,
        )

        context.view_layer.update()


        # Never hide the source when results are excluded or invisible.
        if any(
            not obj.visible_get()
            for obj in objects
        ):
            raise ValueError(
                "The Parts collection is hidden or excluded. "
                "Make it visible and retry."
            )

        for obj in list(context.selected_objects):
            obj.select_set(False)

        for obj in objects:
            obj.select_set(True)

        context.view_layer.objects.active = objects[0]

        # Hide the original only after every result has been published.
        source.hide_set(True)
        source.hide_render = True

        return objects

    except Exception:
        # Roll back only the objects and collections owned by this operation.
        for obj in objects:
            bpy.data.objects.remove(
                obj,
                do_unlink=True,
            )

        if job is not None:
            bpy.data.collections.remove(job)

        if root_created:
            bpy.data.collections.remove(root)
        elif root_linked:
            context.scene.collection.children.unlink(root)

        for mesh in meshes:
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)

        source.hide_set(hidden_before)
        source.hide_render = render_before

        for obj in selected_before:
            obj.select_set(True)

        context.view_layer.objects.active = active_before
        raise


# ---------------------------------------------------------------------------
# Modal operator
# ---------------------------------------------------------------------------

class SNAP_OT_freehand_cut(Operator):
    """Preview and execute a local planar cut from a freehand stroke."""

    bl_idname = "snapsplit.freehand_cut"
    bl_label = "Freehand Cut"
    bl_description = (
        "Draw a local planar cut and preview touched material regions. "
        "Press Enter to split; Cap seams during split controls closure"
    )

    bl_options = {'REGISTER', 'UNDO'}

    brush_radius_px: FloatProperty(
        name="Brush Radius",
        description=(
            "Screen-space tolerance for touching a section loop"
        ),
        default=DEFAULT_BRUSH_RADIUS,
        min=1.0,
        max=100.0,
        options={'SKIP_SAVE'},
    )

    @classmethod
    def poll(cls, context):
        """Require a 3D viewport and an active mesh in Object Mode."""
        obj = context.active_object

        return (
            context.area is not None
            and context.area.type == 'VIEW_3D'
            and context.mode == 'OBJECT'
            and obj is not None
            and obj.type == 'MESH'
        )

    def invoke(self, context, event):
        """Start previewing and install viewport-scoped draw handlers."""
        if _ACTIVE_OPERATORS:
            report_user(
                self,
                'WARNING',
                "A Freehand Cut preview is already active.",
            )
            return {'CANCELLED'}

        obj = context.active_object

        if obj.modifiers:
            report_user(
                self,
                'ERROR',
                "Freehand Cut requires an object without modifiers. "
                "Apply or remove the modifiers first.",
            )
            return {'CANCELLED'}

        if obj.data.shape_keys is not None:
            report_user(
                self,
                'ERROR',
                "Freehand Cut does not support shape keys.",
            )
            return {'CANCELLED'}

        if not obj.data.polygons:
            report_user(
                self,
                'ERROR',
                "The active mesh has no faces.",
            )
            return {'CANCELLED'}

        if context.space_data.region_quadviews:
            report_user(
                self,
                'ERROR',
                "Please leave Quad View before starting Freehand Cut.",
            )
            return {'CANCELLED'}

        region = next(
            (
                region
                for region in context.area.regions
                if region.type == 'WINDOW'
            ),
            None,
        )

        if region is None:
            report_user(
                self,
                'ERROR',
                "No viewport window region was found.",
            )
            return {'CANCELLED'}

        try:
            obj.matrix_world.inverted()
        except ValueError:
            report_user(
                self,
                'ERROR',
                "The object transform is singular.",
            )
            return {'CANCELLED'}

        self._obj = obj
        self._mesh = obj.data
        self._matrix_world = obj.matrix_world.copy()
        self._mesh_counts = self._counts()
        self._geometry_signature = _geometry_signature(
            self._mesh
        )

        self._cut_bm = None
        self._cut_loops = []
        self._cut_loop_edges = []
        self._cut_selected = set()
        self._cut_tolerance = None
        self._cut_invalid_count = 0

        self._area = context.area
        self._region = region
        self._rv3d = context.space_data.region_3d
        self._window = context.window
        self._wm = context.window_manager

        self._handle_pixel = None
        self._handle_view = None
        self._timer = None
        self._closed = False
        self._drawing = False
        self._points = []
        self._stroke_batch = None
        self._preview_batches = []
        self._plane_point = None
        self._plane_normal = None
        self._selected_count = 0
        self._draw_error = None

        try:
            self._shader = gpu.shader.from_builtin(
                'POLYLINE_UNIFORM_COLOR'
            )
            self._polyline_shader = True

        except Exception:
            try:
                self._shader = gpu.shader.from_builtin(
                    'UNIFORM_COLOR'
                )
                self._polyline_shader = False

            except Exception as exc:
                self._cleanup()
                report_user(
                    self,
                    'ERROR',
                    "Cannot create preview shader: {error}",
                    error=exc,
                )
                return {'CANCELLED'}

        try:
            self._handle_pixel = (
                bpy.types.SpaceView3D.draw_handler_add(
                    self._draw_pixel,
                    (),
                    'WINDOW',
                    'POST_PIXEL',
                )
            )
            self._handle_view = (
                bpy.types.SpaceView3D.draw_handler_add(
                    self._draw_view,
                    (),
                    'WINDOW',
                    'POST_VIEW',
                )
            )
            self._timer = self._wm.event_timer_add(
                0.25,
                window=self._window,
            )

            _ACTIVE_OPERATORS.append(self)
            self._wm.modal_handler_add(self)

            self._set_header(
                "Draw with LMB | Shift-release: axis snap | Esc/RMB: exit"
            )

        except Exception as exc:
            self._cleanup()
            report_user(
                self,
                'ERROR',
                "Cannot start preview: {error}",
                error=exc,
            )
            return {'CANCELLED'}

        warn_if_unapplied_transforms(
            obj,
            operator=self,
        )
        self._area.tag_redraw()
        return {'RUNNING_MODAL'}

    def _clear_cut_data(self):
        """Free retained preview geometry and reset the cutting payload."""
        bm = getattr(self, "_cut_bm", None)

        # Clear the reference before releasing the owned resource.
        self._cut_bm = None
        self._cut_loops = []
        self._cut_loop_edges = []
        self._cut_selected = set()
        self._cut_tolerance = None
        self._cut_invalid_count = 0


        if bm is not None:
            bm.free()

    def _commit_cut(self, context):
        """Validate the source and publish only completely prepared results."""
        if not self._source_valid(context):
            raise ValueError(
                "The source object changed. Start Freehand Cut again."
            )

        if (
            _geometry_signature(self._mesh)
            != self._geometry_signature
        ):
            raise ValueError(
                "Source coordinates or topology changed. "
                "Start Freehand Cut again."
            )

        if self._mesh.shape_keys is not None:
            raise ValueError(
                "Shape keys are not supported."
            )

        # Seam migration is deliberately reserved for stage C.
        if any(
            str(key).startswith("snapsplit_seam")
            for key in self._obj.keys()
        ):
            raise ValueError(
                "The source has existing seam metadata. "
                "Repeated cutting requires seam migration "
                "and is not supported in this stage."

            )

        # Result objects do not inherit rigging, animation or constraints.
        if (
            self._obj.vertex_groups
            or self._obj.constraints
            or self._obj.animation_data is not None
            or self._mesh.animation_data is not None
        ):
            raise ValueError(
                "This cutting version does not support vertex groups, "
                "constraints or animation."
            )

        # Read the shared split setting when the user confirms the cut.
        cap_seams = bool(
            context.scene.snapsplit.cap_seams_during_split
        )

        meshes, seam_regions = _build_freehand_meshes(
            self,
            cap_seams,
        )

        objects = _publish_freehand_parts(
            context,
            self,
            meshes,
            seam_regions,
            cap_seams,
        )

        return len(objects), cap_seams



    def _counts(self):
        """Return a cheap topology signature for the original mesh."""
        return (
            len(self._mesh.vertices),
            len(self._mesh.edges),
            len(self._mesh.polygons),
        )

    def _source_valid(self, context):
        """Reject obvious source changes rather than showing stale geometry."""
        try:
            return (
                context.mode == 'OBJECT'
                and context.active_object == self._obj
                and self._obj.data == self._mesh
                and not self._obj.modifiers
                and self._counts() == self._mesh_counts
                and self._obj.matrix_world == self._matrix_world
            )
        except ReferenceError:
            return False

    def _mouse(self, event):
        """Convert window coordinates to the originating WINDOW region."""
        return Vector((
            event.mouse_x - self._region.x,
            event.mouse_y - self._region.y,
        ))

    def _inside(self, point):
        """Test whether a mouse position lies inside the viewport."""
        return (
            0 <= point.x < self._region.width
            and 0 <= point.y < self._region.height
        )

    def _ray(self, coordinate):
        """Build a world-space ray from the current viewport."""
        origin = view3d_utils.region_2d_to_origin_3d(
            self._region,
            self._rv3d,
            coordinate,
        )
        direction = (
            view3d_utils.region_2d_to_vector_3d(
                self._region,
                self._rv3d,
                coordinate,
            ).normalized()
        )
        return origin, direction

    def _hit(self, coordinate):
        """Raycast only the active object and return a world-space hit."""
        origin, direction = self._ray(coordinate)
        inverse = self._matrix_world.inverted()

        local_origin = inverse @ origin
        local_direction = inverse.to_3x3() @ direction

        if local_direction.length_squared <= 1e-20:
            return None

        result, location, _normal, _index = self._obj.ray_cast(
            local_origin,
            local_direction.normalized(),
        )

        return (
            self._matrix_world @ location
            if result
            else None
        )

    def _append_point(self, point, force=False):
        """Collect a bounded stroke while preserving its complete extent."""
        if (
            not self._points
            or force
            or (point - self._points[-1]).length >= 2.0
        ):
            if (
                self._points
                and (point - self._points[-1]).length < 1e-6
            ):
                return

            self._points.append(point.copy())

            if len(self._points) > MAX_STROKE_POINTS:
                self._points = (
                    self._points[::2]
                    + [self._points[-1]]
                )

            if len(self._points) >= 2:
                self._stroke_batch = batch_for_shader(
                    self._shader,
                    'LINE_STRIP',
                    {
                        "pos": [
                            (point.x, point.y, 0.0)
                            for point in self._points
                        ]
                    },
                )

    def _world_pixel_radius(self, coordinate, world_point):
        """Convert brush pixels to a world-space tolerance at the hit depth."""
        center = view3d_utils.region_2d_to_location_3d(
            self._region,
            self._rv3d,
            coordinate,
            world_point,
        )
        shifted = view3d_utils.region_2d_to_location_3d(
            self._region,
            self._rv3d,
            coordinate + Vector((self.brush_radius_px, 0.0)),
            world_point,
        )
        return (shifted - center).length

    def _build_preview(self, snap):
        """Fit the plane and retain the exact locally selected cut geometry."""
        self._clear_cut_data()
        self._preview_batches = []
        self._selected_count = 0
        self._plane_point = None
        self._plane_normal = None

        if (
            _geometry_signature(self._mesh)
            != self._geometry_signature
        ):
            raise ValueError(
                "Source coordinates or topology changed. "
                "Start Freehand Cut again."
            )

        samples = _resample_stroke(self._points)
        _center, endpoint_a, endpoint_b = _fit_line(samples)

        hits = []
        for coordinate in samples:
            location = self._hit(coordinate)
            if location is not None:
                hits.append((coordinate, location))

        if not hits:
            raise ValueError(
                "The stroke did not hit the active mesh."
            )

        origin_a, direction_a = self._ray(endpoint_a)
        origin_b, direction_b = self._ray(endpoint_b)

        if self._rv3d.is_perspective:
            normal = direction_a.cross(direction_b)
        else:
            normal = (
                origin_b - origin_a
            ).cross(direction_a)

        if normal.length_squared <= 1e-16:
            raise ValueError(
                "Cannot determine a stable cutting plane."
            )

        normal.normalize()

        # Anchor near the surface instead of using a distant camera origin.
        anchor = (
            sum(
                (hit for _, hit in hits),
                Vector((0.0, 0.0, 0.0)),
            )
            / len(hits)
        )
        plane_point = (
            anchor
            - normal * (anchor - origin_a).dot(normal)
        )

        if snap:
            axis = max(
                range(3),
                key=lambda index: abs(normal[index]),
            )
            sign = 1.0 if normal[axis] >= 0.0 else -1.0
            normal = Vector((0.0, 0.0, 0.0))
            normal[axis] = sign
            plane_point = anchor.copy()

        corners = [
            self._matrix_world @ Vector(corner)
            for corner in self._obj.bound_box
        ]
        low = Vector(tuple(
            min(point[i] for point in corners)
            for i in range(3)
        ))
        high = Vector(tuple(
            max(point[i] for point in corners)
            for i in range(3)
        ))
        diagonal = (high - low).length

        if diagonal <= 1e-12:
            raise ValueError(
                "The object is too small or degenerate."
            )

        tolerance = max(
            diagonal * 1e-7,
            1e-10,
        )

        # The retained BMesh uses this exact offset plane for the actual cut.
        plane_point += normal * (tolerance * 4.0)

        (
            loops,
            invalid_segments,
            invalid_count,
            self._cut_bm,
            loop_edges,
        ) = _extract_sections(
            self._mesh,
            self._matrix_world,
            plane_point,
            normal,
            tolerance,
            keep_bmesh=True,
        )

        u, v = _plane_basis(normal)
        polygons = [
            [
                Vector((
                    (point - plane_point).dot(u),
                    (point - plane_point).dot(v),
                ))
                for point in loop
            ]
            for loop in loops
        ]

        selected = set()

        for coordinate, hit in hits:
            projected = (
                hit
                - normal * (hit - plane_point).dot(normal)
            )
            point_2d = Vector((
                (projected - plane_point).dot(u),
                (projected - plane_point).dot(v),
            ))
            radius = max(
                self._world_pixel_radius(coordinate, hit),
                tolerance * 8.0,
            )

            eligible = []

            for index, polygon in enumerate(polygons):
                distance = _polygon_distance(
                    point_2d,
                    polygon,
                )

                if (
                    distance <= radius
                    or _point_in_polygon(point_2d, polygon)
                ):
                    eligible.append((distance, index))
            if eligible:
                # First identify the nearest touched boundary.
                selected.add(min(eligible)[1])

        # Expand touched boundaries to complete material regions.
        # Inner rims are visibly selected before Enter can cut them.
        _polygons, groups = _section_groups(
            loops,
            plane_point,
            normal,
            tolerance * 2.0,
        )
        selected = _expand_section_selection(selected, groups)
        self._cut_invalid_count = invalid_count

        selected_region_count = sum(
            bool(selected.intersection(group["indices"]))
            for group in groups
        )

        for index, loop in enumerate(loops):

            coordinates = []

            for i, point in enumerate(loop):
                coordinates.extend((
                    point,
                    loop[(i + 1) % len(loop)],
                ))

            batch = batch_for_shader(
                self._shader,
                'LINES',
                {"pos": coordinates},
            )
            self._preview_batches.append((
                batch,
                ORANGE if index in selected else GRAY,
                3.0 if index in selected else 1.5,
            ))

        if invalid_segments:
            batch = batch_for_shader(
                self._shader,
                'LINES',
                {"pos": invalid_segments},
            )
            self._preview_batches.append((
                batch,
                INVALID_COLOR,
                2.0,
            ))

        self._plane_point = plane_point.copy()
        self._plane_normal = normal.copy()
        self._selected_count = len(selected)

        self._cut_loops = loops
        self._cut_loop_edges = loop_edges
        self._cut_selected = set(selected)
        self._cut_tolerance = tolerance

        self._set_header(
            f"Preview: {selected_region_count}/{len(groups)} material regions"
            f" | {len(selected)} boundary loops selected"
            " | Enter: cut | LMB: redraw | MMB: orbit | Esc: exit"
        )

        report_user(
            self,
            'INFO',
            "Preview: {selected} of {total} material regions selected "
            "with {loops} boundary loops. No mesh was changed.",
            selected=selected_region_count,
            total=len(groups),
            loops=len(selected),
        )


        if invalid_count:
            report_user(
                self,
                'WARNING',
                "{count} open or branched section(s) "
                "were excluded and shown in red.",
                count=invalid_count,
            )

        if not selected:
            report_user(
                self,
                'WARNING',
                "No valid section loop was touched. "
                "Try a straighter stroke.",
            )

    # -----------------------------------------------------------------------
    # Drawing
    # -----------------------------------------------------------------------

    def _draw_here(self):
        """Restrict shared SpaceView3D handlers to the originating region."""
        context = bpy.context

        return (
            not self._closed
            and context.area == self._area
            and context.region == self._region
        )

    def _draw_batches(self, batches):
        """Draw cached batches and restore the previous GPU state."""
        old_blend = gpu.state.blend_get()
        old_depth = gpu.state.depth_test_get()
        old_mask = gpu.state.depth_mask_get()
        old_width = gpu.state.line_width_get()

        try:
            gpu.state.blend_set('ALPHA')
            gpu.state.depth_test_set('NONE')
            gpu.state.depth_mask_set(False)

            self._shader.bind()

            for batch, color, width in batches:
                self._shader.uniform_float(
                    "color",
                    color,
                )

                if self._polyline_shader:
                    self._shader.uniform_float(
                        "viewportSize",
                        gpu.state.viewport_get()[2:],
                    )
                    self._shader.uniform_float(
                        "lineWidth",
                        width,
                    )
                else:
                    gpu.state.line_width_set(1.0)

                batch.draw(self._shader)

        finally:
            gpu.state.line_width_set(old_width)
            gpu.state.depth_mask_set(old_mask)
            gpu.state.depth_test_set(old_depth)
            gpu.state.blend_set(old_blend)

    def _draw_pixel(self):
        """Draw the stroke in screen space only while dragging."""
        if (
            not self._draw_here()
            or not self._drawing
            or self._stroke_batch is None
        ):
            return

        try:
            self._draw_batches([
                (self._stroke_batch, ORANGE, 3.0)
            ])
        except Exception as exc:
            self._draw_error = str(exc)

    def _draw_view(self):
        """Draw section loops in world space, including hidden portions."""
        if (
            not self._draw_here()
            or self._drawing
            or not self._preview_batches
        ):
            return

        try:
            self._draw_batches(self._preview_batches)
        except Exception as exc:
            self._draw_error = str(exc)

    def _set_header(self, text):
        """Display modal instructions in the viewport header."""
        self._area.header_text_set(text)

    # -----------------------------------------------------------------------
    # Resource lifecycle
    # -----------------------------------------------------------------------

    def _cleanup(self):
        """Remove every owned resource; repeated calls are harmless."""
        if getattr(self, "_closed", True):
            return

        self._closed = True
        self._clear_cut_data()

        for attribute in (
            "_handle_pixel",
            "_handle_view",
        ):
            handle = getattr(self, attribute, None)

            if handle is not None:
                try:
                    bpy.types.SpaceView3D.draw_handler_remove(
                        handle,
                        'WINDOW',
                    )
                except (
                    ReferenceError,
                    ValueError,
                    RuntimeError,
                ):
                    pass

                setattr(self, attribute, None)

        if self._timer is not None:
            try:
                self._wm.event_timer_remove(self._timer)
            except (
                ReferenceError,
                ValueError,
                RuntimeError,
            ):
                pass

            self._timer = None

        try:
            self._area.header_text_set(None)
            self._area.tag_redraw()
        except ReferenceError:
            pass

        self._stroke_batch = None
        self._preview_batches = []

        if self in _ACTIVE_OPERATORS:
            _ACTIVE_OPERATORS.remove(self)

    def cancel(self, context):
        """Support Blender-driven cancellation as well as explicit exit."""
        self._cleanup()

    # -----------------------------------------------------------------------
    # Modal interaction
    # -----------------------------------------------------------------------

    def modal(self, context, event):
        """Handle drawing, cutting, navigation and safe cancellation."""
        if self._closed:
            return {'CANCELLED'}

        try:
            # Collection membership expects names, so compare Area objects.
            if not any(
                area == self._area
                for area in self._window.screen.areas
            ):
                self._cleanup()
                return {'CANCELLED'}

            if not self._source_valid(context):
                report_user(
                    self,
                    'WARNING',
                    "The active object changed. "
                    "Freehand Cut preview was cancelled.",
                )
                self._cleanup()
                return {'CANCELLED'}

            if self._draw_error is not None:
                report_user(
                    self,
                    'ERROR',
                    "Preview drawing failed: {error}",
                    error=self._draw_error,
                )
                self._cleanup()
                return {'CANCELLED'}

            if (
                event.type in {'ESC', 'RIGHTMOUSE'}
                and event.value == 'PRESS'
            ):
                self._cleanup()
                return {'CANCELLED'}

            if event.type == 'TIMER':
                return {'RUNNING_MODAL'}

            point = self._mouse(event)

            if (
                event.type == 'LEFTMOUSE'
                and event.value == 'PRESS'
            ):
                if not self._inside(point):
                    return {'RUNNING_MODAL'}

                # Preserve alternative Alt-LMB navigation layouts.
                if event.alt:
                    return {'PASS_THROUGH'}

                self._clear_cut_data()
                self._drawing = True
                self._points = []
                self._stroke_batch = None
                self._preview_batches = []
                self._selected_count = 0
                self._plane_point = None
                self._plane_normal = None

                self._append_point(point)
                self._set_header(
                    "Drawing | Release LMB to preview | Shift: axis snap"
                )
                self._area.tag_redraw()
                return {'RUNNING_MODAL'}

            if self._drawing:
                if event.type == 'MOUSEMOVE':
                    self._append_point(point)
                    self._area.tag_redraw()
                    return {'RUNNING_MODAL'}

                if (
                    event.type == 'LEFTMOUSE'
                    and event.value == 'RELEASE'
                ):
                    self._append_point(
                        point,
                        force=True,
                    )
                    self._drawing = False
                    self._stroke_batch = None

                    try:
                        self._build_preview(
                            snap=event.shift
                        )

                    except (ValueError, RuntimeError) as exc:
                        self._clear_cut_data()
                        self._preview_batches = []
                        self._selected_count = 0
                        self._plane_point = None
                        self._plane_normal = None

                        self._set_header(
                            "Draw again with LMB"
                            " | Shift-release: axis snap | Esc: exit"
                        )

                        report_user(
                            self,
                            'WARNING',
                            "Preview unavailable: {error}",
                            error=exc,
                        )

                    self._area.tag_redraw()
                    return {'RUNNING_MODAL'}

                # Keep the camera unchanged during a single stroke.
                return {'RUNNING_MODAL'}

            if (
                event.type in {'RET', 'NUMPAD_ENTER'}
                and event.value == 'PRESS'
            ):
                if not self._selected_count:
                    report_user(
                        self,
                        'WARNING',
                        "Draw a stroke that touches "
                        "at least one valid section loop.",
                    )
                    return {'RUNNING_MODAL'}

                try:
                    count, cap_seams = self._commit_cut(context)


                except Exception as exc:
                    # Rejected cuts retain the preview and the untouched source.
                    report_user(
                        self,
                        'ERROR',
                        "Freehand cut was not completed: {error}",
                        error=exc,
                    )
                    return {'RUNNING_MODAL'}

                self._cleanup()

                # Report the actual boundary state of the published parts.
                message = (
                    "Freehand cut created {count} closed parts. "
                    "The unchanged original was hidden."
                    if cap_seams
                    else
                    "Freehand cut created {count} parts with open cut boundaries. "
                    "The unchanged original was hidden."
                )

                report_user(
                    self,
                    'INFO',
                    message,
                    count=count,
                )

                return {'FINISHED'}

            navigation = {
                'MIDDLEMOUSE',
                'WHEELUPMOUSE',
                'WHEELDOWNMOUSE',
                'TRACKPADPAN',
                'TRACKPADZOOM',
                'MOUSEROTATE',
                'MOUSESMARTZOOM',
                'NDOF_MOTION',
                'NUMPAD_0',
                'NUMPAD_1',
                'NUMPAD_2',
                'NUMPAD_3',
                'NUMPAD_4',
                'NUMPAD_5',
                'NUMPAD_6',
                'NUMPAD_7',
                'NUMPAD_8',
                'NUMPAD_9',
                'NUMPAD_PERIOD',
                'NUMPAD_PLUS',
                'NUMPAD_MINUS',
            }

            if event.type in navigation:
                return {'PASS_THROUGH'}

            if event.type == 'MOUSEMOVE':
                return {'PASS_THROUGH'}

            # Block editing shortcuts while the source-dependent preview runs.
            return {'RUNNING_MODAL'}

        except Exception as exc:
            report_user(
                self,
                'ERROR',
                "Freehand Cut failed: {error}",
                error=exc,
            )
            self._cleanup()
            return {'CANCELLED'}


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_CLASSES = (SNAP_OT_freehand_cut,)


def register():
    """Register the combined preview and local cutting operator."""
    for cls in _CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    """Close active previews before unregistering the operator class."""
    for operator in tuple(_ACTIVE_OPERATORS):
        operator._cleanup()

    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)
