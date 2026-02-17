Addon for Blender that automates splitting / cutting complex 3D models into printable parts and generates precise, glue-free snap-fit connectors.

Its goal is to integrate into a 3D printing workflow and uses robust booleans, adaptive tolerance models, and printer/material profiles.

---------------------------
---------------------------

For now I tested it with Blender 5.0.1 and Blender 4.5.3 LTS, which both work. Please let me know if you test it on other Blender versions. Lets update version compatabilities.

Installation:
    -> Download snapsplit.zip
    -> In Blender: Edit → Preferences → Add-ons → Install… → select the ZIP → enable.

Blender setup:
    *   Unit system: Metric, Unit scale: 1.000, Length: Adaptive

Quality assurance and error prevention:
    - Scaling: Work in mm values; the add-on converts correctly to Blender’s internal meters.
    - Before splitting: use f.e. 3D-Printing Toolbox (manifold, thin walls, intersections).
    - Ctrl + A -> Apply all transforms = important if you f.e. rotate or change the size the object.
    - After splitting: visually check that all parts contain polygons.
    - Scaling: Work in mm values; the add-on converts correctly to Blender’s internal meters.

-------------------------
-------------------------

Cut / Split workflow:

    - Select a watertight (manifold) mesh.
    - Apply all transformations (Ctrl+A → All transforms).
    - Scale Unit = 1.000, Millimeters
    - N-Panel → SnapSplit:
        Choose desired number of parts and split axis.
    - for larger part numbers you can deselect "cap seams" and create the caps afterwards
    - Set an individualized split axis per mousewheel or offset adjustment
    - Adjust split axis

    -> Run "Planar Split".

    Multiple parts will be created in the “_SnapSplit_Parts” collection.

Build Connections:

    Pins/tenons are distributed along a seam line or spread across a grid on the seam surface: The pin/tenon is unioned into Part A, and a socket with tolerance is cut into Part B.

    Select two or more adjacent parts (order does not matter) and choose connector type and tolerance profile (optional override).

    ->  Click “Add Connectors”.

    or

    ->  Choose "Place connectors (click)"
        to set individualized connectors with your mouse clicking at spots along the seems.

Export parts as usual (STL/OBJ/3MF). Tip: for 3MF, double-check scale/units.

-------------------------
-------------------------

The panel in the 3D View (N-Panel → “SnapSplit”) features:

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
---------------------------

If you want to contribute, fork and explore the code.

Necessary folder structure (inside snapsplit.zip):

    snapsplit/
        __init__.py
        ops_split.py
        ops_connectors.py
        ui.py
        prefs.py
        utils.py
        profiles.py

Roadmap of ideas:

    Determine seam curves precisely
    Overhang/wall-thickness–aware placement
    Automatic anti-rotation combinations
    Freeform/curvature-based seams
    Export operator (3MF with metadata)
    QA panel (manifold/wall-thickness checks)
    Bayonet/dovetail connectors
    A calibration wizard for tolerances
    SLA models may require vent holes in sockets
    Support-aware features, etc.

---------------------------
---------------------------

The project is made with AI assistance and under the terms of the GNU General Public License.

Have fun splitting and printing.

CONTACT: Christoph Medicus | dev@betakontext.de
