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
    """Transfer intact old seams and return a metadata rollback callback.

    Newly created seam documents must already exist on all result objects.
    Intersected, open, or modified old seams are deliberately rejected.
    No mesh geometry is modified by this function.
    """
    if ARCHIVE_KEY in source:
        raise SeamValidationError(
            "This object is an archived cut source. "
            "Use an active Freehand result or restore the earlier operation."
        )

    if DATA_KEY not in source and OBJECT_ID_KEY not in source:
        return lambda: None

    source_document = _validated_document(source)
    source_id = source_document["object_id"]

    result_documents = []

    for obj in results:
        document = read_seam_data(obj)

        if document is None:
            raise SeamValidationError(
                "A new result is missing its newly created seam metadata."
            )

        result_documents.append(copy.deepcopy(document))

    # Partner changes are accumulated in detached documents first.
    partners = {}
    planned_transfers = []

    for old_record in source_document["seams"]:
        if not old_record["capped_at_creation"]:
            raise SeamValidationError(
                "Migration of existing open seams is not implemented. "
                "No result or partner metadata was changed."
            )

        partner_id = old_record["partner_id"]

        if partner_id not in partners:
            partner = _find_partner(partner_id)
            document = copy.deepcopy(_validated_document(partner))
            partners[partner_id] = (partner, document)

        partner, partner_document = partners[partner_id]
        reciprocal = _counterpart(
            partner_document,
            source_id,
            old_record["seam_id"],
        )

        if (
            reciprocal["side"] != -old_record["side"]
            or not reciprocal["capped_at_creation"]
        ):
            raise SeamValidationError(
                "An existing seam has inconsistent sides or cap states."
            )

        frame = _world_record(source, old_record)
        tolerance = _frame_tolerance(frame)

        # Reject already altered old caps before attempting ownership transfer.
        _verify_current_cap(source, frame, tolerance)

        owners = []
        rejected_results = []

        for index, obj in enumerate(results):
            try:
                _verify_current_cap(obj, frame, tolerance)
            except SeamValidationError as exc:
                rejected_results.append(
                    f"'{obj.name}': {exc}"
                )
            else:
                owners.append(index)

        if len(owners) != 1:
            seam_id = old_record["seam_id"]

            if owners:
                owner_names = ", ".join(
                    f"'{results[index].name}'"
                    for index in owners
                )
                summary = (
                    "The existing seam matches more than one result: "
                    f"{owner_names}."
                )
            else:
                summary = (
                    "No result contains a complete cap matching the "
                    "existing strict contour validation."
                )

            details = "\n".join(
                f"  - {message}"
                for message in rejected_results
            )

            diagnostic = (
                "[SnapSplit] Existing seam migration rejected\n"
                f"Source: '{source.name}'\n"
                f"Seam ID: {seam_id}\n"
                f"Partner: '{partner.name}'\n"
                f"World tolerance: {tolerance:.9g}\n"
                f"{summary}"
            )

            if details:
                diagnostic += "\nRejected results:\n" + details

            # Keep full per-result diagnostics available in Blender's console.
            print(diagnostic)

            raise SeamValidationError(
                f"Existing seam '{seam_id}' on '{source.name}' "
                f"could not be migrated. {summary} "
                "This can indicate changed edge subdivision, a split "
                "contact region, or invalid result geometry. "
                "See the system console for individual validation errors. "
                "Contact-region splitting is not implemented in this version."
            )


        owner_index = owners[0]
        owner = results[owner_index]
        owner_document = result_documents[owner_index]

        if any(
            record["seam_id"] == old_record["seam_id"]
            for record in owner_document["seams"]
        ):
            raise SeamValidationError(
                "The migrated seam ID already exists on its new owner."
            )

        migrated = _record_for_object(old_record, frame, owner)
        owner_document["seams"].append(migrated)

        # Keep the seam ID and external partner ID; replace only its owner.
        reciprocal["partner_id"] = owner_document["object_id"]

        planned_transfers.append({
            "seam_id": old_record["seam_id"],
            "new_owner_id": owner_document["object_id"],
        })

    # Serialize every payload before touching existing objects.
    changes = [
        (obj, _encode(document))
        for obj, document in zip(results, result_documents)
    ]
    changes.extend(
        (obj, _encode(document))
        for obj, document in partners.values()
    )

    archive = _encode({
        "version": 1,
        "state": "REPLACED_BY_FREEHAND_RESULTS",
        "previous_document": source_document,
        "transfers": planned_transfers,
    })

    touched = [source, *results]
    touched.extend(obj for obj, _document in partners.values())

    snapshots = []
    seen = set()

    for obj in touched:
        pointer = obj.as_pointer()

        if pointer not in seen:
            snapshots.append(_snapshot(obj))
            seen.add(pointer)

    def rollback():
        """Restore source, result, and external partner metadata."""
        for snapshot in reversed(snapshots):
            _restore(snapshot)

    try:
        for obj, payload in changes:
            obj[DATA_KEY] = payload

        # Preserve history without retaining an active identity or relationship.
        source[ARCHIVE_KEY] = archive
        del source[DATA_KEY]
        del source[OBJECT_ID_KEY]

    except Exception:
        rollback()
        raise

    return rollback


