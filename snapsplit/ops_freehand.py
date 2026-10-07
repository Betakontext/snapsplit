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

import math

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


# Stage A uses an operator property, not a persistent scene property.
# The panel control will be introduced with the later integration stage.
DEFAULT_BRUSH_RADIUS = 10.0
SAMPLE_SPACING = 6.0
MAX_SAMPLES = 200
MAX_STROKE_POINTS = 4096

ORANGE = (1.0, 0.35, 0.04, 1.0)
GRAY = (0.48, 0.52, 0.58, 0.75)
INVALID_COLOR = (1.0, 0.15, 0.12, 0.9)

_ACTIVE_OPERATORS = []


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

    count = min(MAX_SAMPLES, max(2, math.ceil(total / SAMPLE_SPACING) + 1))
    result = []
    segment = 0

    for i in range(count):
        distance = total * i / (count - 1)
        while segment < len(points) - 2 and lengths[segment + 1] < distance:
            segment += 1

        span = lengths[segment + 1] - lengths[segment]
        factor = (distance - lengths[segment]) / span if span > 1e-8 else 0.0
        result.append(points[segment].lerp(points[segment + 1], factor))

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
        raise ValueError("The stroke has no clear direction. Draw a straighter line.")

    angle = 0.5 * math.atan2(2.0 * xy, xx - yy)
    direction = Vector((math.cos(angle), math.sin(angle)))
    positions = [(point - center).dot(direction) for point in points]

    low = min(positions)
    high = max(positions)
    if high - low < 8.0:
        raise ValueError("Draw a stroke at least 8 pixels long.")

    return center, center + direction * low, center + direction * high


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

    factor = max(0.0, min(1.0, (point - a).dot(delta) / denominator))
    return (point - (a + factor * delta)).length


def _polygon_distance(point, polygon):
    """Return the distance to the boundary of a closed 2D polygon."""
    return min(
        _point_segment_distance(point, polygon[i], polygon[(i + 1) % len(polygon)])
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


def _extract_sections(mesh, matrix_world, plane_point, plane_normal, tolerance):
    """Bisect a temporary world-space BMesh and extract closed section loops.

    No object, mesh datablock, transform, or collection is modified.
    Edges are accepted only when adjacent faces extend to both plane sides.
    This excludes unrelated pre-existing coplanar face interiors.
    """
    bm = bmesh.new()

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
                abs((vertex.co - plane_point).dot(plane_normal)) > edge_tolerance
                for vertex in edge.verts
            ):
                continue

            has_positive = False
            has_negative = False

            for face in edge.link_faces:
                for vertex in face.verts:
                    distance = (vertex.co - plane_point).dot(plane_normal)
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
                    invalid_segments.extend(
                        (edge.verts[0].co.copy(), edge.verts[1].co.copy())
                    )
                continue

            start = seed.verts[0]
            vertex = start
            previous_edge = None
            ordered = []

            for _ in range(len(component_edges)):
                ordered.append(vertex.co.copy())
                edge = next(
                    edge
                    for edge in adjacency[vertex]
                    if edge is not previous_edge
                )
                vertex = edge.other_vert(vertex)
                previous_edge = edge

            if vertex is start and len(ordered) == len(component_vertices):
                loops.append(ordered)
            else:
                invalid_count += 1
                for edge in component_edges:
                    invalid_segments.extend(
                        (edge.verts[0].co.copy(), edge.verts[1].co.copy())
                    )

        return loops, invalid_segments, invalid_count

    finally:
        bm.free()


class SNAP_OT_freehand_cut(Operator):
    """Draw a stroke and preview locally touched planar section loops."""

    bl_idname = "snapsplit.freehand_cut"
    bl_label = "Freehand Cut"
    bl_description = "Preview a local planar cut from a freehand stroke"
    bl_options = {'REGISTER'}

    brush_radius_px: FloatProperty(
        name="Brush Radius",
        description="Screen-space tolerance for touching a section loop",
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
        """Start the preview and install viewport-scoped draw handlers."""
        if _ACTIVE_OPERATORS:
            report_user(self, 'WARNING', "A Freehand Cut preview is already active.")
            return {'CANCELLED'}

        obj = context.active_object

        if obj.modifiers:
            report_user(
                self, 'ERROR',
                "Freehand Cut stage A requires an object without modifiers. "
                "Apply or remove the modifiers first.",
            )
            return {'CANCELLED'}

        if obj.data.shape_keys is not None:
            report_user(
                self, 'ERROR',
                "Freehand Cut stage A does not support shape keys.",
            )
            return {'CANCELLED'}

        if not obj.data.polygons:
            report_user(self, 'ERROR', "The active mesh has no faces.")
            return {'CANCELLED'}

        if context.space_data.region_quadviews:
            report_user(
                self, 'ERROR',
                "Please leave Quad View before starting Freehand Cut.",
            )
            return {'CANCELLED'}

        region = next(
            (region for region in context.area.regions if region.type == 'WINDOW'),
            None,
        )
        if region is None:
            report_user(self, 'ERROR', "No viewport window region was found.")
            return {'CANCELLED'}

        try:
            obj.matrix_world.inverted()
        except ValueError:
            report_user(self, 'ERROR', "The object transform is singular.")
            return {'CANCELLED'}

        self._obj = obj
        self._mesh = obj.data
        self._matrix_world = obj.matrix_world.copy()
        self._mesh_counts = self._counts()

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
            self._shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')
            self._polyline_shader = True
        except Exception:
            try:
                self._shader = gpu.shader.from_builtin('UNIFORM_COLOR')
                self._polyline_shader = False
            except Exception as exc:
                report_user(self, 'ERROR', "Cannot create preview shader: {error}", error=exc)
                return {'CANCELLED'}

        try:
            self._handle_pixel = bpy.types.SpaceView3D.draw_handler_add(
                self._draw_pixel, (), 'WINDOW', 'POST_PIXEL',
            )
            self._handle_view = bpy.types.SpaceView3D.draw_handler_add(
                self._draw_view, (), 'WINDOW', 'POST_VIEW',
            )
            self._timer = self._wm.event_timer_add(0.25, window=self._window)
            _ACTIVE_OPERATORS.append(self)
            self._wm.modal_handler_add(self)
            self._set_header("Draw with LMB | Shift-release: axis snap | Esc/RMB: exit")
        except Exception as exc:
            self._cleanup()
            report_user(self, 'ERROR', "Cannot start preview: {error}", error=exc)
            return {'CANCELLED'}

        warn_if_unapplied_transforms(obj, operator=self)
        self._area.tag_redraw()
        return {'RUNNING_MODAL'}

    def _counts(self):
        """Return a cheap topology signature for the original mesh."""
        return (
            len(self._mesh.vertices),
            len(self._mesh.edges),
            len(self._mesh.polygons),
        )

    def _source_valid(self, context):
        """Reject source changes rather than showing stale geometry."""
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
        """Convert window coordinates to the selected WINDOW region."""
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
            self._region, self._rv3d, coordinate,
        )
        direction = view3d_utils.region_2d_to_vector_3d(
            self._region, self._rv3d, coordinate,
        ).normalized()
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
            local_origin, local_direction.normalized(),
        )
        return self._matrix_world @ location if result else None

    def _append_point(self, point, force=False):
        """Collect a bounded stroke while preserving its entire length."""
        if not self._points or force or (point - self._points[-1]).length >= 2.0:
            if self._points and (point - self._points[-1]).length < 1e-6:
                return

            self._points.append(point.copy())

            if len(self._points) > MAX_STROKE_POINTS:
                self._points = self._points[::2] + [self._points[-1]]

            if len(self._points) >= 2:
                self._stroke_batch = batch_for_shader(
                    self._shader,
                    'LINE_STRIP',
                    {"pos": [(p.x, p.y, 0.0) for p in self._points]},
                )

    def _world_pixel_radius(self, coordinate, world_point):
        """Convert brush pixels to a local world-space tolerance."""
        center = view3d_utils.region_2d_to_location_3d(
            self._region, self._rv3d, coordinate, world_point,
        )
        shifted = view3d_utils.region_2d_to_location_3d(
            self._region,
            self._rv3d,
            coordinate + Vector((self.brush_radius_px, 0.0)),
            world_point,
        )
        return (shifted - center).length

    def _build_preview(self, snap):
        """Fit the plane, bisect a copy, and identify locally touched loops."""
        self._preview_batches = []
        self._selected_count = 0
        self._plane_point = None
        self._plane_normal = None

        samples = _resample_stroke(self._points)
        _center, endpoint_a, endpoint_b = _fit_line(samples)

        hits = []
        for coordinate in samples:
            location = self._hit(coordinate)
            if location is not None:
                hits.append((coordinate, location))

        if not hits:
            raise ValueError("The stroke did not hit the active mesh.")

        origin_a, direction_a = self._ray(endpoint_a)
        origin_b, direction_b = self._ray(endpoint_b)

        if self._rv3d.is_perspective:
            normal = direction_a.cross(direction_b)
        else:
            normal = (origin_b - origin_a).cross(direction_a)

        if normal.length_squared <= 1e-16:
            raise ValueError("Cannot determine a stable cutting plane.")

        normal.normalize()

        # Anchor near the surface instead of using a distant camera origin.
        anchor = sum((hit for _, hit in hits), Vector((0.0, 0.0, 0.0))) / len(hits)
        plane_point = anchor - normal * (anchor - origin_a).dot(normal)

        if snap:
            axis = max(range(3), key=lambda index: abs(normal[index]))
            sign = 1.0 if normal[axis] >= 0.0 else -1.0
            normal = Vector((0.0, 0.0, 0.0))
            normal[axis] = sign
            plane_point = anchor.copy()

        corners = [
            self._matrix_world @ Vector(corner)
            for corner in self._obj.bound_box
        ]
        low = Vector(tuple(min(p[i] for p in corners) for i in range(3)))
        high = Vector(tuple(max(p[i] for p in corners) for i in range(3)))
        diagonal = (high - low).length

        if diagonal <= 1e-12:
            raise ValueError("The object is too small or degenerate.")

        tolerance = max(diagonal * 1e-7, 1e-10)

        # A small deterministic offset reduces vertex-aligned degeneracies.
        # Stage B must reuse this exact stored plane for its actual cut.
        plane_point += normal * (tolerance * 4.0)

        loops, invalid_segments, invalid_count = _extract_sections(
            self._mesh,
            self._matrix_world,
            plane_point,
            normal,
            tolerance,
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
            projected = hit - normal * (hit - plane_point).dot(normal)
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
                distance = _polygon_distance(point_2d, polygon)
                if distance <= radius or _point_in_polygon(point_2d, polygon):
                    eligible.append((distance, index))

            if eligible:
                # Select only the nearest eligible boundary for this surface hit.
                # This avoids marking every overlapping projected loop.
                selected.add(min(eligible)[1])

        for index, loop in enumerate(loops):
            coordinates = []
            for i, point in enumerate(loop):
                coordinates.extend((point, loop[(i + 1) % len(loop)]))

            batch = batch_for_shader(
                self._shader, 'LINES', {"pos": coordinates},
            )
            self._preview_batches.append((
                batch,
                ORANGE if index in selected else GRAY,
                3.0 if index in selected else 1.5,
            ))

        if invalid_segments:
            batch = batch_for_shader(
                self._shader, 'LINES', {"pos": invalid_segments},
            )
            self._preview_batches.append((batch, INVALID_COLOR, 2.0))

        self._plane_point = plane_point.copy()
        self._plane_normal = normal.copy()
        self._selected_count = len(selected)

        self._set_header(
            f"Preview: {len(selected)}/{len(loops)} loops touched"
            " | Enter: confirm preview | LMB: redraw | MMB: orbit | Esc: exit"
        )

        report_user(
            self, 'INFO',
            "Preview: {selected} of {total} closed loops touched. No mesh was changed.",
            selected=len(selected), total=len(loops),
        )

        if invalid_count:
            report_user(
                self, 'WARNING',
                "{count} open or branched section(s) were excluded and shown in red.",
                count=invalid_count,
            )

        if not selected:
            report_user(
                self, 'WARNING',
                "No valid section loop was touched. Try a straighter stroke.",
            )

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
                self._shader.uniform_float("color", color)

                if self._polyline_shader:
                    self._shader.uniform_float(
                        "viewportSize", gpu.state.viewport_get()[2:],
                    )
                    self._shader.uniform_float("lineWidth", width)
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
        if not self._draw_here() or not self._drawing or self._stroke_batch is None:
            return
        try:
            self._draw_batches([(self._stroke_batch, ORANGE, 3.0)])
        except Exception as exc:
            self._draw_error = str(exc)

    def _draw_view(self):
        """Draw section loops in world space, including hidden loop portions."""
        if not self._draw_here() or self._drawing or not self._preview_batches:
            return
        try:
            self._draw_batches(self._preview_batches)
        except Exception as exc:
            self._draw_error = str(exc)

    def _set_header(self, text):
        """Display modal instructions in the viewport header."""
        self._area.header_text_set(text)

    def _cleanup(self):
        """Remove every owned resource; repeated calls are harmless."""
        if getattr(self, "_closed", True):
            return

        self._closed = True

        for attribute in ("_handle_pixel", "_handle_view"):
            handle = getattr(self, attribute, None)
            if handle is not None:
                try:
                    bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')
                except (ReferenceError, ValueError, RuntimeError):
                    pass
                setattr(self, attribute, None)

        if self._timer is not None:
            try:
                self._wm.event_timer_remove(self._timer)
            except (ReferenceError, ValueError, RuntimeError):
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

    def modal(self, context, event):
        """Handle drawing, preview confirmation, navigation, and safe exit."""
        if self._closed:
            return {'CANCELLED'}

        try:
            # Compare Area objects explicitly; collection membership expects names.
            if not any(
                area == self._area
                for area in self._window.screen.areas
            ):
                self._cleanup()
                return {'CANCELLED'}


            if not self._source_valid(context):
                report_user(
                    self, 'WARNING',
                    "The active object changed. Freehand Cut preview was cancelled.",
                )
                self._cleanup()
                return {'CANCELLED'}

            if self._draw_error is not None:
                report_user(
                    self, 'ERROR',
                    "Preview drawing failed: {error}",
                    error=self._draw_error,
                )
                self._cleanup()
                return {'CANCELLED'}

            if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
                self._cleanup()
                return {'CANCELLED'}

            if event.type == 'TIMER':
                return {'RUNNING_MODAL'}

            point = self._mouse(event)

            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                if not self._inside(point):
                    return {'RUNNING_MODAL'}

                # Alt-LMB remains available for alternative navigation layouts.
                if event.alt:
                    return {'PASS_THROUGH'}

                self._drawing = True
                self._points = []
                self._stroke_batch = None
                self._preview_batches = []
                self._selected_count = 0
                self._plane_point = None
                self._plane_normal = None
                self._append_point(point)
                self._set_header("Drawing | Release LMB to preview | Shift: axis snap")
                self._area.tag_redraw()
                return {'RUNNING_MODAL'}

            if self._drawing:
                if event.type == 'MOUSEMOVE':
                    self._append_point(point)
                    self._area.tag_redraw()
                    return {'RUNNING_MODAL'}

                if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                    self._append_point(point, force=True)
                    self._drawing = False
                    self._stroke_batch = None

                    try:
                        self._build_preview(snap=event.shift)
                    except (ValueError, RuntimeError) as exc:
                        self._preview_batches = []
                        self._selected_count = 0
                        self._plane_point = None
                        self._plane_normal = None
                        self._set_header(
                            "Draw again with LMB | Shift-release: axis snap | Esc: exit"
                        )
                        report_user(self, 'WARNING', "Preview unavailable: {error}", error=exc)

                    self._area.tag_redraw()
                    return {'RUNNING_MODAL'}

                # Keep the camera unchanged throughout a single stroke.
                return {'RUNNING_MODAL'}

            if event.type in {'RET', 'NUMPAD_ENTER'} and event.value == 'PRESS':
                if self._selected_count:
                    report_user(
                        self, 'INFO',
                        "Preview confirmed. Stage A does not cut the mesh. "
                        "Draw another stroke or press Esc to exit.",
                    )
                else:
                    report_user(
                        self, 'WARNING',
                        "Draw a stroke that touches at least one valid section loop.",
                    )
                return {'RUNNING_MODAL'}

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

            # Block editing shortcuts while this source-dependent preview runs.
            return {'RUNNING_MODAL'}

        except Exception as exc:
            report_user(self, 'ERROR', "Freehand preview failed: {error}", error=exc)
            self._cleanup()
            return {'CANCELLED'}


_CLASSES = (SNAP_OT_freehand_cut,)


def register():
    """Register the stage A preview operator."""
    for cls in _CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    """Close active previews before unregistering their operator class."""
    for operator in tuple(_ACTIVE_OPERATORS):
        operator._cleanup()

    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)
