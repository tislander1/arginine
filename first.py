# read in the SVG file 'three boxes in libre draw.svg' as xml
import xml.etree.ElementTree as ET
import re
import networkx as nx

def rgb_to_hex(r, g, b):
    """
    Converts RGB values to a HEX color code.

    Parameters:
        r (int): Red component (0-255)
        g (int): Green component (0-255)
        b (int): Blue component (0-255)

    Returns:
        str: HEX color code in the format #RRGGBB
    """
    # Validate input ranges
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError("RGB values must be in the range 0-255.")

    # Convert to HEX and format as #RRGGBB
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

def get_boxes_and_connectors(svg_file):
    # Parse the XML file
    tree = ET.parse(svg_file)
    root = tree.getroot()
    # find any boxes in the SVG file
    # get all elements with <g class="com.sun.star.drawing.CustomShape">
     # Parse the XML file
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # find any boxes in the SVG file
    # get all elements with <g class="com.sun.star.drawing.CustomShape">
    boxes = []
    box_text = {}
    elements = root.findall(".//{http://www.w3.org/2000/svg}g[@class='com.sun.star.drawing.CustomShape']")
    # for each element, get the <g id="some id">.  If g is not None, get the x, y, width, height attributes of the <rect> element inside the <g> element
    for element in elements:
        g = element.find("{http://www.w3.org/2000/svg}g")
        if g is not None:
            id = g.get("id")
            rect = g.find("{http://www.w3.org/2000/svg}rect")
            if rect is not None:
                x_box = float(rect.get("x"))
                y_box = float(rect.get("y"))
                width_box = float(rect.get("width"))
                height_box = float(rect.get("height"))
                this_box = {"id": id, "x": x_box, "y": y_box, "width": width_box, "height": height_box}
            # check if there is a <text> element inside the <g> element
            text_elem = g.find("{http://www.w3.org/2000/svg}text")
            if text_elem is not None:
                # any test will be in the main page, not in an element
                text = "".join(text_elem.itertext())
                this_box["text"] = text
            if rect is not None and text_elem is not None:
                # get all path elements inside the <g> element.  If one of them
                # has a fill attribute that is not 'none', then get the fill attribute which will be the color of the box
                this_box["color"] = (255, 255, 255)
                paths = g.findall("{http://www.w3.org/2000/svg}path")
                for path in paths:
                    fill = path.get("fill")
                    if fill != 'none':
                        color_text = fill
                        # get the red, green, blue components of the color, which will have the form "rgb(0,169,51)"
                        match = re.match(r'rgb\((\d+),(\d+),(\d+)\)', color_text)
                        if match:
                            color = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
                            this_box["color"] = color
                        break
            boxes.append(this_box)
            box_text[id] = text


    # find any connectors in the SVG file
    # get all elements with <g class="com.sun.star.drawing.ConnectorShape">
    connectors = []
    elements = root.findall(".//{http://www.w3.org/2000/svg}g[@class='com.sun.star.drawing.ConnectorShape']")
    # for each element, get the <g id="some id">.  If g is not None, get the x1, y1, x2, y2 attributes of the <line> element inside the <g> element
    for element in elements:
        g = element.find("{http://www.w3.org/2000/svg}g")
        if g is not None:
            id = g.get("id")
            paths = g.findall("{http://www.w3.org/2000/svg}path")
            # get the first path element for which the stroke is not equal to 'none'
            for path in paths:
                stroke = path.get("stroke")
                if stroke != 'none':
                    d_stroke = path.get("d")
                else:
                    d_arrowhead = path.get("d")

            # The d attribute may look like "M 6080,4174 L 7190,4174 7190,5127 8022,5127 "/
            # or like "M 10048,6715 L 10048,7705".  We need to extract the first two numbers
            # by using a regular expression

            x1 = None
            y1 = None
            match = re.search(r'M\s*([\d.]+),([\d.]+)', d_stroke)
            if match:
                x1 = float(match.group(1))
                y1 = float(match.group(2))
            # now extract the last two numbers, which may be the beginning or the end of the arrow
            x2 = None
            y2 = None
            match = re.search(r'\s*([\d.]+),([\d.]+)\s*$', d_stroke)
            if match:
                x2 = float(match.group(1))
                y2 = float(match.group(2))
            # now get the first two numbers from the arrowhead path
            match = re.search(r'M\s*([\d.]+),([\d.]+)', d_arrowhead)
            if match:
                x_arr = float(match.group(1))
                y_arr = float(match.group(2))

            # If the arrowhead is closer to (x1, y1), then (x1, y1) is the end of the line.
            # Otherwise, it is the beginning of the line.
            dist1 = None
            dist2 = None
            if x1 is not None and y1 is not None:
                dist1 = ((x_arr - x1) ** 2 + (y_arr - y1) ** 2) ** 0.5
            if x2 is not None and y2 is not None:
                dist2 = ((x_arr - x2) ** 2 + (y_arr - y2) ** 2) ** 0.5
            if dist1 is not None and dist2 is not None and dist1 < dist2:
                # arrowhead is closer to (x1, y1), so (x1, y1) is the end of the line
                x_start = float(x2)
                y_start = float(y2)
                x_end = float(x1)
                y_end = float(y1)
            elif dist1 is not None and dist2 is not None and dist2 <= dist1:
                # arrowhead is closer to (x2, y2), so (x2, y2) is the end of the line
                x_start = float(x1)
                y_start = float(y1)
                x_end = float(x2)
                y_end = float(y2)
            else:
                # something went wrong
                x_start = None
                y_start = None
                x_end = None
                y_end = None

            if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
                connectors.append({"id": id, "start": (x_start, y_start), "end": (x_end, y_end)})
    return boxes, box_text, connectors

def get_connectivity_of_boxes(boxes, box_text, connectors):
    # Each box has an x, y, width, height
    # Each connector has an x_start, y_start, x_end, y_end and generally connects to the middle of a side of a box
    # We want to determine which boxes are connected by which connectors
    
    for box in boxes:
        box["east"] = (box["x"] + box["width"], box["y"] + box["height"] / 2)
        box["west"] = (box["x"], box["y"] + box["height"] / 2)
        box["north"] = (box["x"] + box["width"] / 2, box["y"])
        box["south"] = (box["x"] + box["width"] / 2, box["y"] + box["height"])
    # Determine which boxes are *closest* to the start and end of each connector
    G = nx.DiGraph()
    for box in boxes:
        # add the box id and text as attributes
        G.add_node(box["id"])
        G.nodes[box["id"]]['text'] = box_text.get(box["id"], "")
        G.nodes[box['id']]['id'] = box['id']
        color = box.get('color', (255, 255, 255))
        G.nodes[box['id']]['color'] = rgb_to_hex(*color)
    
    # For each connector, find the closest box to the start and end points
    # and add an edge from the start box to the end box
    # If no box is found, print a message
    for connector in connectors:
        start_box = None
        end_box = None
        min_start_dist = float('inf')
        min_end_dist = float('inf')
        for box in boxes:
            for side in ['east', 'west', 'north', 'south']:
                side_pos = box[side]
                start_dist = ((connector["start"][0] - side_pos[0]) ** 2 + (connector["start"][1] - side_pos[1]) ** 2) ** 0.5
                end_dist = ((connector["end"][0] - side_pos[0]) ** 2 + (connector["end"][1] - side_pos[1]) ** 2) ** 0.5
                if start_dist < min_start_dist:
                    min_start_dist = start_dist
                    start_box = box['id']
                if end_dist < min_end_dist:
                    min_end_dist = end_dist
                    end_box = box['id']
        if start_box is not None and end_box is not None:
            G.add_edge(start_box, end_box, id=connector["id"], )
            print(f'''Connector {connector['id']} connects {start_box} ({box_text[start_box]}) ---> {end_box} ({box_text[end_box]})''')
        else:
            print(f"Connector {connector['id']} could not be connected to boxes")
    return G

if __name__ == '__main__':
    svg_file = 'three boxes in libre draw.svg'

    boxes, box_text, connectors = get_boxes_and_connectors(svg_file)
    
    print("Boxes:")
    for box in boxes:
        print(box)
    print("Connectors:")
    for connector in connectors:
        print(connector)

    networkx_graph = get_connectivity_of_boxes(boxes, box_text, connectors)

    # save the graph to a graphml file
    nx.write_graphml(networkx_graph, "three_boxes.graphml")



    x = 2

    x = 2