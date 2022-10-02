from . import *

def cleanup(element):
    element.clear()
    for ancestor in element.xpath('ancestor-or-self::*'):
        while ancestor.getprevious() is not None:
            del ancestor.getparent()[0]

def geom2shape(element,make_bound=False):
    if (geom:=element.xpath(XP_GEOMETRIE2D)):
        stack_points = []
        for coord in geom[0].xpath(XP_POS):
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
        for coord in geom[0].xpath(XP_POS):
            split_points = np.array(coord.text.split(" "),dtype=float)
            stack_points.append(split_points)
        stack_points = np.concatenate(stack_points,axis=None).reshape(-1,2)
        stack_points = (stack_points*1000).astype(int).tolist()
        stack_points = [str(p[0])+str(p[1]) for p in stack_points]
        return stack_points
        
def get_lokaal_id(element):
    if (lokaal_id := element.xpath(XP_LOKAALID)):
        return lokaal_id[0].text

def rotation2degree(rotation):
    degree = abs(rotation)
    if rotation>0:
        degree = 360-rotation
    return degree

def get_labels(element):
    text_elements = element.xpath(XP_TEKST)
    texts = [el.text for el in text_elements]

    gml_points = element.xpath(XP_POINT)
    rotation_elements = element.xpath(XP_HOEK)

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
    if isinstance(input_doc,lxml.etree._Element):
        if cleanup_ns:
            etree.cleanup_namespaces(input_doc)
        tree = input_doc.getroottree()
        if indent_by:
            etree.indent(tree,indent_by)
        tree.write(output_doc,pretty_print=True, encoding='UTF-8')
    
    if isinstance(input_doc,ezdxf.document.Drawing):
        input_doc.saveas(output_doc)

    print(f"Exported to {output_doc}")


