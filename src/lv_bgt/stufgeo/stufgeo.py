from . import *
from .xml import XML
import shapely
import copy

class Stufgeo(XML):
    def __init__(self,filename):
        self.filename = filename
        self.root = self.construct_root(filename)

    def construct_root(self,filename):
        doc = etree.iterparse(filename,huge_tree=True,events=("start",))
        _,root = next(doc)
        root_str = etree.tostring(root).decode("utf-8")
        end_index = root_str.find(">")
        start_tags= root_str[:end_index+len(">")]+"\n"
        end_tag = start_tags.split()[0].replace("<","</")+">"
        
        base_root = etree.fromstring(start_tags+end_tag)
        base_root.append(root.find(IMGEO_STUUR))
        base_root.append(root.find(IMGEO_BERICHT))

        return base_root
    
    @staticmethod
    def get_lokaal_id(element):
        if (lokaal_id := element.xpath(XP_LOKAALID)):
            return lokaal_id[0].text
    
    @staticmethod
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
    
    @staticmethod
    def geom2d_to_shape(element):
        if (geom:=element.xpath(XP_GEOMETRIE2D)):
            coords = np.hstack([coord.text.split(" ") for coord in geom[0].xpath(XP_POS)]).reshape(-1,2).astype(float)
            shape = shapely.multipoints(coords)
            if len(coords)>1:
                shape = shapely.linestrings(coords)
            return shape

    @classmethod
    def filter_objects(cls,geofilter):
        obj_count = 0

        for _,el in etree.iterparse(cls.filename,huge_tree=True,tag=IMGEO_OBJ):
            parent = el.getparent()
            if shapely.intersects(geofilter,Stufgeo.geom2d_to_shape(el)):
                cls.root.append(copy.deepcopy(parent))
                obj_count +=1

            if (orl_el:=el.find(IMGEO_ORL)) is not None:
                orl_points = XML.get_labels(orl_el)[2]
                if shapely.intersects(geofilter,shapely.multipoints(orl_points)):
                    cls.root.append(copy.deepcopy(parent))
                    
            print(f"Objects found: {obj_count}",end='\r')

            Stufgeo.cleanup_element(el)

        print(f"Objects found: {obj_count}")

        

    # @staticmethod
    # def concat_xy(element,xquery):
    #     if (geom:=element.xpath(xquery)):
    #         coords = np.hstack([coord.text.split(" ") for coord in geom[0].xpath(XP_POS)]).reshape(-1,2).astype(float)
    #         scaled_coords = (coords*1000).astype(int).astype(str)
    #         return np.apply_along_axis(''.join, 1, scaled_coords)

    # @staticmethod
    # def filter_pbp(input_xml,input_pbp_xml):

    #     pbp_count = 0
    #     pseudo_points = []
       
    #     doc = etree.iterparse(input_xml,huge_tree=True,tag=IMGEO_OBJ)

    #     for _,el in doc:
    #         pseudo_points.append(Stufgeo.concat_xy(el,XP_GEOMETRIE2D))

    #         if el.find(IMGEO_PBP) is not None:
    #             pseudo_points.clear()
    #             break

    #     if pseudo_points:
    #         pseudo_points = np.hstack(pseudo_points)

    #         root = doc.root
    #         for _,el in etree.iterparse(input_pbp_xml,huge_tree=True,tag=IMGEO_OBJ):
    #             if Stufgeo.concat_xy(el,XP_GEOMETRIE)[0] in pseudo_points:
    #                 root.append(copy.deepcopy(el.getparent()))
    #                 pbp_count +=1
    #                 print(f"PBP found: {pbp_count}",end='\r')

    #             Stufgeo.cleanup_element(el)
                
    #         print(f"Added {pbp_count} PBPs to {input_xml}")
    #         return root
    #     else:
    #         print(f"{input_xml} already contains PBPs")
        
        
            
 
            
        









