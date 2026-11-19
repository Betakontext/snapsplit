# -*- coding: utf-8 -*-
"""
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
"""

# contact_geometry.py

"""Resolve current planar mesh contacts independently of seam metadata."""

from mathutils import Vector
import bpy


def _area2(polygon):
    """Return signed twice-area using a translated coordinate frame."""
    if len(polygon) < 3:
        return 0.0

    origin = polygon[0]
    return sum(
        (a - origin).cross(b - origin)
        for a, b in zip(polygon, polygon[1:] + polygon[:1])
    )


def _clip_triangle(subject, triangle):
    """Intersect a convex polygon with a CCW triangle."""
    polygon = list(subject)

    for a, b in zip(triangle, triangle[1:] + triangle[:1]):
        if not polygon:
            break

        edge = b - a
        output = []

        for first, second in zip(
            polygon, polygon[1:] + polygon[:1]
        ):
            distance_first = edge.cross(first - a)
            distance_second = edge.cross(second - a)

            first_inside = distance_first >= 0.0
            second_inside = distance_second >= 0.0

            if first_inside:
                output.append(first)

            if first_inside != second_inside:
                denominator = distance_first - distance_second
                if denominator != 0.0:
                    parameter = distance_first / denominator
                    output.append(
                        first + (second - first) * parameter
                    )

        polygon = output

    return polygon


def _bounds(points):
    """Return a world-space axis-aligned bounding box."""
    return (
        tuple(min(point[i] for point in points) for i in range(3)),
        tuple(max(point[i] for point in points) for i in range(3)),
    )


def _boxes_overlap(first, second, tolerance):
    """Reject triangle pairs whose expanded boxes cannot touch."""
    return all(
        first[0][i] <= second[1][i] + tolerance
        and second[0][i] <= first[1][i] + tolerance
        for i in range(3)
    )


def _world_triangles(obj, depsgraph):
    """Copy evaluated triangles and release Blender's temporary mesh."""
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()

    try:
        if mesh is None:
            return []

        mesh.calc_loop_triangles()
        matrix = evaluated.matrix_world.copy()
        coordinates = [
            matrix @ vertex.co
            for vertex in mesh.vertices
        ]
        triangles = []

        for loop_triangle in mesh.loop_triangles:
            points = [
                coordinates[index].copy()
                for index in loop_triangle.vertices
            ]

            # Geometric world normals include reflections and scaling.
            normal = (points[1] - points[0]).cross(
                points[2] - points[0]
            )
            if normal.length_squared == 0.0:
                continue

            normal.normalize()
            triangles.append((points, normal, _bounds(points)))

        return triangles

    finally:
        evaluated.to_mesh_clear()


def _project_triangle(points, origin, tangent, bitangent):
    """Project a world triangle and normalize its winding."""
    polygon = [
        Vector((
            (point - origin).dot(tangent),
            (point - origin).dot(bitangent),
        ))
        for point in points
    ]

    if _area2(polygon) < 0.0:
        polygon.reverse()

    return polygon


def resolve_current_contact(obj_p, obj_q, tolerance):
    """Return a connector pair tuple for one dominant planar contact.

    Return None when no positive-area planar contact can be established.
    Do not infer contact from object names, history, or bounding boxes alone.
    """
    if (
        obj_p is None
        or obj_q is None
        or obj_p == obj_q
        or obj_p.type != 'MESH'
        or obj_q.type != 'MESH'
    ):
        return None

    tolerance = float(tolerance)
    if tolerance <= 0.0:
        raise ValueError("Contact tolerance must be positive.")

    depsgraph = bpy.context.evaluated_depsgraph_get()
    first_triangles = _world_triangles(obj_p, depsgraph)
    second_triangles = _world_triangles(obj_q, depsgraph)

    if not first_triangles or not second_triangles:
        return None

    groups = []
    angular_tolerance = 1e-6
    minimum_area = tolerance * tolerance

    for first, first_normal, first_box in first_triangles:
        origin = first[0]

        # Choose the longest edge for a stable projection frame.
        tangent = max(
            (
                first[1] - first[0],
                first[2] - first[1],
                first[0] - first[2],
            ),
            key=lambda edge: edge.length_squared,
        ).normalized()
        bitangent = first_normal.cross(tangent).normalized()

        first_2d = _project_triangle(
            first, origin, tangent, bitangent
        )

        for second, second_normal, second_box in second_triangles:
            if first_normal.dot(second_normal) > (
                -1.0 + angular_tolerance
            ):
                continue

            if not _boxes_overlap(
                first_box, second_box, tolerance
            ):
                continue

            # Check both planes to avoid accepting tilted near-intersections.
            if any(
                abs((point - origin).dot(first_normal)) > tolerance
                for point in second
            ):
                continue

            if any(
                abs((point - second[0]).dot(second_normal)) > tolerance
                for point in first
            ):
                continue

            second_2d = _project_triangle(
                second, origin, tangent, bitangent
            )
            intersection = _clip_triangle(first_2d, second_2d)
            area = abs(_area2(intersection)) * 0.5

            if area <= minimum_area:
                continue

            # A convex intersection's vertex average lies inside it.
            center_2d = sum(intersection, Vector((0.0, 0.0)))
            center_2d /= len(intersection)
            center = (
                origin
                + tangent * center_2d.x
                + bitangent * center_2d.y
            )

            group = next(
                (
                    candidate
                    for candidate in groups
                    if (
                        candidate["normal"].dot(first_normal)
                        >= 1.0 - angular_tolerance
                        and abs(
                            (origin - candidate["origin"]).dot(
                                candidate["normal"]
                            )
                        ) <= tolerance
                    )
                ),
                None,
            )

            if group is None:
                group = {
                    "origin": origin.copy(),
                    "normal": first_normal.copy(),
                    "area": 0.0,
                    "largest_area": 0.0,
                    "center": center.copy(),
                    "tangent": tangent.copy(),
                }
                groups.append(group)

            group["area"] += area

            if area > group["largest_area"]:
                group["largest_area"] = area
                group["center"] = center.copy()
                group["tangent"] = tangent.copy()

    if not groups:
        return None

    group = max(groups, key=lambda candidate: candidate["area"])
    normal = group["normal"].copy()
    tangent = group["tangent"].copy()

    # P's outward normal points from P's material toward Q's material.
    pin = obj_p
    socket = obj_q

    # Keep role assignment stable relative to the dominant world axis.
    dominant_index = max(range(3), key=lambda i: abs(normal[i]))
    if normal[dominant_index] < 0.0:
        normal.negate()
        pin, socket = socket, pin

    tangent -= normal * tangent.dot(normal)
    tangent.normalize()

    center = group["center"]
    axis = ("X", "Y", "Z")[dominant_index]

    return (
        socket,
        pin,
        axis,
        float(center[dominant_index]),
        1,
        (center, normal, tangent),
    )
