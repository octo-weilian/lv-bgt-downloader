from . import *
from app.stufgeo.parser import cleanup_element,get_labels

class StufgeoXML:
    def __init__(self,input_xml,input_pbp_xml):
        self.input_xml = input_xml
        self.input_pbp_xml = input_pbp_xml
        self.root = self.make_root(input_xml)

    def make_root(self,src):
        doc = etree.iterparse(src,huge_tree=True,events=("start",))
        _,root = next(doc)
        root_string = etree.tostring(root).decode("utf-8")
        pattern = ">"
        end_index = root_string.find(pattern)
        start_tags= root_string[:end_index+len(pattern)]+'\n'
        end_tag = start_tags.split()[0].replace("<","</")+">"

        base_root = etree.fromstring(start_tags+end_tag)
        base_root.append(root.find(IMGEO_STUUR))
        base_root.append(root.find(IMGEO_BERICHT))

        return base_root
    
    def geom2shape(self,element):
        if (geom:=element.xpath(XP_GEOMETRIE2D)):
            coords = np.hstack([coord.text.split(" ") for coord in geom[0].xpath(XP_POS)]).reshape(-1,2).astype(float)
            shape = pygeos.multipoints(coords)
            if len(coords)>1:
                shape = pygeos.linestrings(coords)
            return shape

    def concat_xy(self,element,xquery):
        if (geom:=element.xpath(xquery)):
            coords = np.hstack([coord.text.split(" ") for coord in geom[0].xpath(XP_POS)]).reshape(-1,2).astype(float)
            scaled_coords = (coords*1000).astype(int).astype(str)
            return np.apply_along_axis(''.join, 1, scaled_coords)
            
    def extract_objects(self,input_shape):
        obj_count = 0

        for _,el in etree.iterparse(self.input_xml,huge_tree=True,tag=IMGEO_OBJ):
            parent = el.getparent()
            if pygeos.intersects(input_shape,self.geom2shape(el)):
                self.root.append(copy.deepcopy(parent))
                obj_count +=1

            if (orl_el:=el.find(IMGEO_ORL)) is not None:
                orl_points = get_labels(orl_el)[2]
                if pygeos.intersects(input_shape,pygeos.multipoints(orl_points)):
                    self.root.append(copy.deepcopy(parent))
                    
            print(f"Objects found: {obj_count}",end='\r')
            cleanup_element(el)

        print(f"Total objects found: {obj_count}")
        return self.root
    
    def extract_pbp(self):
        pbp_count = 0
        pseudo_points = []
        for _,el in etree.iterwalk(self.root,tag=IMGEO_OBJ):
            pseudo_points.append(self.concat_xy(el,XP_GEOMETRIE2D))
        pseudo_points = np.hstack(pseudo_points)
        
        for _,el in etree.iterparse(self.input_pbp_xml,huge_tree=True,tag=IMGEO_OBJ):
            if self.concat_xy(el,XP_GEOMETRIE)[0] in pseudo_points:
                self.root.append(copy.deepcopy(el.getparent()))
                pbp_count +=1
                print(f"PBP found: {pbp_count}",end='\r')
            cleanup_element(el)

        print(f"Total PBP found: {pbp_count}")
        return self.root
    
        
        
            
 
            
        









