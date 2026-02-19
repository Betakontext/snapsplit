# SnapSplit 

Addon for Blender to automate splitting / cutting complex 3D models, which are f.e. bigger than your printing bed, into printable parts. It generates precise, glue-free snap-fit connectors.

Its goal is to integrate into a 3D printing workflow using robust booleans, material sensible adaptive tolerance models, and various options for splits and connections.

---------------------------

For now I tested with Blender 5.0.1 and Blender 4.5.3 LTS, which both work. Please let me know if you test other Blender versions. Lets update version compatabilities.

### Installation:
- Download the whole repository or only snapsplit.zip
- In Blender: Edit → Preferences → Add-ons → Install… → select the *.ZIP → enable.

### Blender setup:
- Unit system: Metric, Unit scale: 1.000, Length: Adaptive
- The UI is accessible over the N-Panel in Blender.

### Quality assurance and error prevention:
- Scale Unit = 1.000, Metric: Adaptive
- Before splitting: use f.e. 3D-Printing Toolbox (manifold, thin walls, intersections).
- Select a watertight (manifold) mesh.
- Ctrl + A -> Apply all transforms
- This is also important after each change, f.e. rotatations or scale.
- After splitting: visually check that all parts contain polygons.

-------------------------
### Cut / Split workflow:

![SnapSplit UI](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_UI_01.png)

Unfold the segmentation part (More...) to get ready for the split.

![Segmentation](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_UI_02.png)

-> Choose desired number of parts and the asjust the split axis offset.
-> For larger part numbers you can deselect "cap seams" and create the caps afterwards
-> Push: "Adjust split axis"
-> Run "Planar Split": Multiple parts will be temporarily be created in the “_SnapSplit_Parts” collection.

-------------------------
### Build Connections:

Unfold the conections part (More...) to get ready to place connectors.

![F.e. place connections per "click"](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_connections_01.png)

-> Select two or more adjacent parts (order does not matter)
-> Choose pins or tenons distributed along a seam line or spread across a grid, with or without Snap-Pins for glueless connection.
-> Define tolerance profile (optional override) for your material.

->  Click “Add connectors”: The pin/tenon is unioned into Part B, and a socket with tolerance is cut into Part A.
or   ->  Choose "Place connectors (click)" to set individualized connectors with your mouse clicking at spots along the seems.

![F.e. place connections per "click"](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_connections_02.png)

### Export parts as usual (STL/OBJ/3MF). Tip: for 3MF, double-check scale/units.

-------------------------
-------------------------

### The panel in the 3D View (N-Panel → “SnapSplit”) features:

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

### Folder structure (inside snapsplit.zip):

    snapsplit/
        __init__.py
        ops_split.py
        ops_connectors.py
        ui.py
        prefs.py
        utils.py
        profiles.py

### Roadmap of ideas:

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
