import ifcopenshell
import ifcopenshell.geom

import os
import math
import itertools

import OCC.gp, OCC.BRepBuilderAPI, OCC.BRepAlgoAPI, OCC.TopExp, OCC.ShapeAnalysis, OCC.BRep, OCC.GeomAPI

section_plane = OCC.gp.gp_Pln(
        OCC.gp.gp_Pnt(0, 0, 4),
        OCC.gp.gp_Dir(0, 0, 1)
    )

s1 = ifcopenshell.geom.settings()
s1.set(s1.SEW_SHELLS, True)
s1.set(s1.USE_PYTHON_OPENCASCADE, True)

s2 = ifcopenshell.geom.settings()
s2.set(s2.SEW_SHELLS, True)
s2.set(s2.USE_PYTHON_OPENCASCADE, True)
s2.set(s2.INCLUDE_CURVES, True)

s3 = ifcopenshell.geom.settings()
s3.set(s3.SEW_SHELLS, True)
s3.set(s3.USE_PYTHON_OPENCASCADE, True)
s3.set(s3.INCLUDE_CURVES, True)
s3.set(s3.EXCLUDE_SOLIDS_AND_SURFACES, True)

section_face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(section_plane, -10, 50, -10, 50).Face()

def get_verts(w):
    exp = OCC.TopExp.TopExp_Explorer(w, OCC.TopAbs.TopAbs_EDGE)
    last = None
    i = 0
    while exp.More():
        # print ('edge', i)
        i += 1
        exp2 = OCC.TopExp.TopExp_Explorer(exp.Current(), OCC.TopAbs.TopAbs_VERTEX)
        v1 = OCC.TopoDS.topods_Vertex(exp2.Current())
        exp2.Next()
        v2 = OCC.TopoDS.topods_Vertex(exp2.Current())
        if exp.Current().Orientation() == 0:
            vs = [v1, v2] if i == 1 else [v2]
        else:
            vs = [v2, v1] if i == 1 else [v1]
        for v in vs:            
            p = OCC.BRep.BRep_Tool.Pnt(v)
            c = p.X(), p.Y()
            yield c
            # if last != c:
            #     yield c
            # last = c
            # exp2.Next()
        exp.Next()
        
def get_3d_verts(w):
    exp = OCC.TopExp.TopExp_Explorer(w, OCC.TopAbs.TopAbs_VERTEX)
    last = None
    while exp.More():
        v = OCC.TopoDS.topods_Vertex(exp.Current())
        p = OCC.BRep.BRep_Tool.Pnt(v)
        c = p.X(), p.Y(), p.Z()
        if last != c:
            yield c
        last = c
        exp.Next()
        
def get_3d_bounds(it):
    ab = [1e9,1e9,1e9], [-1e9,-1e9,-1e9]
    for xyz in it:
        for c, f in zip(ab, (min, max)):
            for i in range(3):
                c[i] = f(c[i], xyz[i])
    return ab

def get_center(bb):
    return tuple(map(lambda a,b: (a+b)/2., *bb))
        
def bounds(pts):
    a,b,c,d = 1e9, 1e9, -1e9, -1e9
    for pt in pts:
        a = min(a, pt[0])
        b = min(b, pt[1])
        c = max(c, pt[0])
        d = max(d, pt[1])
    return [(a,b),(a,d),(c,b),(c,d)]

def bounds_min(pts):
    a,b,c,d = 1e9, 1e9, -1e9, -1e9
    for pt in pts:
        a = min(a, pt[0])
        b = min(b, pt[1])
        c = max(c, pt[0])
        d = max(d, pt[1])
    return a,b,c,d

def bounds_lines(ptss):
    a,b,c,d = 1e9, 1e9, -1e9, -1e9
    for pts in ptss:
        for pt in pts:
            a = min(a, pt[0])
            b = min(b, pt[1])
            c = max(a, pt[0])
            d = max(b, pt[1])
    return [(a,b),(a,d),(c,b),(c,d)]

def dist(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def dist3(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2)
        
class coord_extractor:
    def __init__(self, fn, gf=None, wf=None, group_lines=True):
        self.f = ifcopenshell.open(fn)
        self.group_lines = group_lines
        if gf:
            self.gf = ifcopenshell.open(gf)
            self.calc_grid_pts()
        if wf:
            self.wf = ifcopenshell.open(wf)
            self.calc_opening_centers()
    def calc_opening_centers(self):
        
        self.openings = []
        
        for o in self.wf.by_type('IfcOpeningElement'):
            shp = ifcopenshell.geom.create_shape(s1, o).geometry
            self.openings.append((get_center(get_3d_bounds(get_3d_verts(shp))), o))
        
    def calc_grid_pts(self):
        
        def generate_grid_edges():
            for g in self.gf.by_type('IfcGrid'):
                shp = ifcopenshell.geom.create_shape(s2, g).geometry
                exp = OCC.TopExp.TopExp_Explorer(shp, OCC.TopAbs.TopAbs_EDGE)
                while exp.More():
                    # v.display(shp, color=(0.,0.,0.))
                    yield OCC.BRep.BRep_Tool.Curve(OCC.TopoDS.topods_Edge(exp.Current()))[0]
                    exp.Next()

        def generate_grid_x_points():
            edges = list(generate_grid_edges())
            for a, b in itertools.permutations(edges, 2):
                x = OCC.GeomAPI.GeomAPI_ExtremaCurveCurve(a, b)
                d = x.LowerDistance()
                if d < 1e-9:
                    p1, p2 = OCC.gp.gp_Pnt(), OCC.gp.gp_Pnt()
                    x.NearestPoints(p1, p2)
                    yield p1.X(), p1.Y()
                    
        self.gps = sorted(generate_grid_x_points())
                    
    def focus(self, guid):
        elem = self.f[guid]
        shp = ifcopenshell.geom.create_shape(s1, elem).geometry
        own_vertices = bounds(set(get_verts(shp)))
        
        center_3d = get_center(get_3d_bounds(get_3d_verts(shp)))
        closest_opening = None
        closest_opening_dist = 1e9
        for c, o in self.openings:
            d = dist3(center_3d, c)
            if d < closest_opening_dist:
                closest_opening_dist, closest_opening = d, o
                
        elem2 = closest_opening.VoidsElements[0].RelatingBuildingElement
        shp = ifcopenshell.geom.create_shape(s1, elem).geometry
        elem2_v = bounds(set(get_verts(shp)))
        
        wall_axis = ifcopenshell.geom.create_shape(s3, elem2).geometry
        exp = OCC.TopExp.TopExp_Explorer(wall_axis, OCC.TopAbs.TopAbs_EDGE)
        while exp.More():
            edge = OCC.TopoDS.topods_Edge(exp.Current())
            wall_axis_crv = OCC.BRep.BRep_Tool.Curve(edge)[0]
            break

        def find_closest(other_vertices):
            min_dist = 1e9
            closest_pt = None
            for a,b in itertools.product(own_vertices, other_vertices):
                d = dist(a,b)
                if d > 1.e-9 and d < min_dist:
                    min_dist = d
                    closest_pt = a, b
            return closest_pt
        
        def project_onto(pt2d):
            p = OCC.gp.gp_Pnt(pt2d[0], pt2d[1], 0.)
            sas = OCC.ShapeAnalysis.ShapeAnalysis_Curve()
            proj = OCC.gp.gp_Pnt()
            r = 1.
            u = sas.Project(wall_axis_crv, p, 1.e-3, proj, r)
            return proj.X(), proj.Y()
        
        def get_ortho(pt2d):
            p = OCC.gp.gp_Pnt(pt2d[0], pt2d[1], 0.)
            sas = OCC.ShapeAnalysis.ShapeAnalysis_Curve()
            proj = OCC.gp.gp_Pnt()
            r = 1.
            u = sas.Project(wall_axis_crv, p, 1.e-3, proj, r)
            pp = OCC.gp.gp_Pnt()
            pv = OCC.gp.gp_Vec()
            # probably `u`  is incorrect, but does not matter for lines
            wall_axis_crv.GetObject().D1(u[0], pp, pv)
            return -pv.Y(), pv.X()
        
        def project_line(pts):
            pp1, pp2 = map(project_onto, pts)
            return pp1, pp2
            # Nicer to have both annotations on the same line... ^ 
            dx, dy = pp2[0] - pp1[0], pp2[1] - pp1[1]
            return pts[0], (pts[0][0] + dx, pts[0][1] + dy)
        
        def move_line(p):
            d1 = get_ortho(p[0])
            def add(pt):
                return pt[0] + d1[0] * 0.2, pt[1] + d1[1] * 0.2
            return list(map(add, p))
        
        self.annotation_lines = list(map(move_line, map(project_line, (find_closest(elem2_v), find_closest(self.gps)))))
        return bounds_min(own_vertices + sum(self.annotation_lines, []))
    
    def get_annotations(self):
        return self.annotation_lines
    
    def extract(self, ty):
        for p in self.f.by_type(ty):
            
            # if p.GlobalId != '1lNGjNoS5E5wxG5QA5o0PB': continue
            
            if p.Representation:
                is_solid = not p.is_a("IfcGrid")
                s = s1 if is_solid else s2
                shp = ifcopenshell.geom.create_shape(s, p).geometry

                if is_solid:
                    
                    # print(p)
                    
                    exps = OCC.TopExp.TopExp_Explorer(shp, OCC.TopAbs.TopAbs_SHELL)
                    while exps.More():
                        # print('shell')
                        shl = OCC.TopoDS.topods_Shell(exps.Current())
                        exps.Next()
                    
                        def generate_edges():
                            section = OCC.BRepAlgoAPI.BRepAlgoAPI_Section(section_face, shl).Shape()
                            exp = OCC.TopExp.TopExp_Explorer(section, OCC.TopAbs.TopAbs_EDGE)
                            while exp.More():
                                yield OCC.TopoDS.topods_Edge(exp.Current())
                                exp.Next()

                        if self.group_lines:

                            edges = OCC.TopTools.TopTools_HSequenceOfShape()
                            edges_handle = OCC.TopTools.Handle_TopTools_HSequenceOfShape(edges)

                            wires = OCC.TopTools.TopTools_HSequenceOfShape()
                            wires_handle = OCC.TopTools.Handle_TopTools_HSequenceOfShape(wires)

                            for edge in generate_edges():
                                # print(edge)
                                edges.Append(edge)

                            OCC.ShapeAnalysis.ShapeAnalysis_FreeBounds.ConnectEdgesToWires(edges_handle, 1e-5, True, wires_handle)
                            wires = wires_handle.GetObject()

                            for i in range(1, wires.Length() + 1):
                                w = wires.Value(i)
                                yield list(get_verts(w))

                        else:
                            for edge in generate_edges(): 
                                yield list(get_verts(edge))

                else:
                    exp = OCC.TopExp.TopExp_Explorer(shp, OCC.TopAbs.TopAbs_EDGE)
                    while exp.More():
                        edge = OCC.TopoDS.topods_Edge(exp.Current())
                        yield list(get_verts(edge))
                        exp.Next()

