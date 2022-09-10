from . import *

GML_NS = "http://www.opengis.net/gml"
etree.register_namespace("gml",GML_NS)

GML_ID_TAG = etree.QName(GML_NS,"id")
GML_SRS ="urn:ogc:def:crs:EPSG::28992"

class GML:

    @classmethod
    def featureCollection(self):
        root_name = etree.QName(GML_NS,"FeatureCollection")
        root = etree.Element(root_name)
        root.text = ""
        return root

    @classmethod
    def featureGeometry(self,name = "geometry" ):
        geom_name = etree.QName(GML_NS,name)
        geom_prop = etree.Element(geom_name)
        geom_prop.text = ""
        return geom_prop
    
    @classmethod
    def featureMember(self):
        feature_member = etree.fromstring("<featureMember></featureMember>")
        feature_member.text = ''
        return feature_member

    @classmethod
    def featureAttribute(self,name,value=''):
        att_name = etree.QName(GML_NS,name)
        att_element = etree.Element(att_name)
        att_element.text = str(value)
        return att_element

    @classmethod
    def featureObject(self,name,gml_geom,gml_id=''):
        feature_name = etree.QName(GML_NS,name)
        feature_object = etree.Element(feature_name,{GML_ID_TAG:str(gml_id)})

        feature_geom = self.featureGeometry()
        gml_geom.attrib["srsName"] = GML_SRS
        feature_geom.append(gml_geom)
        feature_object.append(feature_geom)

        return feature_object


        
    
        

