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

# seam_migration

"""Migrate existing Freehand contacts onto newly created result objects.

New result seam documents must exist before migration starts.
Geometry ownership and contact splitting are delegated to seam_regions.
No mesh geometry is modified by this module.
"""

import copy
import json
from uuid import uuid4

import bpy

from .seam_data import (
    DATA_KEY,
    OBJECT_ID_KEY,
    SeamValidationError,
    _boundaries_match,
    _validated_document,
    _verify_current_cap,
    _world_record,
)
from .seam_regions import frame_tolerance, overlay_region


ARCHIVE_KEY = "snapsplit_seam_archive"

def _checked_contact_step(label, callback, *args):
    """Attach migration context to geometry validation errors."""
    try:
        return callback(*args)
    except ValueError as exc:
        raise SeamValidationError(f"{label}: {exc}") from exc


def _encode(document):
    """Serialize a detached document before changing object properties."""
    return json.dumps(
        document,
        separators=(",", ":"),
        allow_nan=False,
    )


def _snapshot(obj):
    """Capture property presence separately from stored property values."""
    return (
        obj,
        {
            key: (key in obj, obj[key] if key in obj else None)
            for key in (DATA_KEY, OBJECT_ID_KEY, ARCHIVE_KEY)
        },
    )


def _restore(snapshot):
    """Restore the exact presence and value of migration-owned properties."""
    obj, values = snapshot

    for key, (existed, value) in values.items():
        if existed:
            obj[key] = value
        elif key in obj:
            del obj[key]


def _find_partner(object_id):
    """Resolve a unique active seam identity without relying on names."""
    matches = [
        obj
        for obj in bpy.data.objects
        if obj.get(OBJECT_ID_KEY) == object_id
    ]

    if len(matches) != 1:
        raise SeamValidationError(
            "An existing seam partner is missing or has a duplicate object ID."
        )

    partner = matches[0]

    if ARCHIVE_KEY in partner:
        raise SeamValidationError(
            "An existing seam points to an archived Freehand source."
        )

    return partner


def _counterpart(document, source_id, seam_id):
    """Find exactly one reciprocal entry in a detached partner document."""
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
    """Keep the historical helper while using the shared region convention."""
    return frame_tolerance(frame)


def _record_for_object(record, frame, obj):
    """Rebase a world-space contact region onto its new local owner."""
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
        """Convert a vector to JSON-compatible floating-point coordinates."""
        return [float(component) for component in vector]

    def local_loop(loop):
        """Transform one complete world contour into object-local space."""
        return [
            coordinates(inverse @ point)
            for point in loop
        ]

    result["side"] = frame["side"]
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
    """Transfer intact or split contacts in one metadata transaction.

    Newly created seam documents must already exist on all result objects.
    Existing contacts and all new result contacts must be capped.

    Return a callback that restores every metadata property changed here.
    A source without active seam metadata requires no migration.
    """
    if ARCHIVE_KEY in source:
        raise SeamValidationError(
            "This object is an archived Freehand source."
        )

    if DATA_KEY not in source and OBJECT_ID_KEY not in source:
        return lambda: None

    results = list(results)

    if len(results) < 2:
        raise SeamValidationError(
            "Freehand seam migration requires at least two result objects."
        )

    result_pointers = [obj.as_pointer() for obj in results]

    if (
        len(set(result_pointers)) != len(result_pointers)
        or source.as_pointer() in result_pointers
    ):
        raise SeamValidationError(
            "Migration requires distinct result objects separate from the source."
        )

    source_document = _validated_document(source)
    source_id = source_document["object_id"]

    result_documents = []

    for obj in results:
        if ARCHIVE_KEY in obj:
            raise SeamValidationError(
                "A new result unexpectedly contains archived seam metadata."
            )

        document = copy.deepcopy(_validated_document(obj))

        if any(
            not record["capped_at_creation"]
            for record in document["seams"]
        ):
            raise SeamValidationError(
                "Migrating existing contacts requires capped new results."
            )

        result_documents.append(document)

    result_ids = {
        document["object_id"]
        for document in result_documents
    }

    # Keep all edits detached until every old contact has been validated.
    partners = {}
    transfers = []

    used_seam_ids = {
        record["seam_id"]
        for document in [source_document, *result_documents]
        for record in document["seams"]
    }

    def fresh_seam_id():
        """Allocate an identity not already present in this transaction."""
        while True:
            candidate = uuid4().hex
            if candidate not in used_seam_ids:
                used_seam_ids.add(candidate)
                return candidate

    for old_record in source_document["seams"]:
        if not old_record["capped_at_creation"]:
            raise SeamValidationError(
                "Existing open contacts cannot be migrated as closed regions."
            )

        partner_id = old_record["partner_id"]

        if partner_id in result_ids:
            raise SeamValidationError(
                "An existing external partner unexpectedly refers to a new result."
            )

        if partner_id not in partners:
            partner = _find_partner(partner_id)
            partner_document = copy.deepcopy(
                _validated_document(partner)
            )
            partners[partner_id] = (partner, partner_document)

            used_seam_ids.update(
                record["seam_id"]
                for record in partner_document["seams"]
            )

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
                "An old contact has inconsistent reciprocal metadata."
            )

        frame = _world_record(source, old_record)
        partner_frame = _world_record(partner, reciprocal)

        tolerance = max(
            _frame_tolerance(frame),
            _frame_tolerance(partner_frame),
        )

        if (
            frame["normal"].dot(partner_frame["normal"]) < 1.0 - 1e-6
            or frame["tangent"].dot(partner_frame["tangent"]) < 1.0 - 1e-6
            or (frame["origin"] - partner_frame["origin"]).length > tolerance
            or not _boundaries_match(
                frame["loops"],
                partner_frame["loops"],
                tolerance,
            )
        ):
            raise SeamValidationError(
                "An old contact and its external partner no longer coincide."
            )

        seam_id = old_record["seam_id"]

        # Validate each existing contact with an explicit owner context.
        _checked_contact_step(
            f"Existing source contact "
            f"[object={source.name!r}, seam={seam_id}]",
            _verify_current_cap,
            source,
            frame,
            tolerance,
        )

        _checked_contact_step(
            f"Existing partner contact "
            f"[object={partner.name!r}, seam={seam_id}]",
            _verify_current_cap,
            partner,
            partner_frame,
            tolerance,
        )

        # Resolve new owners only after both existing surfaces are valid.
        regions_by_result = list(
            _checked_contact_step(
                f"New result ownership "
                f"[source={source.name!r}, seam={seam_id}]",
                overlay_region,
                frame,
                results,
                tolerance,
            )
        )


        if len(regions_by_result) != len(results):
            raise SeamValidationError(
                "The contact overlay returned an invalid result-owner count."
            )

        regions_by_result = [
            list(regions)
            for regions in regions_by_result
        ]

        region_count = sum(
            len(regions)
            for regions in regions_by_result
        )

        if region_count == 0:
            raise SeamValidationError(
                "An existing contact has no result owner."
            )

        # Replace the old relationship only in the detached partner document.
        partner_document["seams"].remove(reciprocal)

        new_ids = []

        for result_index, regions in enumerate(regions_by_result):
            owner = results[result_index]
            owner_document = result_documents[result_index]

            for region in regions:
                # Preserve identity only for a single intact owner region.
                seam_id = (
                    old_record["seam_id"]
                    if region_count == 1
                    else fresh_seam_id()
                )

                if any(
                    record["seam_id"] == seam_id
                    for record in owner_document["seams"]
                ):
                    raise SeamValidationError(
                        "A migrated seam ID already exists on its new owner."
                    )

                if any(
                    record["seam_id"] == seam_id
                    for record in partner_document["seams"]
                ):
                    raise SeamValidationError(
                        "A migrated seam ID already exists on its partner."
                    )

                # Use the source side explicitly, independent of overlay internals.
                owner_frame = dict(region)
                owner_frame["side"] = old_record["side"]
                _checked_contact_step(
                    f"Migrated result contact "
                    f"[object={owner.name!r}, seam={seam_id}]",
                    _verify_current_cap, owner, owner_frame, tolerance,
                )

                partner_check_frame = dict(region)
                partner_check_frame["side"] = reciprocal["side"]
                _checked_contact_step(
                    f"Migrated partner contact "
                    f"[object={partner.name!r}, seam={seam_id}]",
                    _verify_current_cap,
                    partner,
                    partner_check_frame,
                    tolerance,
                )

                migrated = _record_for_object(
                    old_record,
                    owner_frame,
                    owner,
                )
                migrated["seam_id"] = seam_id
                migrated["partner_id"] = partner_id

                # Rebase the identical world contour on the external partner.
                reverse_frame = dict(region)
                reverse_frame["side"] = reciprocal["side"]

                reverse_record = _record_for_object(
                    reciprocal,
                    reverse_frame,
                    partner,
                )
                reverse_record["seam_id"] = seam_id
                reverse_record["partner_id"] = owner_document["object_id"]

                owner_document["seams"].append(migrated)
                partner_document["seams"].append(reverse_record)

                new_ids.append({
                    "seam_id": seam_id,
                    "new_owner_id": owner_document["object_id"],
                })

        transfers.append({
            "previous_seam_id": old_record["seam_id"],
            "regions": new_ids,
        })

    # Prepare every JSON payload before changing any object property.
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
        "transfers": transfers,
    })

    touched = [source, *results]
    touched.extend(
        obj
        for obj, _document in partners.values()
    )

    snapshots = []
    seen = set()

    for obj in touched:
        pointer = obj.as_pointer()

        if pointer not in seen:
            snapshots.append(_snapshot(obj))
            seen.add(pointer)

    def rollback():
        """Restore all snapshots, attempting every object even after an error."""
        errors = []

        for snapshot in reversed(snapshots):
            try:
                _restore(snapshot)
            except Exception as exc:
                errors.append(exc)

        if errors:
            raise RuntimeError(
                "Freehand metadata rollback could not restore every object."
            ) from errors[0]

    try:
        for obj, payload in changes:
            obj[DATA_KEY] = payload

        # Retain history without leaving an active duplicated seam identity.
        source[ARCHIVE_KEY] = archive
        del source[DATA_KEY]
        del source[OBJECT_ID_KEY]

    except Exception:
        rollback()
        raise

    return rollback

