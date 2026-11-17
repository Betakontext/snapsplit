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



# seam_regions.py

import math
from collections import defaultdict

from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt


class RegionError(ValueError):
    """Indicate inconsistent or numerically ambiguous contact geometry."""


def signed_area(points):
    """Return signed polygon area using double-precision scalar arithmetic."""
    if len(points) < 3:
        return 0.0

    # Translate to reduce cancellation for polygons far from the origin.
    reference_x = float(points[0].x)
    reference_y = float(points[0].y)

    return 0.5 * math.fsum(
        (float(points[index].x) - reference_x)
        * (float(points[(index + 1) % len(points)].y) - reference_y)
        - (float(points[(index + 1) % len(points)].x) - reference_x)
        * (float(points[index].y) - reference_y)
        for index in range(len(points))
    )


def inside_polygon(point, polygon):
    """Classify a point using an odd-even ray without a boundary offset."""
    if len(polygon) < 3:
        return False

    inside = False
    previous = polygon[-1]

    for current in polygon:
        if (current.y > point.y) != (previous.y > point.y):
            crossing = (
                (previous.x - current.x)
                * (point.y - current.y)
                / (previous.y - current.y)
                + current.x
            )
            if point.x < crossing:
                inside = not inside

        previous = current

    return inside


def inside_region(point, loops):
    """Accept the outer polygon while excluding every stored hole."""
    return bool(loops) and (
        inside_polygon(point, loops[0])
        and not any(
            inside_polygon(point, hole)
            for hole in loops[1:]
        )
    )


def frame_tolerance(frame):
    """Derive a world-space tolerance from the current region dimensions."""
    loops = frame.get("loops")

    if not loops or any(len(loop) < 3 for loop in loops):
        raise RegionError("A stored contact has invalid contour loops.")

    reference = loops[0][0]
    span = max(
        (point - reference).length
        for loop in loops
        for point in loop
    )

    if not math.isfinite(span):
        raise RegionError("A stored contact contains invalid coordinates.")

    return max(1e-7, span * 1e-6)


def _check_closed_mesh(obj):
    """Require a nonempty closed edge-manifold mesh without loose vertices."""
    mesh = obj.data

    if not mesh.vertices or not mesh.polygons:
        raise RegionError(f"'{obj.name}' has no closed mesh surface.")

    counts = defaultdict(int)
    used_vertices = set()

    for polygon in mesh.polygons:
        used_vertices.update(polygon.vertices)

        for edge in polygon.edge_keys:
            counts[tuple(sorted(edge))] += 1

    if (
        len(used_vertices) != len(mesh.vertices)
        or any(
            counts[tuple(sorted(edge.vertices))] != 2
            for edge in mesh.edges
        )
        or any(count != 2 for count in counts.values())
    ):
        raise RegionError(
            f"'{obj.name}' is open or contains loose/non-manifold geometry."
        )


def _triangle_groups(vertices, faces):
    """Group triangles through shared edges, not through point contacts."""
    edge_faces = defaultdict(list)

    for index, face in enumerate(faces):
        for offset in range(3):
            edge = tuple(sorted((
                face[offset],
                face[(offset + 1) % 3],
            )))
            edge_faces[edge].append(index)

    adjacency = [set() for _face in faces]

    for linked in edge_faces.values():
        if len(linked) > 2:
            raise RegionError(
                "The planar overlay contains non-manifold edges."
            )

        if len(linked) == 2:
            a, b = linked
            adjacency[a].add(b)
            adjacency[b].add(a)

    remaining = set(range(len(faces)))
    groups = []

    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        group = {seed}
        pending = [seed]

        while pending:
            current = pending.pop()
            neighbors = adjacency[current] & remaining
            remaining.difference_update(neighbors)
            group.update(neighbors)
            pending.extend(sorted(neighbors))

        groups.append([
            faces[index]
            for index in sorted(group)
        ])

    return groups


def _group_boundaries(vertices, faces):
    """Recover outer and hole cycles from a connected triangle region."""
    occurrences = defaultdict(list)

    for face in faces:
        for index in range(3):
            edge = (face[index], face[(index + 1) % 3])
            occurrences[tuple(sorted(edge))].append(edge)

    if any(len(items) > 2 for items in occurrences.values()):
        raise RegionError(
            "A contact region contains a non-manifold triangulation."
        )

    # Interior edges must have opposite directions in adjacent triangles.
    for directed in occurrences.values():
        if len(directed) == 2:
            first, second = directed
            if first != (second[1], second[0]):
                raise RegionError(
                    "A contact region has inconsistent triangle winding."
                )

    boundary = [
        directed[0]
        for directed in occurrences.values()
        if len(directed) == 1
    ]

    outgoing = {}
    incoming = {}

    for a, b in boundary:
        if a in outgoing or b in incoming:
            raise RegionError(
                "A contact region has a touching or branched boundary."
            )

        outgoing[a] = b
        incoming[b] = a

    if not boundary or set(outgoing) != set(incoming):
        raise RegionError("A contact region has an open boundary.")

    remaining = set(outgoing)
    cycles = []

    while remaining:
        start = min(remaining)
        current = start
        indices = []

        while current in remaining:
            remaining.remove(current)
            indices.append(current)
            current = outgoing[current]

        if current != start or len(indices) < 3:
            raise RegionError("A contact boundary could not be ordered.")

        cycles.append([
            vertices[index]
            for index in indices
        ])

    outers = [
        loop
        for loop in cycles
        if signed_area(loop) > 0.0
    ]
    holes = [
        loop
        for loop in cycles
        if signed_area(loop) < 0.0
    ]

    if len(outers) != 1 or len(outers) + len(holes) != len(cycles):
        raise RegionError(
            "A contact region has ambiguous outer boundaries."
        )

    outer = outers[0]

    if any(not inside_polygon(hole[0], outer) for hole in holes):
        raise RegionError(
            "A contact hole lies outside its outer boundary."
        )

    return [outer, *holes]

def _diagnostic_triangle_distance(point, triangle):
    """Measure planar distance to a filled triangle using scalar arithmetic."""
    px, py = float(point.x), float(point.y)
    points = [
        (float(vertex.x), float(vertex.y))
        for vertex in triangle
    ]

    signs = []
    distances = []

    for index in range(3):
        ax, ay = points[index]
        bx, by = points[(index + 1) % 3]
        dx, dy = bx - ax, by - ay
        rx, ry = px - ax, py - ay

        signs.append(dx * ry - dy * rx)
        length_squared = dx * dx + dy * dy

        if length_squared == 0.0:
            distances.append(math.hypot(rx, ry))
            continue

        parameter = max(
            0.0,
            min(1.0, (rx * dx + ry * dy) / length_squared),
        )
        distances.append(
            math.hypot(rx - parameter * dx, ry - parameter * dy)
        )

    ax, ay = points[0]
    bx, by = points[1]
    cx, cy = points[2]
    area_twice = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)

    if area_twice != 0.0 and (
        min(signs) >= 0.0 or max(signs) <= 0.0
    ):
        return 0.0

    return min(distances)


def _missing_coverage_report(
    polygon,
    objects,
    diagnostic_surfaces,
    scale,
    tolerance,
    creation_tolerance,
):
    """Report sampled distances without changing coverage decisions."""
    samples = list(polygon)
    samples.extend(
        (polygon[index] + polygon[(index + 1) % 3]) * 0.5
        for index in range(3)
    )
    samples.append(
        sum(polygon, Vector((0.0, 0.0))) / 3.0
    )

    lines = [
        "[SnapSplit coverage diagnostic]",
        f"Current world tolerance: {tolerance:.12g}",
        f"Stored creation tolerance: {creation_tolerance!r}",
        "All following distances are in Blender world units.",
        "Samples: 3 vertices, 3 edge midpoints, 1 centroid.",
    ]

    for obj, entries in zip(objects, diagnostic_surfaces):
        accepted = [entry for entry in entries if entry[2]]
        rejected = [entry for entry in entries if not entry[2]]

        lines.append(
            f"Object {obj.name!r}: "
            f"accepted_planar_triangles={len(accepted)}, "
            f"rejected_by_plane={len(rejected)}"
        )

        if accepted:
            gaps = [
                min(
                    _diagnostic_triangle_distance(sample, entry[0])
                    for entry in accepted
                ) * scale
                for sample in samples
            ]
            lines.append(
                "  Sample distances to accepted projected surface: "
                + ", ".join(f"{gap:.12g}" for gap in gaps)
            )
            lines.append(
                f"  Largest sampled gap / current tolerance: "
                f"{max(gaps) / tolerance:.12g}"
            )
        else:
            lines.append("  No accepted planar surface triangles.")

        if rejected:
            centroid = samples[-1]
            nearest = min(
                rejected,
                key=lambda entry: _diagnostic_triangle_distance(
                    centroid, entry[0]
                ),
            )
            projected_gap = _diagnostic_triangle_distance(
                centroid, nearest[0]
            ) * scale

            lines.append(
                "  Nearest plane-rejected triangle by projected centroid "
                f"distance: polygon={nearest[3]}, "
                f"projected_gap={projected_gap:.12g}, "
                f"maximum_plane_deviation={nearest[1]:.12g}"
            )

    lines.append(
        "Diagnostic samples are not a proof of complete surface coverage. "
        "Plane-rejected triangles are diagnostic candidates, not owners."
    )
    return "\n".join(lines)

def _point_surface_distance(point, triangles):
    """Measure distance to a union of filled triangles using Python floats."""
    px, py = point
    best = math.inf

    for triangle in triangles:
        signs = []
        edge_distances = []

        for index in range(3):
            ax, ay = triangle[index]
            bx, by = triangle[(index + 1) % 3]
            dx, dy = bx - ax, by - ay
            rx, ry = px - ax, py - ay

            signs.append(dx * ry - dy * rx)
            length_squared = dx * dx + dy * dy

            if length_squared == 0.0:
                edge_distances.append(math.hypot(rx, ry))
                continue

            parameter = max(
                0.0,
                min(1.0, (rx * dx + ry * dy) / length_squared),
            )
            edge_distances.append(
                math.hypot(
                    rx - parameter * dx,
                    ry - parameter * dy,
                )
            )

        ax, ay = triangle[0]
        bx, by = triangle[1]
        cx, cy = triangle[2]
        area_twice = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)

        if area_twice != 0.0 and (
            min(signs) >= 0.0 or max(signs) <= 0.0
        ):
            return 0.0

        best = min(best, min(edge_distances))

    return best


def _cell_within_surface_tolerance(polygon,triangles,tolerance):
 return _ss_patch_cell_covered(polygon,triangles,tolerance)



def overlay_region(frame, objects, tolerance):
    """Partition a stored region using current planar surface ownership.

    Each retained CDT triangle must belong to exactly one input surface
    triangle of exactly one supplied object, with the expected orientation.

    Face provenance identifies the stored outer contour, stored holes,
    and surface triangles in one consistent CDT coordinate arrangement.

    Return one list of world-space contact frames per supplied object.
    """
    objects = list(objects)

    if not objects:
        raise RegionError("No contact owners were supplied.")

    if not math.isfinite(tolerance) or tolerance <= 0.0:
        raise RegionError("The contact tolerance must be finite and positive.")

    loops_world = frame.get("loops")

    if not loops_world or any(len(loop) < 3 for loop in loops_world):
        raise RegionError("A stored contact has invalid contour loops.")

    origin = frame["origin"].copy()
    normal = frame["normal"].copy()
    tangent = frame["tangent"].copy()

    if any(
        not math.isfinite(component)
        for vector in (origin, normal, tangent)
        for component in vector
    ):
        raise RegionError("A stored contact has an invalid coordinate frame.")

    if normal.length <= 1e-12 or tangent.length <= 1e-12:
        raise RegionError("A stored contact has a degenerate coordinate frame.")

    normal.normalize()
    tangent.normalize()

    # Reject malformed frames rather than silently changing their geometry.
    if abs(normal.dot(tangent)) > 1e-5:
        raise RegionError(
            "The stored contact tangent is not perpendicular to its normal."
        )

    x_axis = tangent - normal * tangent.dot(normal)
    x_axis.normalize()
    y_axis = normal.cross(x_axis).normalized()

    side = frame["side"]

    if side not in (-1, 1):
        raise RegionError("A stored contact has an invalid side value.")

    if any(
        not math.isfinite(component)
        for loop in loops_world
        for point in loop
        for component in point
    ):
        raise RegionError(
            "A stored contact region contains invalid coordinates."
        )

    if any(
        abs((point - origin).dot(normal)) > tolerance
        for loop in loops_world
        for point in loop
    ):
        raise RegionError("A stored contact contour is not planar.")

    scale = max(
        (point - origin).length
        for loop in loops_world
        for point in loop
    )

    if not math.isfinite(scale) or scale <= tolerance:
        raise RegionError("A contact region is too small or degenerate.")

    def project(point):
        """Project a world point into normalized planar coordinates."""
        delta = point - origin
        return Vector((
            delta.dot(x_axis) / scale,
            delta.dot(y_axis) / scale,
        ))

    def unproject(point):
        """Restore a normalized planar point to the stored world plane."""
        return origin + scale * (
            x_axis * point.x + y_axis * point.y
        )

    loops = [
        [project(point) for point in loop]
        for loop in loops_world
    ]

    loop_areas = [abs(signed_area(loop)) for loop in loops]

    if any(area <= 0.0 for area in loop_areas):
        raise RegionError("A stored contact contour is degenerate.")

    expected_area = loop_areas[0] - math.fsum(loop_areas[1:])

    if expected_area <= 0.0:
        raise RegionError("A stored contact region has no material area.")

    # Preserve the previous merging tolerance and area-error budget.
    epsilon = max(
        1e-10,
        min(1e-7, tolerance / scale * 0.02),
    )
    allowed_error = max(
        expected_area * 1e-5,
        epsilon * epsilon * 64.0,
    )

    coordinates = []
    input_faces = []

    def add_face(points):
        """Append one CCW face and return its input provenance index."""
        points = list(points)
        area = signed_area(points)

        if area == 0.0:
            raise RegionError(
                "A degenerate planar face cannot enter the contact overlay."
            )

        if area < 0.0:
            points.reverse()

        start = len(coordinates)
        coordinates.extend(points)
        face_id = len(input_faces)
        input_faces.append(
            list(range(start, start + len(points)))
        )
        return face_id

    # Holes are separate positive input faces, then excluded by provenance.
    outer_id = add_face(loops[0])
    hole_ids = {
        add_face(loop)
        for loop in loops[1:]
    }

    expected_normal = -side * normal
    surface_info = {}
    surface_geometry = {}
    surface_counts = []
    diagnostic_surfaces = []




    for owner_index, obj in enumerate(objects):
        if obj.type != 'MESH' or obj.data is None:
            raise RegionError("Contact owners must be mesh objects.")

        _check_closed_mesh(obj)

        matrix = obj.matrix_world
        world = [
            matrix @ vertex.co
            for vertex in obj.data.vertices
        ]

        if any(
            not math.isfinite(component)
            for point in world
            for component in point
        ):
            raise RegionError(
                f"'{obj.name}' contains invalid coordinates."
            )

        obj.data.calc_loop_triangles()
        count = 0
        diagnostic_entries = []
        diagnostic_surfaces.append(diagnostic_entries)


        for item in obj.data.loop_triangles:
            points = [
                world[index]
                for index in item.vertices
            ]

            plane_deviation = max(
                abs((point - origin).dot(normal))
                for point in points
            )
            projected = [project(point) for point in points]
            planar = plane_deviation <= tolerance

            diagnostic_entries.append((
                projected,
                plane_deviation,
                planar,
                item.polygon_index,
            ))

            if not planar:
                continue


            # Do not drop small nonzero triangles based on epsilon.
            if signed_area(projected) == 0.0:
                continue

            area_vector = (
                (points[1] - points[0]).cross(
                    points[2] - points[0]
                )
            )

            if area_vector.length == 0.0:
                raise RegionError(
                    f"'{obj.name}' has a numerically degenerate planar triangle."
                )

            orientation_ok = (
                area_vector.normalized().dot(expected_normal)
                >= 1.0 - 1e-5
            )

            face_id = add_face(projected)
            surface_info[face_id] = (
                owner_index,
                orientation_ok,
                item.polygon_index,
            )
            surface_geometry[face_id] = projected
            count += 1


        surface_counts.append(count)

    vertices, _edges, faces, _ov, _oe, original_faces = delaunay_2d_cdt(
        coordinates,
        [],
        input_faces,
        0,
        epsilon,
        True,
    )

    if len(original_faces) != len(faces):
        raise RegionError(
            "The contact overlay returned incomplete face provenance."
        )

    assigned = [[] for _obj in objects]
    covered_areas = []
    omitted_areas = []
    retained_count = 0
    omitted_cells = []


    for cell_index, (face, provenance) in enumerate(
        zip(faces, original_faces)
    ):
        source_ids = set(provenance)

        if outer_id not in source_ids:
            continue

        if source_ids & hole_ids:
            continue

        retained_count += 1

        if len(face) != 3:
            raise RegionError(
                "The contact overlay returned a non-triangle."
            )

        polygon = [vertices[index] for index in face]
        area_signed = signed_area(polygon)
        area = abs(area_signed)

        if not math.isfinite(area) or area == 0.0:
            raise RegionError(
                "The contact overlay returned a degenerate material cell."
            )

        hits = [
            surface_info[face_id]
            for face_id in sorted(source_ids)
            if face_id in surface_info
        ]

        owners = sorted({
            owner_index
            for owner_index, _orientation, _polygon in hits
        })

        # Report world-space area and tolerance for reproducible diagnostics.
        cell_area_world = area * scale * scale
        object_summary = ", ".join(
            f"{obj.name!r}:{count}"
            for obj, count in zip(objects, surface_counts)
        )
        details = (
            f"cell={cell_index}, "
            f"area_world={cell_area_world:.9g}, "
            f"tolerance_world={tolerance:.9g}, "
            f"epsilon_normalized={epsilon:.9g}, "
            f"planar_triangles=[{object_summary}]"
        )

        if not owners:
            omitted_cells.append((polygon, details))
            omitted_areas.append(area)
            continue



        if len(owners) > 1:
            names = ", ".join(
                repr(objects[index].name)
                for index in owners
            )
            raise RegionError(
                "Stored contact has multiple result owners: "
                f"owners={len(owners)}, objects=[{names}]; "
                + details
            )

        if len(hits) != 1:
            owner_name = objects[owners[0]].name
            raise RegionError(
                "Overlapping planar triangles cover a contact cell: "
                f"object={owner_name!r}, triangle_hits={len(hits)}; "
                + details
            )

        owner_index, orientation_ok, polygon_index = hits[0]

        if not orientation_ok:
            raise RegionError(
                "A contact surface has inconsistent orientation: "
                f"object={objects[owner_index].name!r}, "
                f"polygon={polygon_index}; "
                + details
            )

        ordered = tuple(face)

        if area_signed < 0.0:
            ordered = tuple(reversed(ordered))

        assigned[owner_index].append(ordered)
        covered_areas.append(area)

    covered_area = math.fsum(covered_areas)
    omitted_area = math.fsum(omitted_areas)

    if retained_count == 0:
        raise RegionError(
            "The contact overlay retained no stored material cells."
        )

    partition_area = math.fsum((covered_area, omitted_area))

    if abs(partition_area - expected_area) > allowed_error:
        raise RegionError(
            "The contact overlay does not preserve its input partition: "
            f"expected_world={expected_area * scale * scale:.9g}, "
            f"partition_world={partition_area * scale * scale:.9g}, "
            f"allowed_error_world={allowed_error * scale * scale:.9g}."
        )

    if covered_area <= 0.0:
        raise RegionError(
            "The stored contact has no actual surface intersection."
        )

    # Only correctly oriented, actually retained surface triangles support
    # the tolerance proof. Rejected planes never become contact owners.
    supporting_ids = set()

    for provenance in original_faces:
        source_ids = set(provenance)

        if outer_id not in source_ids or source_ids & hole_ids:
            continue

        for face_id in source_ids:
            if face_id in surface_info and surface_info[face_id][1]:
                supporting_ids.add(face_id)

    supporting_triangles = [
        tuple(
            (float(point.x), float(point.y))
            for point in surface_geometry[face_id]
        )
        for face_id in sorted(supporting_ids)
    ]

    for polygon, details in omitted_cells:
        if _cell_within_surface_tolerance(
            polygon,
            supporting_triangles,
            tolerance / scale,
        ):
            continue

        report = _missing_coverage_report(
            polygon,
            objects,
            diagnostic_surfaces,
            scale,
            tolerance,
            frame.get("tolerance_world_at_creation"),
        )
        print(report, flush=True)

        raise RegionError(
            "Stored contact has uncovered geometry outside the "
            "certified surface tolerance, or its distance proof "
            "could not be resolved numerically; "
            + details
            + ". See the console coverage diagnostic."
        )


    result = [[] for _obj in objects]

    for owner_index, triangles in enumerate(assigned):
        for group in _triangle_groups(vertices, triangles):
            boundaries = _group_boundaries(vertices, group)
            part = dict(frame)
            part["loops"] = [
                [unproject(point) for point in loop]
                for loop in boundaries
            ]
            result[owner_index].append(part)

    if omitted_cells:
        print(
            "[SnapSplit] Contact intersection normalized: "
            f"omitted_cells={len(omitted_cells)}, "
            f"omitted_area_world={omitted_area * scale * scale:.9g}, "
            f"world_tolerance={tolerance:.9g}",
            flush=True,
        )


    return result


\
# SnapSplit freehand patch v3
def _ss_patch_f(v):
    v=float(v)
    if not math.isfinite(v): raise ValueError("non-finite coordinate")
    return v
def _ss_patch_xy(p):
    try: return _ss_patch_f(p.x),_ss_patch_f(p.y)
    except AttributeError: return _ss_patch_f(p[0]),_ss_patch_f(p[1])
def _ss_patch_cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def _ss_patch_area(p):
    if len(p)<3:return 0.0
    x,y=p[0]
    return math.fsum((p[i][0]-x)*(p[(i+1)%len(p)][1]-y)-(p[i][1]-y)*(p[(i+1)%len(p)][0]-x) for i in range(len(p)))/2
def _ss_patch_hull(q):
    q=sorted(set(q))
    def half(a):
        z=[]
        for p in a:
            while len(z)>1 and _ss_patch_cross(z[-2],z[-1],p)<=0:z.pop()
            z.append(p)
        return z
    return half(q)[:-1]+half(q[::-1])[:-1] if len(q)>2 else q
def _ss_patch_split(p,a,b):
    inn=[];out=[]
    for i,u in enumerate(p):
        v=p[(i+1)%len(p)];cu=_ss_patch_cross(a,b,u);cv=_ss_patch_cross(a,b,v)
        if cu>=0:inn.append(u)
        if cu<=0:out.append(u)
        if (cu>0 and cv<0) or (cu<0 and cv>0):
            t=cu/(cu-cv);w=(u[0]+t*(v[0]-u[0]),u[1]+t*(v[1]-u[1]));inn.append(w);out.append(w)
    return inn,out
def _ss_patch_sub(piece,clip):
    inside=[piece];outside=[]
    for i,a in enumerate(clip):
        nxt=[];b=clip[(i+1)%len(clip)]
        for q in inside:
            inn,out=_ss_patch_split(q,a,b)
            if len(out)>=3 and _ss_patch_area(out)!=0:outside.append(out)
            if len(inn)>=3 and _ss_patch_area(inn)!=0:nxt.append(inn)
        inside=nxt
        if not inside:break
    return outside
def _ss_patch_cell_covered(polygon,triangles,tolerance):
    tolerance=float(tolerance)
    if not math.isfinite(tolerance) or tolerance<=0:return False
    remain=[[_ss_patch_xy(p) for p in polygon]]
    if len(remain[0])<3 or _ss_patch_area(remain[0])==0:return False
    for tri in triangles:
        if len(tri)!=3:raise ValueError("supporting triangle is not a triangle")
        v=[_ss_patch_xy(p) for p in tri]
        if _ss_patch_area(v)==0:continue
        q=list(v)
        for x,y in v:q.extend((x+tolerance*math.cos(2*math.pi*k/64),y+tolerance*math.sin(2*math.pi*k/64)) for k in range(64))
        clip=_ss_patch_hull(q)
        if len(clip)<3 or _ss_patch_area(clip)==0:continue
        remain=[z for r in remain for z in _ss_patch_sub(r,clip)]
        if not remain:return True
    return False
