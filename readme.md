This conversion tool is used to create GraphML networks using LibreOffice Draw.

Read in SVG exported by LibreOffice Draw 25.8.0.4 (X86_64)
Can read elements:
- Rectangle
- Connectors --> Connector Ends With Arrow

In LibreOffice, draw an image using Rectangles and "Connector Ends With Arrow" elements, then export it with File --> Export --> SVG.  
Set the "svg_file =" to point to the file of interest.
The routine will extract the connectivity, rectangle text, and any fill color and export it to GraphML.
This file type represents the network, and can be read by networkx and Cytoscape.

- Use these tools:<br>
<img width="287" height="84" alt="image" src="https://github.com/user-attachments/assets/e8d0c759-8ec4-4a01-8295-183ba1b9aee3" /><br>
<img width="213" height="249" alt="image" src="https://github.com/user-attachments/assets/314b2c24-e060-4449-b25a-b6e23b2b8be7" /><br>

- Make a drawing in LibreOffice Draw:<br>
<img width="338" height="435" alt="image" src="https://github.com/user-attachments/assets/f0bf4af6-f8f1-4b9e-b6dd-d0e990f2afcd" />

- GraphML visualization in Cytoscape (in yFiles Hierarchical view):<br>
<img width="791" height="807" alt="image" src="https://github.com/user-attachments/assets/9bdba614-8483-42c1-a596-89d2174bf556" />



