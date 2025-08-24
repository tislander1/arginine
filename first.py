# read in the SVG file 'three boxes in libre draw.svg' as xml
import xml.etree.ElementTree as ET
import re
import networkx as nx

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
                boxes.append({"id": id, "x": x_box, "y": y_box, "width": width_box, "height": height_box})


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
                connectors.append({"id": id, "x_start": x_start, "y_start": y_start, "x_end": x_end, "y_end": y_end})
    return boxes, connectors

def get_connectivity_of_boxes(boxes, connectors):
    pass

if __name__ == '__main__':
    svg_file = 'three boxes in libre draw.svg'

    boxes, connectors = get_boxes_and_connectors(svg_file)
    
    print("Boxes:")
    for box in boxes:
        print(box)
    print("Connectors:")
    for connector in connectors:
        print(connector)

    get_connectivity_of_boxes(boxes, connectors)



    x = 2

    x = 2