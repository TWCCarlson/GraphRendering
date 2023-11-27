# GraphRendering
TkInter app for designing orthogonal robot workspaces

![image](https://github.com/TWCCarlson/GraphRendering/assets/72635603/4f57de71-6646-47ed-a116-70038ab86349)

# Purpose
This application was used as a jumping off point to quickly generate graphs compatible with [my thesis project](https://github.com/TWCCarlson/RoboWarehousingSim), which simulates the behaviors of fleets of agents controlled by various algorithms over the spaces designed using this application.

This application is very much a prototype and the resulting maps could be developed without GUI. See the thesis repository for documentation regarding this.

It is likely this will become obsolete and incorporated directly into the other application I have developed in the future, with an original take on the codebase.

# Usage
Either use the packaged application in /dist/VisualFloorDesigner/ or create an environment and execute the toplevel VisualFloorDesigner.py.

# License
This application is a modified version of [Tile Basic](https://multilingual-coder.github.io/tilebasic/about.html), which is distributed under the GNU General Public Licence. 
You can view the licence here: [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
If you redistribute this software, the licence requires that you:
 - Include a copy of the licence and copyright notice with the redistributed sofware.
 - State the changes you have made to the software.
 - Make the source code of the redistributed software available.
 - Distribute the software under the same licence
Accordingly, this software is also distributed under the GNU GPL v3.0 and left available.

The following alterations were made:
 - Removed features which allow inserting custom tile images (the other application expects certain input tiles)
 - Tile options were replaced with my own images
 - The output file format and datastructures used in the program were adjusted to include data for the other application I developed
 - Various UI changes which helped me learn about TkInter
