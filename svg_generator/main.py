import os
import sys

import svgwrite
import ifcopenshell

import extract_geom

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Create a an empty SVG drawing
dwg_main = svgwrite.Drawing('layout.svg')

# Overlay two drawings
for i in range(2):

    dwg = svgwrite.Drawing('test.svg')
    
    extract_geom.read(dwg, 'models/Stelkozijn 1st floor.ifc', 'IfcProduct')
    window_plotter = extract_geom.read(dwg, 'models/Windows 1st floor.ifc', 'models/Test woning grid.ifc', 'models/Walls 1st floor.ifc', 'IfcWindow', group_lines=False)
    extract_geom.read(dwg, 'models/Walls 1st floor sep.ifc', 'IfcWall')
    extract_geom.readGrids(dwg, 'models/Test woning grid.ifc', 'IfcGrid')

    if i == 0:
        # First time, zoom onto highlighted element
        
        guid = sys.argv[-1]
        if '-' in guid:
            # Uncompressed guid
            ifcopenshell.guid.compress(guid.replace('-',''))

        rect = window_plotter.focus(guid)
        extract_geom.center(dwg, *rect)
        extract_geom.lines(dwg, window_plotter.get_annotations())
    else:
        # Second time provide overview drawing
        dwg.add(svgwrite.shapes.Rect(stroke='red',fill='none',insert=(rect[0]*100-5, rect[1]*100-5), size=((rect[2]-rect[0])*100+10, (rect[3]-rect[1])*100+10)))
        
    dwg_main.add(dwg)

# Display zoom area
dwg_main.add(svgwrite.shapes.Rect(stroke='red',fill='none',insert=(rect[0]*100-5, rect[1]*100-5), size=((rect[2]-rect[0])*100+10, (rect[3]-rect[1])*100+10)))

# Write SVG to stdout
print(dwg_main.tostring())
