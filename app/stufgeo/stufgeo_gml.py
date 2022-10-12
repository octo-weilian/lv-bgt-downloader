from . import *
from app.stufgeo.gml import GML
from app.stufgeo.parser import get_lokaal_id,cleanup_element,get_labels

class StufgeoGML:
    def __init__(self,input_xml):
        self.input_xml = input_xml
        self.imgeo_objects = etree.iterparse(input_xml,huge_tree=True,tag=IMGEO_OBJ)
        self.feature_collection = GML.featureCollection()

    def build_gml(self):
        for _,el in self.imgeo_objects:
            feature_member = GML.featureMember()
            if (imgeo_geom:=el.xpath(XP_GEOMETRIE2D)):
                feature_member.append(self.topo_feature(el,imgeo_geom[0]))
                self.feature_collection.append(feature_member)
                
            try:
                if el.find(IMGEO_HOUSENR) is not None:
                    for feature_label in self.gen_labels(el):
                        feature_member.append(feature_label)
                        self.feature_collection.append(feature_member)

                if el.find(IMGEO_ORL) is not None:
                    for feature_label in self.gen_labels(el):
                        feature_member.append(feature_label)
                        self.feature_collection.append(feature_member)
            except:
                pass
            
            cleanup_element(el)

        return self.feature_collection

    def gen_labels(self,element):
        texts,rotations,points,gml_points = get_labels(element)
        for i in range(len(gml_points)):
            feature_label = GML.featureObject("Label",gml_points[i])
            feature_label.append(GML.featureAttribute("Text",texts[i]))
            feature_label.append(GML.featureAttribute("Rotation",float(rotations[i]) ))
            yield feature_label
    
    def topo_feature(self,element,imgeo_geom):
        gml_geom = imgeo_geom.xpath(XP_GML)[0]
        geom_type = etree.QName(gml_geom).localname
        if geom_type == "Point":
            feature_obj = GML.featureObject("TopoPoint",gml_geom,get_lokaal_id(element))
            feature_obj.append(GML.featureAttribute("Type",element.find(IMGEO_PLUSTYPE).text))
        elif "Line" in geom_type:
            feature_obj = GML.featureObject("TopoLine",gml_geom,get_lokaal_id(element))
        else:
            feature_obj = GML.featureObject("Topo",gml_geom,get_lokaal_id(element))

        feature_obj.append(GML.featureAttribute("Object",element.attrib[STUFGEO_ENT_TYPE]))
        return feature_obj


        

