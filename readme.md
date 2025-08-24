<h1>The Arginine graph conversion tool is used to:<br>
(1) create NetworkX/GraphML networks using LibreOffice Draw.
(2) create NetworkX/GraphML networks from KeggXML.</h1>


<h2>LibreOffice Draw to GraphML</h2>
The tool can read in SVG exported by LibreOffice Draw 25.8.0.4 (X86_64) and produce a GraphML object containing a directed graph, with arrows as drawn.<br>

The following elements are supported:
- Rectangle
- Connectors --> Connector Ends With Arrow

Steps:<br>
1. In LibreOffice, draw an image using Rectangles and "Connector Ends With Arrow" elements, then export it with File --> Export --> SVG.  
2. Set the "svg_file =" line to point to the file of interest.
3. The libreoffice_draw_svg_to_graphml.py routine will extract the connectivity, rectangle text, and any fill color and export it to GraphML.

- Use these tools:<br>
<img width="287" height="84" alt="image" src="https://github.com/user-attachments/assets/e8d0c759-8ec4-4a01-8295-183ba1b9aee3" /><br>
<img width="213" height="249" alt="image" src="https://github.com/user-attachments/assets/314b2c24-e060-4449-b25a-b6e23b2b8be7" /><br>

- Make a drawing in LibreOffice Draw:<br>
<img width="338" height="435" alt="image" src="https://github.com/user-attachments/assets/f0bf4af6-f8f1-4b9e-b6dd-d0e990f2afcd" />

- GraphML visualization in Cytoscape (in yFiles Hierarchical view):<br>
<img width="791" height="807" alt="image" src="https://github.com/user-attachments/assets/9bdba614-8483-42c1-a596-89d2174bf556" />

<h2>KeggXML to GraphML</h2>

Steps:
1. Set the 'kegg_xml_file = ' line to point to the file of interest.
2. The kegg_xml_to_graphml.py routine will extract the connectivity, assign colors, and export it to GraphML.



