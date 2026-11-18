# SnapSplit

SnapSplit is a Blender add-on for splitting 3D models into printable parts and creating matching connectors and sockets. It is useful for models that exceed your print bed, modular sculptures, props, prototypes, and other projects that need to be assembled after printing.

SnapSplit combines planar segmentation, stroke-based local cuts, hollow-aware seam capping, and connector placement in one workflow. Connector options include pins, tenons, dovetails, snap variants, and custom mesh shapes.

Material-specific tolerance presets and a manual override help you adjust the fit for your printing process. Final fit depends on your material, printer calibration, print orientation, and connector dimensions.

**Current version: 0.2.0**

![SnapSplit Slideshow](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_SLAIDSHOW.gif?cache=1)

### Why SnapSplit?

SnapSplit brings two common modeling tasks together:

- Splitting large or complex models into manageable parts.
- Creating matching connector and socket geometry for assembly.

Place connectors along a seam line, distribute them across a grid, or position them individually with mouse clicks. Live Preview helps you inspect placement before applying the connector operations.

SnapSplit also supports splitting and capping **existing hollow models**. It is not a replacement for a dedicated hollowing tool or a final printability check.

Snap variants are intended for glue-free assembly. Test the fit on a small sample before printing a large project.

Feedback, bug reports, and suggestions are welcome.

### Blender compatibility

The maintainer reports successful testing with:

- Blender 4.5.3 LTS
- Blender 4.5.9 LTS
- Blender 5.0.1
- Blender 5.1.0
- Blender 5.1.1
- Blender 5.2.0 LTS
- Blender 5.2.2 LTS

Please report your results with other Blender versions, including the SnapSplit version and the workflow you tested.

**Metadata note:** The current extension manifest declares Blender 4.2.0 as the minimum version, while the legacy `bl_info` metadata specifies Blender 5.2.0. These declarations are not a guarantee that every intervening version has been tested.

### Installation

1. Download the packaged SnapSplit release ZIP.
2. In Blender, open **Edit → Preferences → Add-ons**.
3. Open the add-on menu and choose **Install from Disk…**.
4. Select the SnapSplit ZIP and complete the installation.
5. Enable SnapSplit if it is not enabled automatically.

The exact installation controls may vary slightly between Blender versions.

If you download the repository rather than a packaged release, create an extension ZIP containing `blender_manifest.toml` and the add-on modules at the archive root. Do not assume that the repository download ZIP is already an installable package.

### Blender setup

Recommended scene settings:

- **Unit System:** Metric
- **Unit Scale:** 1.000
- **Length:** Adaptive

Open the **3D Viewport sidebar** with **N**, then select the **SnapSplit** tab.

### Mesh preparation and quality checks

Before splitting or adding connectors:

- Save a backup of your model.
- Check the mesh for non-manifold geometry, intersections, inconsistent normals, and thin walls.
- Use Blender’s **3D Print Toolbox** or another suitable mesh-checking tool.
- Start with a watertight mesh wherever possible.
- Review unapplied rotation and scale.

Planar Split attempts to apply rotation and scale automatically while preserving object location. Nevertheless, checking transforms before an operation helps produce predictable results.

**Freehand Cut has stricter requirements:** apply or remove modifiers first, and use a static mesh without shape keys. See the Freehand Cut limitations below.

After splitting and adding connectors:

- Confirm that every intended part contains faces.
- Inspect the caps, connector roots, and sockets.
- Check the result for non-manifold edges and insufficient wall thickness.
- Verify the exported dimensions in your slicer.
- Print a small fit test before committing to a large assembly.

### Planar Split workflow

Expand the segmentation section using **More…** to access the additional settings.

![SnapSplit segmentation settings](https://dev.betakontext.de/snapsplit/img/jpg/betakontext_snapsplit_UI_01.jpg?cache=1)

![SnapSplit additional segmentation settings](https://dev.betakontext.de/snapsplit/img/jpg/betakontext_snapsplit_UI_02.jpg?cache=1)

1. Select the mesh you want to split.
2. Choose the split axis: **X**, **Y**, or **Z**.
3. Set the desired **Number of Parts**.
4. Enable **Show split preview** to display the planned cutting planes.
5. Adjust the split offset, or use **Adjust split axis**.
6. Choose whether to enable **Cap seams during split**.
7. Run **Planar Split**.
8. Inspect the resulting parts.

![Planar segmentation preview](https://dev.betakontext.de/snapsplit/img/jpg/betakontext_snapsplit_SEG_01.jpg?cache=1)

The split offset shifts the planned cutting positions along the selected axis. An offset of **0** means no additional shift; for a two-part split, the default plane is at the middle of the object’s extent along that axis.

#### Seam capping

With **Cap seams during split** enabled, SnapSplit attempts to close the new cut boundaries:

- For solid geometry, it fills the cut surface.
- For supported hollow geometry, it fills between the outer and inner boundaries to preserve the cavity.

![Capped seams on a hollow model](https://dev.betakontext.de/snapsplit/img/jpg/betakontext_snapsplit_SEG_03.jpg?cache=1)

Automatic capping can increase processing time on dense meshes or when creating many parts. You can disable it and use **Cap seams now** afterwards where the resulting boundaries are supported.

Always inspect the caps. Hollow-aware capping depends on valid, identifiable section loops and is not a general-purpose mesh repair operation.

### Freehand Cut workflow

**Freehand Cut** creates a local planar cut from a mouse-drawn stroke. The stroke determines a cutting plane and selects the material regions touched by the stroke.

**It does not create an arbitrary curved cutting path.**

![Planar segmentation preview](https://dev.betakontext.de/snapsplit/img/jpg/betakontext_snapsplit_SEG_04.jpg?cache=1)

1. Select the source mesh in **Object Mode**.
2. Apply or remove its modifiers.
3. Leave Quad View if it is active.
4. Choose whether to enable **Cap seams during split**.
5. Click **Freehand Cut**.
6. Draw a stroke across the intended cutting region with the **left mouse button**.
7. Release the button to generate the preview.
8. Inspect the highlighted section boundaries.
9. Press **Enter** to execute the cut, or **Esc/right-click** to cancel.

Hold **Shift when releasing the mouse button** to snap the cutting-plane normal to a world axis.

#### Preview colours

- **Orange:** Selected section boundaries.
- **Grey:** Unselected section boundaries.
- **Red:** Invalid open or branched sections.

Selection expands to complete material regions, including their associated inner boundaries. This helps preserve hollow sections rather than treating the outer and inner loops as unrelated cuts.

The preview does not modify the source mesh. On successful execution, SnapSplit creates new result objects and hides the unchanged original.

The shared **Cap seams during split** setting controls whether the new cut boundaries are closed or left open.

#### Current Freehand Cut limitations

Freehand Cut currently requires:

- An active mesh in Object Mode.
- No modifiers, including disabled modifiers.
- No shape keys.
- No vertex groups, constraints, or animation.
- A non-singular object transform.
- A source without existing SnapSplit seam metadata.

Repeated cutting of objects that already contain SnapSplit seam metadata is not supported in this version. Do not delete seam metadata merely to bypass this restriction, because it identifies relationships needed by later operations.

Do not change the source geometry or transforms while the preview is active. Restart Freehand Cut if the source changes.

#### Connectors on Freehand seams

Connector placement on Freehand results is supported only when the seam relationship passes validation. Current requirements include:

- A unique reciprocal seam relationship between the partner parts.
- Seams that were **capped when the Freehand cut was created**.
- Matching seam frames and contours.
- Closed, edge-manifold partner meshes.
- No active viewport or render modifiers on the partner parts.
- Supported, non-mirrored transforms.

Capping an initially open Freehand seam later does not, by itself, satisfy the requirement that it was capped at creation.

**Automatic material-boundary and wall-depth validation is not currently enabled for Freehand connectors.** Check that every connector and socket has enough surrounding material, especially on hollow or thin-walled parts.

### Building connections

Expand the connections section using **More…** to choose the connector type and adjust its placement and dimensions.

![SnapSplit connection settings](https://dev.betakontext.de/snapsplit/img/jpg/betakontext_snapsplit_UI_03.jpg?cache=1) ![SnapSplit additional connection settings](https://dev.betakontext.de/snapsplit/img/jpg/betakontext_snapsplit_UI_04.jpg?cache=1)

Available connector options include:

- Cylindrical pins
- Rectangular tenons
- Dovetails
- Snap-pin variants
- Snap-tenon variants
- Snap-dovetail variants
- Custom mesh connectors

#### Line and grid placement

1. Select the adjacent parts you want to connect.
2. Choose a connector type.
3. Select **Line** or **Grid** placement.
4. Adjust the connector dimensions, spacing, margins, and other available parameters.
5. Choose a material tolerance profile or enter a positive tolerance override.
6. Enable **Live Preview** to inspect the placement.
7. Use **Swap Pin / Socket** if you want to reverse the connector and socket roles.
8. Click **Add connectors**.

SnapSplit joins the connector geometry to one partner and cuts the matching socket into the other. The swap setting reverses those roles.

![Custom connectors distributed across a seam](https://dev.betakontext.de/snapsplit/img/jpg/betakontext_snapsplit_CUSTOM_CON_01.jpg?cache=1)

*Example: Blender’s Suzanne mesh used as a custom connector.*

For multi-part selections, inspect the preview to confirm the intended seam and partner relationships. Freehand seams must meet the validation requirements described above.

#### Individual click placement

Use **Place connectors (click)** to position connectors individually on a supported connection surface.

![Individual connector placement](https://dev.betakontext.de/snapsplit/img/jpg/betakontext_snapsplit_CON_01.jpg?cache=1)

1. Select the intended partner parts.
2. Choose and configure the connector.
3. Start **Place connectors (click)**.
4. Click the desired positions on the connection surface.
5. Press **S** during click placement to swap the connector and socket roles.

![Connector placement and tolerance settings](https://dev.betakontext.de/snapsplit/img/jpg/betakontext_snapsplit_CON_02.jpg?cache=1)

![Connectors placed along a seam](https://dev.betakontext.de/snapsplit/img/jpg/betakontext_snapsplit_CON_03.jpg?cache=1)

#### Dovetails and snap variants

Dovetail options include snap spheres, span controls, and hard-side cutting settings.

![Dovetails with snap spheres and span controls](https://dev.betakontext.de/snapsplit/img/jpg/betakontext_snapsplit_CON_06.jpg?cache=1)

Check the available assembly direction and surrounding wall thickness. A connector that fits geometrically may still be difficult to assemble or too fragile to print.

#### Live Preview

Live Preview displays temporary wireframe connector geometry for placement checks.

- It is limited to **200 preview objects**.
- It does not reproduce the complete final Boolean result.
- It does not perform the final hard-side Boolean cut.
- It is not a printability or fit guarantee.

SnapSplit temporarily enables X-ray for supported preview and click-placement workflows where the viewport shading mode allows it.

### Custom connectors

Choose a watertight mesh object from your scene in the **Custom Connector Object** field.

SnapSplit scales a copy to the specified **Width / Length / Depth** dimensions and uses it as the connector shape. Custom connectors support line placement, grid placement, and individual click placement.

![Custom connector example](https://dev.betakontext.de/snapsplit/img/jpg/betakontext_snapsplit_CUSTOM_CON_02.jpg?cache=1)

Important preparation notes:

- The object’s **local Z axis** defines its depth/insertion direction.
- Use clean, watertight geometry.
- Inspect the orientation and scaled shape in the preview.
- Test socket clearance and assembly before printing the complete model.

Additional controls include custom snap spheres, chamfer, span axis, hard-side cutting, in-plane offsets, and in-plane rotation.

Custom connectors are useful for keyed shapes, anti-rotation features, logos, and purpose-designed assembly mechanisms. A custom shape is not automatically a reliable snap-fit mechanism.

### Tolerance profiles

The following presets specify clearance **per side**, in millimetres:

| Material profile | Default tolerance per side |
|---|---:|
| PLA | 0.20 mm |
| PETG | 0.30 mm |
| ABS | 0.25 mm |
| ASA | 0.25 mm |
| TPU | 0.35 mm |
| SLA | 0.10 mm |

Use the tolerance override field to replace the selected preset:

- **0:** Use the material profile value.
- **Positive value:** Use the entered tolerance instead.

**An override of 0 does not request zero clearance.**

These presets are starting points, not automatic printer calibration. Adjust them for your printer, material, print orientation, and required fit.

### Face-to-face alignment

SnapSplit includes a face-picking alignment tool that works in Object Mode.

Use it to align suitable connection faces before placing connectors, including on supported objects that were not created by SnapSplit’s splitting tools.

After alignment, inspect the connection orientation and preview. Alignment alone does not guarantee that an arbitrary pair of meshes forms a valid connector seam.

### Exporting parts

Export the finished parts using Blender’s available export tools, such as STL or OBJ. Use 3MF if a suitable exporter is available in your Blender setup.

SnapSplit’s collection organization helps keep result parts and helper objects separate. Confirm that only the intended printable objects are included in the export.

Before printing:

- Check exported scale and units in the slicer.
- Confirm that all intended parts are present.
- Run a final mesh and wall-thickness check.
- Verify connector fit with a small test print.

### Panel overview

The **3D Viewport → N-panel → SnapSplit** panel provides:

#### Segmentation

- Global X/Y/Z planar splitting
- Number of parts
- Split offset and interactive adjustment
- Split preview
- Automatic seam capping
- Post-split capping and decapping tools
- Stroke-based Freehand Cut

#### Connections

- Pin, tenon, dovetail, and snap variants
- Custom mesh connectors
- Line and grid distribution
- Individual click placement
- Live Preview
- Connector/socket role swapping
- Percentage-based placement margins
- Insertion-depth control, with a default of 50%
- Type-specific dimension, taper, chamfer, span, rotation, and offset controls

#### Tolerance and alignment

- Material tolerance profiles
- Manual tolerance override
- Face-to-face alignment in Object Mode

### Languages

SnapSplit uses Blender’s translation system and follows the interface language where a matching translation is available.

The project includes translation dictionaries for:

- German
- French
- Spanish
- Italian
- Portuguese
- Dutch
- Polish
- Japanese
- Chinese
- Russian
- Ukrainian
- Turkish
- Slovenian
- Korean
- Swahili
- Arabic
- Persian
- Hindi
- Bengali

English is the source language and fallback.

Translation availability depends on the locales recognized by your Blender build and its interface translation settings. Labels without a matching translation remain in English.

To contribute a language or improve a translation, edit **`localization.py`** and open a pull request.

The current preferences panel does not include a **Reload UI Language** button.

### Add-on preferences

Open **Edit → Preferences → Add-ons → SnapSplit** to access:

- **Default Profile**
- **Create export collection**

These controls are present in the current preferences UI. However, their integration is incomplete: do not rely on them to initialize a material profile for every new file/object or to control all collection creation.

Choose the material profile directly in the SnapSplit panel and inspect the generated collections before export.

### Package structure

The installable extension ZIP contains these files at its root:

```text
snapsplit.zip
├── blender_manifest.toml
├── __init__.py
├── localization.py
├── LICENCE.txt
├── ops_align.py
├── ops_connectors.py
├── ops_freehand.py
├── ops_split.py
├── prefs.py
├── profiles.py
├── README.md
├── seam_data.py
├── ui.py
└── utils.py
```

### Changelog

#### 0.2.0

- Added a hollow-aware Freehand Cut operator with stroke-based planar preview.
- Added local material-region selection and optional seam capping.
- Added seam metadata and validated connector handling for supported Freehand seam pairs.
- Preserves the source mesh and hides the original after a successful Freehand cut.
- Repeated cutting of objects with existing SnapSplit seam metadata remains unsupported.

#### 0.1.9

- Added a toggle to swap connector and socket orientation.
- Added **S** to swap roles during click placement.
- Added automatic X-ray handling for split preview, connector Live Preview, and click placement.
- Added automatic rotation and scale application before planar splitting.
- Improved connector orientation after face alignment of non-split objects.

#### 0.1.8

- Moved face-pick storage for the alignment tool into a registered PropertyGroup.
- Cleaned up localization.

#### 0.1.7

- Migrated from key-based `tr()` translation calls to literal strings with `_trf()`.
- Centralized translation data in `localization.py`.
- Integrated translation registration with Blender.
- Improved custom connector Boolean stability.
- Replaced selected `bpy.ops` operations with RNA/BMesh API usage.
- Limited dependency-graph handler registration to active Live Preview.
- Improved error handling and orphaned-object cleanup.
- Improved the connector settings layout.
- Made changes intended to meet Blender Extensions requirements.
- Removed advertising and donation links from the add-on UI.

#### 0.1.6

- Added line/grid Live Preview for all connector types.
- Added placement margin, taper, chamfer, span, rotation, and in-plane offset controls.
- Improved splitting and seam capping for supported hollow geometry created with Boolean modifiers.

#### 0.1.5

- Added translation dictionaries covering 19 additional languages alongside English.
- Integrated language selection with Blender’s interface translation system.

#### 0.1.4

- Added dovetail and snap-dovetail connectors.
- Added custom mesh connectors with Width/Length/Depth scaling and click placement.

#### 0.1.3

- Introduced cylindrical pins, rectangular tenons, snap-pins, and snap-tenons.
- Added planar splitting with axis and offset controls.
- Added optional seam capping.
- Added line, grid, and individual click placement.
- Added material tolerance profiles.
- Added face-to-face alignment.
- Added collection organization and cleanup.

### Roadmap

Ideas for future development include:

- Complete default-profile initialization and make its scope explicit.
- Make export-collection behaviour configurable and consistent.
- Support repeated cuts through seam-metadata migration.
- Add material-boundary and wall-depth validation for Freehand connectors.
- Expand translation coverage, including newer workflow labels.
- Improve diagnostics, documentation, and automated testing.

These are development ideas, not commitments to a particular release.

### Feedback and contributions

SnapSplit is developed in my free time. Bug reports, reproducible examples, translation improvements, and focused pull requests are welcome.

For bug reports, please include:

- Your Blender version
- Your SnapSplit version
- Steps to reproduce the issue
- Relevant settings
- The error message or console output
- A minimal example file, if you can share it

You can contribute by forking the repository and opening a pull request.

Thank you for your feedback and suggestions. They help improve the workflow and make SnapSplit a more useful free tool for Blender-based 3D printing.

### Support

If SnapSplit is useful to you and you would like to support its development:

- [Support on Gumroad](https://betakontext.gumroad.com/l/snapsplit)
- [Support on Superhive](https://superhivemarket.com/products/snapsplit)
- [Buy me a coffee](https://buymeacoffee.com/betakontext)

**Contact:** dev@betakontext.de
**Website:** [dev.betakontext.de](https://dev.betakontext.de/)

### License

SnapSplit is developed with AI assistance and distributed under the **GNU General Public License, version 3 or later**.

See **`LICENCE.txt`** for the license terms.
