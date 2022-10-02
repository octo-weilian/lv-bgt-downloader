from . import *
import ezdxf
from ezdxf.math import ConstructionArc
from app.stufgeo import parser
from app.stufgeo.parser import rotation2degree,cleanup,get_labels

class StufgeoCAD:
    def __init__(self,input_xml):
        self.input_xml = input_xml
        self.imgeo_objects = etree.iterparse(input_xml,huge_tree=True,tag=IMGEO_OBJ)
        self.doc = ezdxf.new(units=1)
        self.msp = self.doc.modelspace()

    def gen_labels(self,element):
        texts,rotations,points,_ = get_labels(element)
        for i in range(len(points)):
            yield texts[i],rotation2degree(float(rotations[i])),points[i]

    def draw_arc(self,arc_coords):
        p1,arc_pos,p2 = arc_coords
        arc_orient = (arc_pos[0]-p1[0])*(p2[1]-p1[1]) - (arc_pos[1]-p1[1])*(p2[0]-p1[0])
        ccw = True 
        if arc_orient<0:
            ccw = False
        return ConstructionArc.from_3p(p1,p2,arc_pos,ccw=ccw)

    def build_cad(self):
        for _,el in self.imgeo_objects:
            entity_type = el.attrib[STUFGEO_ENT_TYPE]

            label_attributes = {"layer":entity_type,"height":1}
            object_attributes = {"layer":entity_type}
            
            if (imgeo_geom:=el.xpath(XP_GEOMETRIE2D)):
                shapes = self.contruct_shapes(imgeo_geom[0])
                for shape in shapes:
                    if "arc" in str(type(shape)):
                        shape.add_to_layout(self.msp,dxfattribs=object_attributes)
                    else:
                        shape.update_dxf_attribs(object_attributes)
            try:
                if el.find(IMGEO_ORL) is not None:
                    for text,rot_degree,point in self.gen_labels(el):
                        self.msp.add_text(text,dxfattribs=label_attributes,rotation=rot_degree).set_pos(point)
                        
                if el.find(IMGEO_HOUSENR) is not None:
                    for text,rot_degree,point in self.gen_labels(el):
                        self.msp.add_text(text,dxfattribs=label_attributes,rotation=rot_degree).set_pos(point)
            except:
                pass

            cleanup(el)
      
        return self.doc

    def contruct_shapes(self,imgeo_geom):
        gml_geom = imgeo_geom.xpath(XP_GML)[0]
        geom_type = etree.QName(gml_geom).localname
        
        if geom_type == "Point":
            gml_pos = gml_geom.find(GML_POS)
            coord = np.array(gml_pos.text.split(),dtype=float)
            yield self.msp.add_point(coord)
        else:
            for poslist in gml_geom.xpath(XP_POSLIST):
                geom_subtype = etree.QName(poslist.getparent()).localname
                coords = np.array(poslist.text.split(),dtype=float).reshape(-1,2)
                if  geom_subtype == "Arc":
                    yield self.draw_arc(coords)
                else:
                    lwpolyline_shape = self.msp.add_lwpolyline(coords,close=False)
                    yield lwpolyline_shape
       
    def explode_lwpolyline(self,lwpolyline):
        for line_shape in list(lwpolyline.explode(self.msp)):
            yield line_shape