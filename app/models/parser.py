from . import *
from app.models.gml import GML

def cleanup(element):
    element.clear()
    for ancestor in element.xpath('ancestor-or-self::*'):
        while ancestor.getprevious() is not None:
            del ancestor.getparent()[0]

def geom2shape(element,make_bound=False):
    if (geom:=element.xpath(xp_geometrie2d)):
        stack_points = []
        for coord in geom[0].xpath(xp_pos):
            split_points = np.array(coord.text.split(" "),dtype=float)
            stack_points.append(split_points)
        stack_points = np.concatenate(stack_points,axis=None).reshape(-1,2)
        shape = pygeos.multipoints(stack_points)
        if len(stack_points)>1 and make_bound:
            shape = pygeos.linestrings(stack_points)
        return shape

def sum_geom(element,xquery):
    if (geom:=element.xpath(xquery)):
        stack_points = []
        for coord in geom[0].xpath(xp_pos):
            split_points = np.array(coord.text.split(" "),dtype=float)
            stack_points.append(split_points)
        stack_points = np.concatenate(stack_points,axis=None).reshape(-1,2)
        stack_points = (stack_points*1000).astype(int).tolist()
        stack_points = [str(p[0])+str(p[1]) for p in stack_points]
        
        return stack_points
        
def get_lokaal_id(element):
    if (lokaal_id := element.xpath(xp_lokaalid)):
        return lokaal_id[0].text

def rotation2degree(rotation):
    degree = abs(rotation)
    if rotation>0:
        degree = 360-rotation
    return degree

def make_ogr_label(text,rotation=0,text_size=100,color=None):
    OGR_LABEL = f"LABEL(f:Arial,c:{color},s:{text_size}cm,p:5,a:{rotation},t:{text})"
    return GML.featureAttribute("OGR_STYLE",OGR_LABEL)

def make_ogr_pen(color=None,width='5'):
    OGR_PEN = f"PEN(c:{color},w:{width}px)"
    return GML.featureAttribute("OGR_STYLE",OGR_PEN)

def make_label_members(element,gml_id=None,color=None):
    texts,rotations,points,gml_points = get_labels(element)
    for i in range(len(gml_points)):
        feature_member = GML.featureMember()
        feature_obj = GML.featureObject("Label",gml_points[i],gml_id)
        ogr_style_attribute = make_ogr_label(text=texts[i],rotation=rotation2degree(float(rotations[i])),color=color)
        feature_obj.append(ogr_style_attribute)
        feature_member.append(feature_obj)
        yield feature_member
        
def get_labels(element):
    text_elements = element.xpath(xp_tekst)
    texts = [el.text for el in text_elements]

    gml_points = element.xpath(xp_point)
    rotation_elements = element.xpath(xp_hoek)

    if len(text_elements)!=len(gml_points):
        texts = texts * len(gml_points)

    points = []
    rotations = []
    for i in range(len(gml_points)):
        pos = gml_points[i].find(GML_POS)
        coord = np.array(pos.text.split(" "),dtype=float)
        points.append(coord)
        rotations.append(rotation_elements[i].text)

    points = np.concatenate(points,axis=None).reshape(-1,2)
    return texts,rotations,points,gml_points

def export_document(input_doc,output_doc,cleanup_ns=True,indent_by=' '):
    if cleanup_ns:
        etree.cleanup_namespaces(input_doc)
    tree = input_doc.getroottree()
    if indent_by:
        etree.indent(tree,indent_by)
    tree.write(output_doc,pretty_print=True, encoding='UTF-8')
    print(f"Exported to {output_doc}")
    

def make_topo_point_feature(element,gml_geom,geom_type):
    feature_obj = GML.featureObject("Topo_point",gml_geom,get_lokaal_id(element))
    feature_obj.append(GML.featureAttribute("OBJECT",element.attrib[STUFGEO_ENT_TYPE]))
    feature_obj.append(GML.featureAttribute("TYPE",element.find(IMGEO_PLUSTYPE).text))
    return feature_obj

def make_topo_feature(element,gml_geom,geom_type):
    feature_obj = GML.featureObject("Topo",gml_geom,get_lokaal_id(element))
    feature_obj.append(GML.featureAttribute("OBJECT",element.attrib[STUFGEO_ENT_TYPE]))
    return feature_obj

def parse_gml(input_xml,output_gml,tag=IMGEO_OBJ):
    
        feature_collection = GML.featureCollection()
        for _,el in etree.iterparse(input_xml,huge_tree=True,tag=tag):
            feature_member = GML.featureMember()
           
            if (geom:=el.xpath(xp_geometrie2d)):
                gml_geom = geom[0].xpath(xp_gml)[0]
                geom_type = gml_geom.tag.lstrip(GML_NS)
                
                if geom_type =="Point":
                    feature_obj = make_topo_point_feature(el,gml_geom,geom_type)
                    
                else:
                    feature_obj = make_topo_feature(el,gml_geom,geom_type)
                    if el.attrib[STUFGEO_ENT_TYPE] == 'PND':
                        
                        if len(list(el.find(IMGEO_HOUSENR)))>0:
                            for member in make_label_members(el,get_lokaal_id(el),'#FF0000'):
                                feature_collection.append(member)

                feature_member.append(feature_obj)
                feature_collection.append(feature_member)

            if el.find(IMGEO_ORL) is not None:
                for member in make_label_members(el,get_lokaal_id(el)):
                    feature_collection.append(member)
             
            cleanup(el)
    
        return feature_collection



