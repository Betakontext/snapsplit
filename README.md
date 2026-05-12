# SnapSplit

Addon for Blender to automate cut and connection building workflows for complex 3D models, which are f.e. larger than your printing bed, to create printable parts. It generates precise, glue-free snap-fit connectors.

Its goal is to integrate into a 3D printing workflow using robust booleans, material sensible adaptive tolerance models, and various options for splits and connections.

---------------------------

For now I tested it with Blender 4.5.3 LTS, 4.5.9 LTS, 5.0.1, 5.1.0 and 5.1.1 which work fine. Please let me know if you test on other Blender versions to update version compatabilities.

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

Unfold the segmentation part (More...) to get ready for the split.

![SnapSplit UI](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_UI_02.png?cache=1)
![SnapSplit UI](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_UI_01.png?cache=1)

-> Click "Show split preview" if you want to see the split preview plane permanently. Offset 0 is the middle of the selected part.

![F.e. Segmentation](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_SEG_01.png?cache=1)

-> Choose desired number of parts and adjust the split axis offset.
-> Push: "Adjust split axis"

-> For larger part numbers you can deselect "cap seams" and create the caps afterwards.
-> Cap seams closes walls, if hollow or solidify is detected. If none it closes the whole cut area. You can also use it per part afterwards if "Cap seams" is deselected


-> Run "Planar Split"

![F.e. Cap seams if hollow](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_SEG_02.png?cache=1)

-------------------------
### Build Connections:

![SnapSplit UI](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_UI_03.png?cache=1)

Unfold the conections part (More...) to choose and place your connectors.

![F.e. place connections per "click"](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_CON_01.png?cache=1)

-> Select two or more adjacent parts (order does not matter).
-> Choose pins or tenons distributed along a seam line or spread across a grid, with or without Snap-Pins for glueless connection.
-> Define your tolerance profile (under Connections UI) for your material.

![F.e. place connections per "click"](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_CON_02.png?cache=1)

->  Click “Add connectors”: The pin/tenon is unioned into Part B, and a socket with tolerance is cut into Part A.
or   ->  Choose "Place connectors (click)" to set individualized connectors with your mouse clicking at spots along the seems.

![F.e. place connections per "click"](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_CON_03.png?cache=1)

### Export parts as usual (STL/OBJ/3MF). Tip: for 3MF, double-check scale/units.

-------------------------
-------------------------

### The panel in the 3D View (N-Panel → “SnapSplit”) features:

Property group with:

- Segmentation: Number of parts. Unclick "cap seams" for larger part numbers
- Connections:  Cylindrical Pin, Rectangular Tenon, Snap-Pin, Snap-Tenon 
- Tolerance:    Material profiles (PLA, PETG, ABS, ASA, TPU, SLA)
- Alignment:    Face to face alignment option in object mode


Operators:

- Planar Split along a global axis into the specified number of parts
- Split preview and adjustment
- Decap and cap seams toggle, pre and post split
- Percentage-based edge margin for connector placement
- Seam line connectors, Grid connectors with rows and columns input and individual per click connectors placement on the cut face.
- Pin and Snap-Pin adjustments
- Adjustable insertion depth. Default: 50%
- Alignment with face selection in object mode

Tolerance profiles (guidelines, adjustable):

![SnapSplit UI](https://dev.betakontext.de/snapsplit/img/betakontext_snapsplit_UI_04.png?cache=1)

- PLA: 0.15–0.25 mm per side
- PETG: 0.25–0.35 mm per side
- ABS/ASA: 0.20–0.30 mm per side
- TPU: 0.30–0.45 mm per side
- SLA: 0.05–0.15 mm per side

Tolerances are provided as presets and can be overridden by the user.

---------------------------
---------------------------

### Folder structure (files inside snapsplit.zip):

    ├── blender_manifest.toml
    ├── __init__.py
    ├── LICENCE.txt
    ├── ops_connectors.py
    ├── ops_split.py
    ├── prefs.py
    ├── profiles.py
    ├── README.md
    ├── ui.py
    └── utils.py

---------------------------
---------------------------

### Roadmap of ideas:

-> Planing to add more connector types: f.e. Bayonet/dovetail connectors, ball-and-socket joints ...

If you want to join the development, fork and explore the code.



The project is made with AI assistance and under the terms of the GNU General Public License.

Please try it out. 

If you like SnapSplit and continue using it

-> buy me a drink on Gumroad: https://betakontext.gumroad.com/l/snapsplit

-> and/or support me on Superhive: https://superhivemarket.com/products/snapsplit

-> or buy me a coffee on Buymeacoffee: https://buymeacoffee.com/betakontext

Actually I'm happy for any feedback, f.e. your further needs and and options for next versions, or/and better connection building experiences. 

Have fun splitting and printing, and feel free to fork and join in to further developments.

CONTACT: dev@betakontext.de | https://dev.betakontext.de

