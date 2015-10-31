
# coding: utf-8

# In[29]:

#drawAnnotation
import svgwrite, math
from svgwrite import cm, mm  
from math import atan2,degrees, sqrt

def getAngleOfLineBetweenTwoPoints(p1, p2): 
    xDiff = p2[0] - p1[0] 
    yDiff = p2[1] - p1[1] 
    return degrees(atan2(yDiff, xDiff))

def getDistanceBetweenPoints(p1, p2):
    pass

def drawDimension(dwg, anchor_points):
    text_offset=-2
    distance = sqrt( (anchor_points[len(anchor_points)-1][0] - anchor_points[0][0])**2 + (anchor_points[len(anchor_points)-1][1] - anchor_points[0][1])**2 ) 
    distance = round(distance, 2)
    if(distance < 1):
        return
    
    text_value = str(distance)#'sqrt((x2-x1)2 + (y2-y1)2)'
    
    dimension = dwg.add(dwg.g(id='base_line', stroke='black', fill='white', stroke_width=0.1))
    
    #create MidPoint
    mid_point_x = ( anchor_points[0][0] + anchor_points[len(anchor_points)-1][0] ) / 2
    mid_point_y = ( anchor_points[0][1] + anchor_points[len(anchor_points)-1][1] ) / 2
    
    #create Rect Marker
    marker_size = 60
    marker = dwg.marker(insert=(marker_size/8, marker_size/2), size=(marker_size,marker_size), orient='auto', markerUnits="strokeWidth")
    marker.add(dwg.rect(insert=(0, 0), size=(marker_size/8, marker_size), fill='black', stroke_width=0))
    dwg.defs.add(marker)
    
    #create Text Marker
    #text_marker = dwg.marker(insert=(0, text_offset), size=(100,100), orient='auto')
    #text_marker.add(dwg.text(text_value, insert=(0, text_offset), style='font:100pt; overflow:visible'))
    #dwg.defs.add(text_marker)

    #create Polyline with 3 points
    base_line = dwg.polyline([anchor_points[0], (mid_point_x, mid_point_y), anchor_points[len(anchor_points)-1]])
    
    #assign Markers
    base_line['marker-start'] = marker.get_funciri()
    #base_line['marker-mid'] = text_marker.get_funciri()
    base_line['marker-end'] = marker.get_funciri()
    
    angle = getAngleOfLineBetweenTwoPoints(anchor_points[len(anchor_points)-1], anchor_points[0] )
    rotation_angle = 'rotate(' + str(angle) + ',' + str(mid_point_x) + ',' + str(mid_point_y+text_offset) + ')'
    dimension.add(base_line)
    dimension.add(dwg.text(text_value, insert=(mid_point_x - 5, mid_point_y+text_offset), transform=rotation_angle, style='font-size:6; stroke-width:0.5; fill:black; text-anchor:center') )  
    
    #save svg image
    #dwg.save()


def drawGridBubbles(dwg, anchor_points, text_value, text_size):
    grid_bubbles = dwg.add(dwg.g(id='base_line', stroke='black', fill='white', stroke_width=0.5))

    #create Bubble Marker
    marker_size = 120
    bubble_marker = dwg.marker(insert=(marker_size/2,marker_size/2), size=(marker_size,marker_size), orient='auto')
    bubble_marker.add(dwg.circle((marker_size/2, marker_size/2), r=marker_size/2-marker_size/5, fill='white', stroke='black'))
    dwg.defs.add(bubble_marker)
    
    #create Polyline
    base_line = dwg.polyline([anchor_points[0], anchor_points[len(anchor_points)-1]], stroke='black', style='stroke-dasharray:15, 10, 5, 10')
    
    #assign Markers
    base_line['marker-start'] = bubble_marker.get_funciri()
    base_line['marker-end'] = bubble_marker.get_funciri()
   
    rotation_angle='rotate(0)'

    grid_bubbles.add(base_line)
    grid_bubbles.add(dwg.text(text_value,insert=(anchor_points[0][0]-text_size,anchor_points[0][1]+text_size/2), transform=rotation_angle, style='font-size:15; stroke_width:0; text-anchor:left'))
    grid_bubbles.add(dwg.text(text_value,insert=(anchor_points[len(anchor_points)-1][0]-text_size,anchor_points[len(anchor_points)-1][1]+text_size/2), transform=rotation_angle, style='font-size:15; stroke_width:0; text-anchor:center'))
    #save svg image
    #dwg.save()

