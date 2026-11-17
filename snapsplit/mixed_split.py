# SnapSplit mixed planar runtime support.
# Addon imports stay lazy to avoid import cycles.
import json
import uuid


def _planar_frames(results, cuts, tolerance):
    """Yield cut-face frames from Blender's evaluated mesh tessellation.

    Loop triangles include triangles, quads, and n-gons without changing
    the mesh topology. Coordinates and orientation are evaluated in world
    space so object transforms do not change the geometric test.
    """
    import math
    from mathutils import Vector

    eps = float(tolerance)
    if not math.isfinite(eps) or eps <= 0.0:
        raise ValueError("Planar contact tolerance must be positive and finite.")

    axes = (
        Vector((1.0, 0.0, 0.0)),
        Vector((0.0, 1.0, 0.0)),
        Vector((0.0, 0.0, 1.0)),
    )

    # Cache world coordinates and tessellation once per result object.
    meshes = []
    for obj in results:
        mesh = obj.data
        mesh.calc_loop_triangles()
        coords = [
            obj.matrix_world @ vertex.co
            for vertex in mesh.vertices
        ]
        triangles = [
            tuple(triangle.vertices)
            for triangle in mesh.loop_triangles
        ]
        meshes.append((coords, triangles))

    for cut_index, (point, normal) in enumerate(cuts):
        origin = Vector(point)
        no = Vector(normal)

        if not all(math.isfinite(value) for value in (*origin, *no)):
            raise ValueError(
                f"Cut plane {cut_index} contains non-finite coordinates."
            )

        if no.length == 0.0:
            raise ValueError(
                f"Cut plane {cut_index} has a zero-length normal."
            )
        no.normalize()

        axis = min(axes, key=lambda value: abs(value.dot(no)))
        tangent = axis - no * axis.dot(no)
        tangent.normalize()

        signed = []
        negatives = []
        positives = []

        for index, obj in enumerate(results):
            coords, _triangles = meshes[index]
            values = [
                (coord - origin).dot(no)
                for coord in coords
            ]
            signed.append(values)

            if not values:
                continue

            minimum = min(values)
            maximum = max(values)

            if minimum < -eps and maximum <= eps:
                negatives.append((index, obj))
            elif minimum >= -eps and maximum > eps:
                positives.append((index, obj))
            elif minimum < -eps and maximum > eps:
                raise ValueError(
                    f"Result '{obj.name}' still crosses cut plane "
                    f"{cut_index}; contact ownership is not resolved."
                )

        if not negatives or not positives:
            raise ValueError(
                f"Cut plane {cut_index} has no results on both sides "
                f"within world tolerance {eps:.9g}."
            )

        emitted = 0

        for negative_index, negative in negatives:
            coords, triangles = meshes[negative_index]
            values = signed[negative_index]

            for indices in triangles:
                if any(abs(values[index]) > eps for index in indices):
                    continue

                tri = [coords[index] for index in indices]
                outward = (tri[1] - tri[0]).cross(tri[2] - tri[0])

                # Cross-product magnitude has area units. Do not compare
                # it to a length tolerance, which rejects small valid faces.
                if outward.length == 0.0:
                    continue

                outward.normalize()

                # Only the negative part's outward cap faces the cut normal.
                if outward.dot(no) < 1.0 - 1.0e-5:
                    continue

                frame = {
                    "origin": origin.copy(),
                    "normal": no.copy(),
                    "tangent": tangent.copy(),
                    "side": 1,
                    "loops": [[vertex.copy() for vertex in tri]],
                }
                emitted += 1
                yield frame, negative_index, positives

        if emitted == 0:
            names = ", ".join(obj.name for _, obj in negatives)
            raise ValueError(
                f"No outward cap triangles were found for cut plane "
                f"{cut_index} on [{names}]. Check capping, face normals, "
                f"and world tolerance {eps:.9g}."
            )


def _build_documents(results, contacts, tolerance):
    """Prepare reciprocal documents and restore properties on failure.

    Empty documents are rejected before any object properties are written.
    The migration API requires every result to have a valid seam document.
    """
    import math
    from .seam_data import (
        DATA_KEY,
        OBJECT_ID_KEY,
        SCHEMA_VERSION,
        _validated_document,
    )
    from .seam_migration import _record_for_object

    tolerance = float(tolerance)
    if not math.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("Stored contact tolerance must be positive and finite.")

    results = list(results)
    contacts = list(contacts)

    if len(results) < 2:
        raise ValueError("At least two planar results are required.")

    pointers = [obj.as_pointer() for obj in results]
    if len(set(pointers)) != len(pointers):
        raise ValueError("The planar result list contains duplicate objects.")

    docs = [
        {
            "version": SCHEMA_VERSION,
            "object_id": uuid.uuid4().hex,
            "seams": [],
        }
        for _obj in results
    ]

    for contact_index, contact in enumerate(contacts):
        negative_index, positive_index, region = contact

        for index in (negative_index, positive_index):
            if (
                isinstance(index, bool)
                or not isinstance(index, int)
                or not 0 <= index < len(results)
            ):
                raise ValueError(
                    f"Contact {contact_index} has an invalid result index."
                )

        if negative_index == positive_index:
            raise ValueError(
                f"Contact {contact_index} connects an object to itself."
            )

        loops = region.get("loops")
        if not loops or any(len(loop) < 3 for loop in loops):
            raise ValueError(
                f"Contact {contact_index} has missing or malformed contours."
            )

        seam_id = uuid.uuid4().hex

        for own, other, side in (
            (negative_index, positive_index, -1),
            (positive_index, negative_index, 1),
        ):
            template = {
                "kind": "FREEHAND",
                "capped_at_creation": True,
                "tolerance_world_at_creation": tolerance,
                "seam_id": seam_id,
                "partner_id": docs[other]["object_id"],
            }
            frame = dict(region)
            frame["side"] = side

            record = _record_for_object(template, frame, results[own])
            docs[own]["seams"].append(record)

    empty_names = [
        obj.name
        for obj, doc in zip(results, docs)
        if not doc["seams"]
    ]
    if empty_names:
        raise ValueError(
            "Planar contact generation found no reciprocal contact for: "
            + ", ".join(repr(name) for name in empty_names)
            + f". Generated contacts: {len(contacts)}; "
            + f"world tolerance: {tolerance:.9g}. "
            + "No seam documents were written."
        )

    # Serialize every document before modifying any result object.
    payloads = [
        json.dumps(doc, allow_nan=False)
        for doc in docs
    ]
    keys = (OBJECT_ID_KEY, DATA_KEY)
    snapshots = [
        {
            key: (key in obj, obj.get(key))
            for key in keys
        }
        for obj in results
    ]

    try:
        # Write all partners before running document validation.
        for obj, doc, payload in zip(results, docs, payloads):
            obj[OBJECT_ID_KEY] = doc["object_id"]
            obj[DATA_KEY] = payload

        for obj in results:
            _validated_document(obj)

    except Exception as exc:
        rollback_errors = []

        for obj, snapshot in zip(results, snapshots):
            for key, (existed, value) in snapshot.items():
                try:
                    if existed:
                        obj[key] = value
                    elif key in obj:
                        del obj[key]
                except Exception as rollback_exc:
                    rollback_errors.append(
                        f"{obj.name}.{key}: {rollback_exc}"
                    )

        if rollback_errors:
            raise RuntimeError(
                f"Planar seam document creation failed: {exc}. "
                "Property rollback also failed: "
                + "; ".join(rollback_errors)
            ) from exc
        raise

    return docs



def execute_planar_mixed(operator, context, original_execute, globals_dict):
    """Run the legacy planar splitter on a private clone and record contacts."""
    import bpy
    from mathutils import Vector
    from .seam_data import DATA_KEY, OBJECT_ID_KEY, _validated_document, has_freehand_metadata
    from .seam_migration import ARCHIVE_KEY, migrate_intact_freehand_seams
    source = context.active_object
    props = context.scene.snapsplit
    def error(message):
        operator.report({'ERROR'}, message)
    if source is None or source.type != 'MESH' or source.mode != 'OBJECT':
        error('Mixed planar split requires an active mesh in Object Mode.')
        return {'CANCELLED'}
    metadata = has_freehand_metadata(source)
    if ARCHIVE_KEY in source:
        error('Archived source cannot be split.')
        return {'CANCELLED'}
    # A metadata source must be capped; do not clone or invoke the legacy operator.
    if metadata and not props.cap_seams_during_split:
        error('Mixed planar split of a Freehand source requires auto cap during split.')
        return {'CANCELLED'}
    if not metadata and not props.cap_seams_during_split:
        return original_execute(operator, context)
    if metadata:
        try:
            _validated_document(source)
        except Exception as exc:
            error('Invalid source seam document: ' + str(exc))
            return {'CANCELLED'}
    if source.constraints or source.animation_data or source.vertex_groups:
        error('Mixed planar split requires a static source without constraints, animation, or vertex groups.')
        return {'CANCELLED'}
    if source.modifiers or source.data.shape_keys:
        error('Mixed planar split requires a static mesh without modifiers or shape keys.')
        return {'CANCELLED'}
    selected = list(context.selected_objects)
    active = context.view_layer.objects.active
    source_hidden = source.hide_get()
    before = {obj.as_pointer() for obj in bpy.data.objects}
    owned_meshes = set()
    rollback = None
    def cleanup(keep=()):
        keep_pointers = {obj.as_pointer() for obj in keep}
        problems = []
        for obj in list(bpy.data.objects):
            if obj.as_pointer() not in before and obj.as_pointer() not in keep_pointers:
                try:
                    bpy.data.objects.remove(obj, do_unlink=True)
                except Exception as exc:
                    problems.append('object: ' + str(exc))
        for mesh in list(bpy.data.meshes):
            if mesh.as_pointer() in owned_meshes and mesh.users == 0:
                try:
                    bpy.data.meshes.remove(mesh)
                except Exception as exc:
                    problems.append('mesh: ' + str(exc))
        if problems:
            operator.report({'WARNING'}, 'Cleanup warning (rollback is not guaranteed): ' + '; '.join(problems))
    try:
        clone = source.copy()
        clone.data = source.data.copy()
        owned_meshes.add(clone.data.as_pointer())
        clone.name = 'SNAPSPLIT_MIXED_WORK_' + uuid.uuid4().hex
        for key in (DATA_KEY, OBJECT_ID_KEY, ARCHIVE_KEY):
            if key in clone:
                del clone[key]
        for collection in (list(source.users_collection) or [context.scene.collection]):
            collection.objects.link(clone)
        # Compute cuts and tolerance before the legacy operator mutates/deletes clone.
        cuts = list(globals_dict['create_cut_data_with_offset'](
            clone, props.split_axis, max(2, int(props.parts_count)),
            global_offset_scene=float(getattr(props, 'split_offset_mm', 0.0)) * globals_dict['unit_mm']()))
        bbox = [clone.matrix_world @ Vector(corner) for corner in clone.bound_box]
        tolerance = max(1.0e-7, max((a - b).length for a in bbox for b in bbox) * 1.0e-6)
        if not cuts:
            raise RuntimeError('planar splitter produced no cut planes')
        for obj in context.selected_objects:
            obj.select_set(False)
        clone.select_set(True)
        context.view_layer.objects.active = clone
        old_result = original_execute(operator, context)
        if 'FINISHED' not in old_result:
            raise RuntimeError('original planar operator did not finish')
        results = [obj for obj in context.selected_objects if obj.type == 'MESH'
                   and obj.as_pointer() not in before and obj is not clone]
        # Include meshes from every new object, even transient objects the legacy
        # operator did not leave selected.  The source data pointer is never owned.
        for obj in bpy.data.objects:
            if obj.as_pointer() not in before and obj.type == 'MESH':
                owned_meshes.add(obj.data.as_pointer())
        if len(results) < 2:
            raise RuntimeError('original planar operator produced fewer than two mesh parts')
        from .seam_regions import _check_closed_mesh, overlay_region
        for obj in results:
            _check_closed_mesh(obj)
        contacts = []
        for frame, negative_index, positives in _planar_frames(results, cuts, tolerance):
            positive_objects = [obj for _, obj in positives]
            for positive_index, regions in enumerate(overlay_region(frame, positive_objects, tolerance)):
                for region in regions:
                    contacts.append((negative_index, positives[positive_index][0], region))
        _build_documents(results, contacts, tolerance)
        if metadata:
            rollback = migrate_intact_freehand_seams(source, results)
        source.hide_set(True)
        for obj in context.selected_objects:
            obj.select_set(False)
        for obj in results:
            obj.select_set(True)
        context.view_layer.objects.active = results[0]
    except Exception as exc:
        messages = [str(exc)]
        if callable(rollback):
            try:
                rollback()
            except Exception as rollback_exc:
                messages.append('migration rollback failed: ' + str(rollback_exc))
        cleanup()
        try:
            source.hide_set(source_hidden)
        except Exception as restore_exc:
            messages.append('hide restore failed: ' + str(restore_exc))
        try:
            for obj in context.selected_objects:
                obj.select_set(False)
            for obj in selected:
                obj.select_set(True)
            context.view_layer.objects.active = active
        except Exception as restore_exc:
            messages.append('selection restore failed: ' + str(restore_exc))
        error('; '.join(messages))
        return {'CANCELLED'}
    cleanup(results)
    return {'FINISHED'}
