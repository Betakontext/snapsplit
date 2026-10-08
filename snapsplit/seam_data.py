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

"""Store versioned Freehand seam metadata on result objects."""

# seam_data.py

import json
import math
import bpy
from uuid import uuid4

from mathutils import Vector


SCHEMA_VERSION = 1
OBJECT_ID_KEY = "snapsplit_seam_object_id"
DATA_KEY = "snapsplit_seam_data"


def _coordinates(vector):
    """Convert a vector to JSON-compatible coordinates."""
    return [float(component) for component in vector]


def read_seam_data(obj):
    """Read supported metadata without silently accepting another version."""
    raw = obj.get(DATA_KEY)

    if raw is None:
        return None

    if not isinstance(raw, str):
        raise ValueError(
            f"Invalid seam metadata on '{obj.name}': expected JSON text."
        )

    try:
        data = json.loads(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Cannot read seam metadata on '{obj.name}'."
        ) from exc

    if not isinstance(data, dict):
        raise ValueError(f"Invalid seam metadata on '{obj.name}'.")

    if data.get("version") != SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported seam metadata version on '{obj.name}'."
        )

    if (
        not isinstance(data.get("object_id"), str)
        or data["object_id"] != obj.get(OBJECT_ID_KEY)
        or not isinstance(data.get("seams"), list)
    ):
        raise ValueError(
            f"Inconsistent seam metadata on '{obj.name}'."
        )

    return data


def write_freehand_seams(
    objects,
    regions,
    plane_point,
    plane_normal,
    tangent,
    capped,
    tolerance,
):
    """Write reciprocal seam records on newly created result objects only."""
    if len(objects) < 2 or not regions:
        raise ValueError("No valid Freehand seam relationships were prepared.")

    normal_world = Vector(plane_normal).normalized()
    tangent_world = Vector(tangent).normalized()

    object_ids = [uuid4().hex for _obj in objects]
    documents = [
        {
            "version": SCHEMA_VERSION,
            "object_id": object_id,
            "seams": [],
        }
        for object_id in object_ids
    ]

    for region in regions:
        negative = region["negative_part"]
        positive = region["positive_part"]

        if (
            not 0 <= negative < len(objects)
            or not 0 <= positive < len(objects)
            or negative == positive
        ):
            raise ValueError("A seam has invalid result partners.")

        seam_id = uuid4().hex

        for own_index, partner_index, side in (
            (negative, positive, -1),
            (positive, negative, 1),
        ):
            obj = objects[own_index]
            matrix = obj.matrix_world
            inverse = matrix.inverted()

            # A world-space plane normal becomes local via M transposed.
            normal_local = (
                matrix.to_3x3().transposed() @ normal_world
            ).normalized()

            # A tangent is a direction, not a normal.
            tangent_local = (
                inverse.to_3x3() @ tangent_world
            ).normalized()

            def local_loop(points):
                return [
                    _coordinates(inverse @ Vector(point))
                    for point in points
                ]

            record = {
                "seam_id": seam_id,
                "kind": "FREEHAND",
                "partner_id": object_ids[partner_index],
                "side": side,
                "capped_at_creation": bool(capped),
                "plane_point_local": _coordinates(
                    inverse @ Vector(plane_point)
                ),
                "plane_normal_local": _coordinates(normal_local),
                "tangent_local": _coordinates(tangent_local),
                "outer_local": local_loop(region["outer"]),
                "holes_local": [
                    local_loop(hole)
                    for hole in region["holes"]
                ],
                "tolerance_world_at_creation": float(tolerance),
            }

            documents[own_index]["seams"].append(record)

    if any(not document["seams"] for document in documents):
        raise ValueError("A result object has no assigned Freehand seam.")

    # Serialize everything before modifying any object properties.
    serialized = [
        json.dumps(
            document,
            separators=(",", ":"),
            allow_nan=False,
        )
        for document in documents
    ]

    for obj, object_id, raw in zip(objects, object_ids, serialized):
        obj[OBJECT_ID_KEY] = object_id
        obj[DATA_KEY] = raw


def describe_seams(obj):
    """Return concise diagnostic lines without changing scene data."""
    data = read_seam_data(obj)

    if data is None:
        return [f"{obj.name}: no Freehand seam metadata"]

    lines = [
        f"{obj.name}: object_id={data['object_id']}, "
        f"seams={len(data['seams'])}"
    ]

    for record in data["seams"]:
        state = (
            "capped at creation"
            if record["capped_at_creation"]
            else "open at creation"
        )
        lines.append(
            f"  seam={record['seam_id']} "
            f"partner={record['partner_id']} "
            f"side={record['side']:+d} "
            f"holes={len(record['holes_local'])} "
            f"state={state}"
        )

    return lines

class SeamValidationError(ValueError):
    """Indicate invalid, unsupported, or ambiguous Freehand seam data."""


def has_freehand_metadata(obj):
    """Reserve objects carrying either new metadata key for this resolver."""
    return (
        obj is not None
        and (
            DATA_KEY in obj
            or OBJECT_ID_KEY in obj
        )
    )


def _checked_vector(value, label):
    """Read a finite three-dimensional vector from JSON data."""
    if (
        not isinstance(value, (list, tuple))
        or len(value) != 3
        or any(
            isinstance(component, bool)
            or not isinstance(component, (int, float))
            or not math.isfinite(component)
            for component in value
        )
    ):
        raise SeamValidationError(f"Invalid {label}.")

    return Vector(value)


def _checked_loop(value, label):
    """Read a polygon boundary without accepting degenerate loops."""
    if not isinstance(value, list) or len(value) < 3:
        raise SeamValidationError(f"Invalid {label}.")

    return [
        _checked_vector(point, label)
        for point in value
    ]


def _validated_document(obj):
    """Validate object identity and the complete local seam record list."""
    try:
        document = read_seam_data(obj)
    except ValueError as exc:
        raise SeamValidationError(str(exc)) from exc

    if document is None:
        raise SeamValidationError(
            f"Missing Freehand seam data on '{obj.name}'."
        )

    object_id = document["object_id"]
    if not object_id:
        raise SeamValidationError("An object ID is empty.")

    holders = [
        candidate
        for candidate in bpy.data.objects
        if candidate.get(OBJECT_ID_KEY) == object_id
    ]

    if len(holders) != 1 or holders[0] != obj:
        raise SeamValidationError(
            f"Duplicate or ambiguous seam object ID on '{obj.name}'."
        )

    records = document["seams"]
    if not records:
        raise SeamValidationError("The seam record list is empty.")

    seen = set()

    for record in records:
        if not isinstance(record, dict):
            raise SeamValidationError("A seam record is not a dictionary.")

        seam_id = record.get("seam_id")
        partner_id = record.get("partner_id")

        if (
            not isinstance(seam_id, str)
            or not seam_id
            or seam_id in seen
            or not isinstance(partner_id, str)
            or not partner_id
            or partner_id == object_id
            or record.get("kind") != "FREEHAND"
        ):
            raise SeamValidationError("Invalid seam identity or partner.")

        seen.add(seam_id)

        if (
            type(record.get("side")) is not int
            or record["side"] not in (-1, 1)
            or type(record.get("capped_at_creation")) is not bool
        ):
            raise SeamValidationError("Invalid seam side or cap status.")

        for key in (
            "plane_point_local",
            "plane_normal_local",
            "tangent_local",
        ):
            _checked_vector(record.get(key), key)

        _checked_loop(record.get("outer_local"), "outer contour")

        holes = record.get("holes_local")
        if not isinstance(holes, list):
            raise SeamValidationError("Invalid inner contour list.")

        for hole in holes:
            _checked_loop(hole, "inner contour")

        tolerance = record.get("tolerance_world_at_creation")
        if (
            isinstance(tolerance, bool)
            or not isinstance(tolerance, (int, float))
            or not math.isfinite(tolerance)
            or tolerance <= 0.0
        ):
            raise SeamValidationError("Invalid stored seam tolerance.")

    return document


def _world_record(obj, record):
    """Transform a seam frame and its boundaries into current world space."""
    if obj.type != 'MESH' or obj.data is None:
        raise SeamValidationError("Freehand partners must be mesh objects.")

    if obj.mode != 'OBJECT':
        raise SeamValidationError("Switch both partners to Object Mode.")

    if any(
        modifier.show_viewport or modifier.show_render
        for modifier in obj.modifiers
    ):
        raise SeamValidationError(
            f"Active modifiers are not supported on '{obj.name}' in C2."
        )

    matrix = obj.matrix_world
    linear = matrix.to_3x3()
    determinant = linear.determinant()

    if not math.isfinite(determinant) or determinant <= 1e-12:
        raise SeamValidationError(
            "Singular, mirrored, or extremely small transforms are unsupported."
        )

    if any(
        not math.isfinite(matrix[row][column])
        for row in range(4)
        for column in range(4)
    ):
        raise SeamValidationError("The object transform contains invalid values.")

    local_normal = _checked_vector(
        record["plane_normal_local"], "local normal"
    )
    local_tangent = _checked_vector(
        record["tangent_local"], "local tangent"
    )

    normal = linear.inverted().transposed() @ local_normal
    tangent = linear @ local_tangent

    if normal.length <= 1e-12:
        raise SeamValidationError("The seam normal is degenerate.")

    normal.normalize()
    tangent -= normal * tangent.dot(normal)

    if tangent.length <= 1e-12:
        raise SeamValidationError("The seam tangent is degenerate.")

    tangent.normalize()

    loops = [
        [
            matrix @ point
            for point in _checked_loop(
                record["outer_local"], "outer contour"
            )
        ]
    ]

    loops.extend(
        [
            matrix @ point
            for point in _checked_loop(hole, "inner contour")
        ]
        for hole in record["holes_local"]
    )

    return {
        "origin": matrix @ _checked_vector(
            record["plane_point_local"], "plane point"
        ),
        "normal": normal,
        "tangent": tangent,
        "loops": loops,
        "side": record["side"],
    }


def _loops_match(first, second, tolerance):
    """Compare polygon cycles independent of start vertex and traversal."""
    if len(first) != len(second):
        return False

    count = len(first)

    for start in range(count):
        for direction in (-1, 1):
            if all(
                (
                    first[index]
                    - second[(start + direction * index) % count]
                ).length <= tolerance
                for index in range(count)
            ):
                return True

    return False


def _boundaries_match(first, second, tolerance):
    """Compare an outer contour and an unordered list of inner contours."""
    if (
        len(first) != len(second)
        or not _loops_match(first[0], second[0], tolerance)
    ):
        return False

    remaining = list(second[1:])

    for hole in first[1:]:
        match = next(
            (
                index
                for index, candidate in enumerate(remaining)
                if _loops_match(hole, candidate, tolerance)
            ),
            None,
        )

        if match is None:
            return False

        remaining.pop(match)

    return not remaining


def _loop_area(loop, origin, x_axis, y_axis):
    """Measure an unsigned polygon area in the seam plane."""
    points = [
        (
            (point - origin).dot(x_axis),
            (point - origin).dot(y_axis),
        )
        for point in loop
    ]

    return abs(
        0.5 * sum(
            points[index][0] * points[(index + 1) % len(points)][1]
            - points[(index + 1) % len(points)][0] * points[index][1]
            for index in range(len(points))
        )
    )


def _verify_current_cap(obj, frame, tolerance):
    """Verify a current planar cap island against its stored boundary edges."""
    mesh = obj.data
    matrix = obj.matrix_world
    vertices = [
        matrix @ vertex.co
        for vertex in mesh.vertices
    ]

    if any(
        not math.isfinite(component)
        for point in vertices
        for component in point
    ):
        raise SeamValidationError("The current mesh contains invalid vertices.")

    origin = frame["origin"]
    normal = frame["normal"]
    edge_faces = {}

    for face in mesh.polygons:
        for edge in face.edge_keys:
            key = tuple(sorted(edge))
            edge_faces.setdefault(key, []).append(face.index)

    # Require a closed edge-manifold surface, including any cavity walls.
    if (
        any(
            len(edge_faces.get(tuple(sorted(edge.vertices)), ())) != 2
            for edge in mesh.edges
        )
        or any(len(faces) != 2 for faces in edge_faces.values())
    ):
        raise SeamValidationError(
            f"'{obj.name}' is open or contains non-manifold edges."
        )

    planar = {
        face.index
        for face in mesh.polygons
        if all(
            abs((vertices[index] - origin).dot(normal)) <= tolerance
            for index in face.vertices
        )
    }

    expected_edges = [
        (loop[index], loop[(index + 1) % len(loop)])
        for loop in frame["loops"]
        for index in range(len(loop))
    ]

    def matches_edge(key, expected):
        a, b = (vertices[index] for index in key)
        c, d = expected
        return (
            (a - c).length <= tolerance
            and (b - d).length <= tolerance
        ) or (
            (a - d).length <= tolerance
            and (b - c).length <= tolerance
        )

    seed_faces = {
        face_index
        for key, linked in edge_faces.items()
        if matches_edge(key, expected_edges[0])
        for face_index in linked
        if face_index in planar
    }

    if len(seed_faces) != 1:
        raise SeamValidationError(
            "The stored contour does not identify a unique current cap."
        )

    adjacency = {index: set() for index in planar}

    for linked in edge_faces.values():
        if linked[0] in planar and linked[1] in planar:
            adjacency[linked[0]].add(linked[1])
            adjacency[linked[1]].add(linked[0])

    island = set()
    pending = list(seed_faces)

    while pending:
        index = pending.pop()
        if index in island:
            continue
        island.add(index)
        pending.extend(adjacency[index] - island)

    boundary = [
        key
        for key, linked in edge_faces.items()
        if sum(index in island for index in linked) == 1
    ]

    if len(boundary) != len(expected_edges):
        raise SeamValidationError(
            "The current cap boundary differs from the stored contours."
        )

    remaining = list(boundary)

    for expected in expected_edges:
        matches = [
            index
            for index, key in enumerate(remaining)
            if matches_edge(key, expected)
        ]

        if len(matches) != 1:
            raise SeamValidationError(
                "A stored contour edge is missing or ambiguous."
            )

        remaining.pop(matches[0])

    # Positive-side parts have outward cap normals pointing to the negative side.
    expected_normal = normal * -frame["side"]
    area = 0.0

    for index in island:
        face = mesh.polygons[index]
        points = [vertices[item] for item in face.vertices]
        reference = points[0]
        area_vector = Vector((0.0, 0.0, 0.0))

        for item in range(1, len(points) - 1):
            area_vector += (
                (points[item] - reference).cross(
                    points[item + 1] - reference
                ) * 0.5
            )

        if (
            area_vector.length <= tolerance * tolerance
            or area_vector.normalized().dot(expected_normal) < 1.0 - 1e-5
        ):
            raise SeamValidationError(
                "A cap face is degenerate or has an inconsistent orientation."
            )

        area += area_vector.length

    x_axis = frame["tangent"]
    y_axis = normal.cross(x_axis).normalized()
    expected_area = (
        _loop_area(frame["loops"][0], origin, x_axis, y_axis)
        - sum(
            _loop_area(hole, origin, x_axis, y_axis)
            for hole in frame["loops"][1:]
        )
    )

    if (
        expected_area <= tolerance * tolerance
        or abs(area - expected_area)
        > max(expected_area * 1e-5, tolerance * tolerance * 32.0)
    ):
        raise SeamValidationError(
            "The current cap area differs from the stored material region."
        )


def resolve_freehand_plane(obj_p, obj_q):
    """Resolve a validated Freehand seam without enabling connector placement.

    Return (socket, pin, origin, normal, tangent), or None when neither object
    has Freehand metadata or when two valid documents have no shared seam.
    Raise SeamValidationError for invalid or unsupported relationships.
    """
    if not (
        has_freehand_metadata(obj_p)
        or has_freehand_metadata(obj_q)
    ):
        return None

    if obj_p == obj_q:
        raise SeamValidationError("Select two different seam partners.")

    if not (
        has_freehand_metadata(obj_p)
        and has_freehand_metadata(obj_q)
    ):
        raise SeamValidationError(
            "Only one selected object has Freehand seam metadata."
        )

    p_data = _validated_document(obj_p)
    q_data = _validated_document(obj_q)

    p_records = [
        record
        for record in p_data["seams"]
        if record["partner_id"] == q_data["object_id"]
    ]
    q_records = [
        record
        for record in q_data["seams"]
        if record["partner_id"] == p_data["object_id"]
    ]

    if not p_records and not q_records:
        return None

    if (
        len(p_records) != 1
        or len(q_records) != 1
        or p_records[0]["seam_id"] != q_records[0]["seam_id"]
    ):
        raise SeamValidationError(
            "The partner relationship is missing, asymmetric, or ambiguous."
        )

    p_record, q_record = p_records[0], q_records[0]

    if p_record["side"] != -q_record["side"]:
        raise SeamValidationError("The seam sides are not opposite.")

    if not (
        p_record["capped_at_creation"]
        and q_record["capped_at_creation"]
    ):
        raise SeamValidationError(
            "Open Freehand seams are not supported for connectors in C2."
        )

    p_frame = _world_record(obj_p, p_record)
    q_frame = _world_record(obj_q, q_record)

    span = max(
        (point - p_frame["loops"][0][0]).length
        for loop in p_frame["loops"]
        for point in loop
    )

    # Derive tolerance from current world dimensions, not stale creation scale.
    tolerance = max(1e-7, span * 1e-6)

    if (
        p_frame["normal"].dot(q_frame["normal"]) < 1.0 - 1e-6
        or p_frame["tangent"].dot(q_frame["tangent"]) < 1.0 - 1e-6
        or (p_frame["origin"] - q_frame["origin"]).length > tolerance
        or not _boundaries_match(
            p_frame["loops"], q_frame["loops"], tolerance
        )
    ):
        raise SeamValidationError(
            "The two seam frames or contours no longer coincide."
        )

    for frame in (p_frame, q_frame):
        if any(
            abs((point - frame["origin"]).dot(frame["normal"])) > tolerance
            for loop in frame["loops"]
            for point in loop
        ):
            raise SeamValidationError("A stored contour is not planar.")

    _verify_current_cap(obj_p, p_frame, tolerance)
    _verify_current_cap(obj_q, q_frame, tolerance)

    if p_frame["side"] == 1:
        socket, pin = obj_p, obj_q
    else:
        socket, pin = obj_q, obj_p

    return (
        socket,
        pin,
        p_frame["origin"],
        p_frame["normal"],
        p_frame["tangent"],
    )

