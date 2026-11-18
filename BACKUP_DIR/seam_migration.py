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

# seam_migration.py
"""Migrate intact Freehand seams when a result object is cut again."""

import copy
import json

import bpy

from .seam_data import (
    DATA_KEY,
    OBJECT_ID_KEY,
    SeamValidationError,
    _validated_document,
    _verify_current_cap,
    _world_record,
    read_seam_data,
)


ARCHIVE_KEY = "snapsplit_seam_archive"


def _encode(document):
    """Serialize metadata before committing any property changes."""
    return json.dumps(
        document,
        separators=(",", ":"),
        allow_nan=False,
    )


def _snapshot(obj):
    """Capture only properties owned by this migration."""
    return (
        obj,
        {
            key: obj[key] if key in obj else None
            for key in (DATA_KEY, OBJECT_ID_KEY, ARCHIVE_KEY)
        },
    )


def _restore(snapshot):
    """Restore a previously captured metadata state."""
    obj, values = snapshot

    for key, value in values.items():
        if value is None:
            if key in obj:
                del obj[key]
        else:
            obj[key] = value


def _find_partner(object_id):
    """Resolve an active object ID without depending on object names."""
    matches = [
        obj
        for obj in bpy.data.objects
        if obj.get(OBJECT_ID_KEY) == object_id
    ]

    if len(matches) != 1:
        raise SeamValidationError(
            "An existing seam partner is missing or has a duplicate object ID."
        )

    return matches[0]


def _counterpart(document, source_id, seam_id):
    """Find exactly one reciprocal record in a partner document."""
    matches = [
        record
        for record in document["seams"]
        if record["partner_id"] == source_id
        and record["seam_id"] == seam_id
    ]

    if len(matches) != 1:
        raise SeamValidationError(
            "An existing seam has a missing or ambiguous reciprocal record."
        )

    return matches[0]


def _frame_tolerance(frame):
    """Use the same current-world scale convention as the C2 resolver."""
    reference = frame["loops"][0][0]
    span = max(
        (point - reference).length
        for loop in frame["loops"]
        for point in loop
    )
    return max(1e-7, span * 1e-6)


def _record_for_object(record, frame, obj):
    """Rebase an existing world-space seam onto its new owner."""
    result = copy.deepcopy(record)
    matrix = obj.matrix_world
    inverse = matrix.inverted()

    normal_local = (
        matrix.to_3x3().transposed() @ frame["normal"]
    ).normalized()

    tangent_local = (
        inverse.to_3x3() @ frame["tangent"]
    ).normalized()

    def coordinates(vector):
        return [float(component) for component in vector]

    def local_loop(loop):
        return [
            coordinates(inverse @ point)
            for point in loop
        ]

    result["plane_point_local"] = coordinates(
        inverse @ frame["origin"]
    )
    result["plane_normal_local"] = coordinates(normal_local)
    result["tangent_local"] = coordinates(tangent_local)
    result["outer_local"] = local_loop(frame["loops"][0])
    result["holes_local"] = [
        local_loop(loop)
        for loop in frame["loops"][1:]
    ]

    return result


def migrate_intact_freehand_seams(source, results):
    """Transfer intact contacts without blocking cuts on modified old caps.

    Modified, divided, or ambiguous old relationships are removed from
    active seam documents and preserved in contact history.

    Existing connector mesh geometry is never modified here.
    Return a callback restoring all metadata changed by this function.
    """
    history_key = "snapsplit_contact_history"
    property_keys = (
        DATA_KEY,
        OBJECT_ID_KEY,
        ARCHIVE_KEY,
        history_key,
    )

    if ARCHIVE_KEY in source:
        raise SeamValidationError(
            "This object is an archived cut source."
        )

    if DATA_KEY not in source and OBJECT_ID_KEY not in source:
        return lambda: None

    results = list(results)
    source_pointer = source.as_pointer()
    result_pointers = [obj.as_pointer() for obj in results]

    if (
        len(results) < 2
        or len(set(result_pointers)) != len(results)
        or source_pointer in result_pointers
    ):
        raise SeamValidationError(
            "Migration requires at least two distinct new result objects."
        )

    source_document = copy.deepcopy(_validated_document(source))
    source_id = source_document["object_id"]

    result_documents = []
    for obj in results:
        if ARCHIVE_KEY in obj:
            raise SeamValidationError(
                "A new result unexpectedly contains archived metadata."
            )
        result_documents.append(
            copy.deepcopy(_validated_document(obj))
        )

    partners = {}
    events = []
    event_targets = []

    def matrix_values(obj):
        """Store the current placement independently of object names."""
        return [
            [
                float(obj.matrix_world[row][column])
                for column in range(4)
            ]
            for row in range(4)
        ]

    def read_history(obj):
        """Preserve previous history instead of silently overwriting it."""
        if history_key not in obj:
            return []

        raw = obj[history_key]
        if not isinstance(raw, str):
            raise SeamValidationError(
                f"Contact history on '{obj.name}' is not JSON text."
            )

        try:
            value = json.loads(raw)
        except (TypeError, ValueError) as exc:
            raise SeamValidationError(
                f"Contact history on '{obj.name}' is invalid."
            ) from exc

        if not isinstance(value, list):
            raise SeamValidationError(
                f"Contact history on '{obj.name}' is not a list."
            )

        return value

    for old_record in source_document["seams"]:
        seam_id = old_record["seam_id"]
        partner_id = old_record["partner_id"]

        if partner_id not in partners:
            partner = _find_partner(partner_id)
            pointer = partner.as_pointer()

            if (
                pointer == source_pointer
                or pointer in result_pointers
                or ARCHIVE_KEY in partner
            ):
                raise SeamValidationError(
                    "An existing contact has an invalid external partner."
                )

            partners[partner_id] = (
                partner,
                copy.deepcopy(_validated_document(partner)),
            )

        partner, partner_document = partners[partner_id]
        reciprocal = _counterpart(
            partner_document,
            source_id,
            seam_id,
        )

        if reciprocal["side"] != -old_record["side"]:
            raise SeamValidationError(
                "An existing contact has inconsistent reciprocal sides."
            )

        # Preserve both original records before editing their relationship.
        event = {
            "previous_seam_id": seam_id,
            "source_id": source_id,
            "partner_id": partner_id,
            "source_record": copy.deepcopy(old_record),
            "partner_record": copy.deepcopy(reciprocal),
            "source_matrix_world": matrix_values(source),
            "partner_matrix_world": matrix_values(partner),
        }

        owners = []

        if old_record["capped_at_creation"]:
            # Local metadata follows the source's current placement.
            # The external partner need not currently coincide with it.
            frame = _world_record(source, old_record)
            tolerance = _frame_tolerance(frame)

            for index, obj in enumerate(results):
                try:
                    _verify_current_cap(obj, frame, tolerance)
                except SeamValidationError:
                    # A changed old cap must not block a new mesh cut.
                    continue
                owners.append(index)

        if len(owners) == 1:
            owner_index = owners[0]
            owner = results[owner_index]
            owner_document = result_documents[owner_index]

            if any(
                record["seam_id"] == seam_id
                for record in owner_document["seams"]
            ):
                raise SeamValidationError(
                    "A migrated seam ID already exists on its new owner."
                )

            migrated = _record_for_object(
                old_record,
                frame,
                owner,
            )
            migrated["side"] = old_record["side"]
            migrated["partner_id"] = partner_id
            owner_document["seams"].append(migrated)

            # Keep the partner's own local geometry and placement unchanged.
            reciprocal["partner_id"] = owner_document["object_id"]

            event["action"] = "TRANSFERRED"
            event["new_owner_id"] = owner_document["object_id"]
            targets = [source, partner, owner]

        else:
            # Do not retain an active link to an archived source.
            # The complete old relationship survives in the history.
            partner_document["seams"].remove(reciprocal)

            event["action"] = "RETIRED"
            event["reason"] = (
                "The old contact was open, modified, divided, or "
                "could not be assigned to one intact result cap."
            )
            targets = [source, partner, *results]

        events.append(event)
        event_targets.append(targets)

    touched = {}
    for obj in [
        source,
        *results,
        *(obj for obj, _document in partners.values()),
    ]:
        touched[obj.as_pointer()] = obj

    histories = {
        pointer: read_history(obj)
        for pointer, obj in touched.items()
    }

    for event, targets in zip(events, event_targets):
        seen = set()
        for obj in targets:
            pointer = obj.as_pointer()
            if pointer not in seen:
                histories[pointer].append(copy.deepcopy(event))
                seen.add(pointer)

    # Prepare all payloads before changing any existing properties.
    writes = []

    for obj, document in zip(results, result_documents):
        writes.append((obj, DATA_KEY, _encode(document)))

    for partner, document in partners.values():
        if document["seams"]:
            writes.append((partner, DATA_KEY, _encode(document)))
        else:
            # An empty active document would fail the existing validator.
            # History alone must not mark the partner as archived.
            writes.append((partner, DATA_KEY, None))
            writes.append((partner, OBJECT_ID_KEY, None))

    for pointer, obj in touched.items():
        writes.append((
            obj,
            history_key,
            _encode(histories[pointer]),
        ))

    archive = {
        "version": 1,
        "state": "REPLACED_BY_FREEHAND_RESULTS",
        "previous_document": source_document,
        "transfers": events,
    }

    writes.extend([
        (source, ARCHIVE_KEY, _encode(archive)),
        (source, DATA_KEY, None),
        (source, OBJECT_ID_KEY, None),
    ])

    snapshots = [
        (
            obj,
            {
                key: (
                    key in obj,
                    copy.deepcopy(obj[key]) if key in obj else None,
                )
                for key in property_keys
            },
        )
        for obj in touched.values()
    ]

    def rollback():
        """Restore every touched property, attempting all restorations."""
        failures = []

        for obj, values in reversed(snapshots):
            for key, (existed, value) in values.items():
                try:
                    if existed:
                        obj[key] = copy.deepcopy(value)
                    elif key in obj:
                        del obj[key]
                except Exception as exc:
                    failures.append(f"{key}: {exc}")

        if failures:
            raise RuntimeError(
                "Contact metadata rollback failed: "
                + "; ".join(failures)
            )

    try:
        for obj, key, value in writes:
            if value is None:
                if key in obj:
                    del obj[key]
            else:
                obj[key] = value

        for obj in results:
            _validated_document(obj)

        for partner, document in partners.values():
            if document["seams"]:
                _validated_document(partner)

    except Exception as exc:
        try:
            rollback()
        except Exception as rollback_exc:
            raise RuntimeError(
                f"Contact migration failed: {exc}. "
                f"Rollback also failed: {rollback_exc}"
            ) from exc
        raise

    return rollback



