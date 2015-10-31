
# coding: utf-8

# In[7]:

# Writing and viewing svg files
import svgwrite

import get_coords

from annotations import drawDimension, drawGridBubbles


def lines(dwg, polygons):
    # Scale polygons
    scaledPolygons = []
    for polygon in polygons:
        scaledPolygon = []
        for coordinate in polygon:
            x = coordinate[0]
            y = coordinate[1]
            scaledPolygon.append((x * 100, y * 100))

        scaledPolygons.append(scaledPolygon)

    # Create svg polygons
    for polygon in scaledPolygons:
        #svgPolygon = svgwrite.shapes.Polygon(polygon, fill='none', stroke='none')
        drawDimension(dwg, polygon)
        #dwg.add(svgPolygon)

def read(dwg, *args, **kwargs):
    # xtractor = get_coords.coord_extractor('models/Test woning grid.ifc')
    xtractor = get_coords.coord_extractor(*args[:-1], **kwargs)
    # polygons = list(xtractor.extract("IfcGrid"))
    polygons = list(xtractor.extract(args[-1]))

    # Writing to SVG
    #dwg = svgwrite.Drawing('test.svg', width="210mm")

    # Find scaling parameters

    maxX = float("-inf")
    minX = float("inf")
    maxY = float("-inf")
    minY = float("inf")

    for polygon in polygons:
        """
        for p in polygon:
            print("(%.1f, %.1f)" % p, end="")
        print()
        """
        for coordinate in polygon:
            x = coordinate[0]
            y = coordinate[1]        

            maxX = max(maxX,x)
            maxY = max(maxY,y)
            minX = min(minX,x)
            minY = min(minY,y)


    # Scale polygons
    scaledPolygons = []
    for polygon in polygons:
        scaledPolygon = []
        for coordinate in polygon:
            x = coordinate[0]
            y = coordinate[1]
            scaledPolygon.append((x * 100, y * 100))

        scaledPolygons.append(scaledPolygon)

    # Create svg polygons
    for polygon in scaledPolygons:
        #if(kwargs == 'IfcGrid'):
        svgPolygon = svgwrite.shapes.Polygon(polygon, fill='none', stroke='black')
        dwg.add(svgPolygon)

    # Set viewbox based on scaling
    dwg.viewbox(minX * 100, minY * 100, 100 * (maxX - minX), 100 * (maxY - minY))

    return xtractor

def readGrids(dwg, *args, **kwargs):
    # xtractor = get_coords.coord_extractor('models/Test woning grid.ifc')
    xtractor = get_coords.coord_extractor(*args[:-1], **kwargs)
    # polygons = list(xtractor.extract("IfcGrid"))
    polygons = list(xtractor.extract(args[-1]))

    # Writing to SVG
    #dwg = svgwrite.Drawing('test.svg', width="210mm")

    # Find scaling parameters

    maxX = float("-inf")
    minX = float("inf")
    maxY = float("-inf")
    minY = float("inf")

    for polygon in polygons:
        """
        for p in polygon:
            print("(%.1f, %.1f)" % p, end="")
        print()
        """
        for coordinate in polygon:
            x = coordinate[0]
            y = coordinate[1]        

            maxX = max(maxX,x)
            maxY = max(maxY,y)
            minX = min(minX,x)
            minY = min(minY,y)


    # Scale polygons
    scaledPolygons = []
    for polygon in polygons:
        scaledPolygon = []
        for coordinate in polygon:
            x = coordinate[0]
            y = coordinate[1]
            scaledPolygon.append((x * 100, y * 100))

        scaledPolygons.append(scaledPolygon)

    # Create svg polygons
    for polygon in scaledPolygons:
        svgPolygon = base_line = dwg.polyline([polygon[0], polygon[len(polygon)-1]], stroke='black', style='stroke-dasharray:15, 10, 5, 10; stroke-width:0.5')
        dwg.add(svgPolygon)

    # Set viewbox based on scaling
    dwg.viewbox(minX * 100, minY * 100, 100 * (maxX - minX), 100 * (maxY - minY))

    return xtractor


def center(dwg, minX, minY, maxX, maxY):
    minX -= 1
    maxX += 1
    minY -= 1
    maxY += 1
    dwg.viewbox(minX * 100, minY * 100, 100 * (maxX - minX), 100 * (maxY - minY))



