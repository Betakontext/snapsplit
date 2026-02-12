This is a first version of “SnapSplit”.
An add-on for Blender that automates splitting complex 3D models into printable parts and generates precise, glue-free snap-fit connectors.
Its goal is to integrate into a 3D printing workflow (tolerances, alignment, build volume, support avoidance) and uses robust booleans, adaptive tolerance models, and printer/material profiles.
---------------------------
Until now I tested it with Blender 5.0.1 and Blender 4.5.3 LTS, which both work. 
Let me know if you test it on another Blender version, to update Version compatability.

Blender setup:  

    Unit scale: 1.000, Millimeters

Installation:
    -> Download snapsplit.zip
    -> In Blender: Edit → Preferences → Add-ons → Install… → select the ZIP → enable.

Split:
    - Select a watertight (manifold) mesh.
    - Apply scale (Ctrl+A → Scale).
    - Scale Unit 1.000, Millimeters
    - N-Panel → SnapSplit:
        Choose desired number of parts and split axis.
        Run Planar Split. Multiple parts will be created in the “_SnapSplit_Parts” collection.

Connect:
    - Select two or more adjacent parts (order does not matter).
    - Choose connector type and tolerance profile (optional override).
    -> Click “Add Connectors”.

Pins/tenons are distributed along a seam line or spread across a grid on the seam surface: The pin/tenon is unioned into Part A, and a socket with tolerance is cut into Part B.

Export parts as usual (STL/OBJ/3MF). Tip: for 3MF, double-check scale/units.

Quality assurance and error prevention:
    - Before splitting: use f.e. 3D-Printing Toolbox (manifold, thin walls, intersections).
    - After splitting: visually check that all parts contain polygons.
    - If booleans fail: try a moderate voxel remesh, remove doubles, recalc normals.
    - Scaling: Work in mm values; the add-on converts correctly to Blender’s internal meters.

-------------------------

For now the add-on includes:

    Panel in the 3D View (N-Panel → “SnapSplit”)

    Property group with:
        Number of parts (e.g., 2–8)
        Connector type (Cylindrical Pin, Rectangular Tenon)
        Material/Printer profile (PLA, PETG, ABS, ASA, TPU, SLA)
        Derived tolerances (per side)

    Operators:
        Planar Split along a global axis into the specified number of parts
        Grid Split on the cut face with rows and columns input
        Percentage-based edge margin for connector placement
        Adjustable insertion depth. Default: 50%
        Automatic placement and generation of connectors

    Tolerance profiles (guidelines, adjustable):

        PLA: 0.15–0.25 mm per side
        PETG: 0.25–0.35 mm per side
        ABS/ASA: 0.20–0.30 mm per side
        TPU: 0.30–0.45 mm per side
        SLA: 0.05–0.15 mm per side

    These are provided as presets and can be overridden by the user.

---------------------------

Limitations and thoughts for next steps:
    The current Planar Split uses heuristics and large cutter bodies. For highly complex geometry, occasional manual cleanup may be helpful.
    Connectors are currently placed along a coarse midline or into a grid across the seam surface.

Future versions can add free-form seams, bayonet locks, dovetails, magnet pockets, support-aware features, etc.

Roadmap of ideas:
    Determine seam curves precisely
    Overhang/wall-thickness–aware placement
    Automatic anti-rotation combinations
    Freeform/curvature-based seams
    Calibration wizard for more accurate tolerances
    Export operator (3MF with metadata)
    QA panel (manifold/wall-thickness checks)
    Bayonet/dovetail connectors
    A calibration wizard for tolerances
    SLA models may require vent holes in sockets.

---------------------------

For development:

Necessary folder structure (inside snapsplit.zip):

    snapsplit/
        __init__.py
        ops_split.py
        ops_connectors.py
        ui.py
        prefs.py
        utils.py
        profiles.py

---------------------------

The project is made with AI assistance (GPT 5) and under the MIT license.
If you want to contribute, fork and explore the code. Have fun splitting and printing.
CONTACT: info@betakontext.de
