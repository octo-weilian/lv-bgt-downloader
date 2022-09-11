from io import StringIO
from . import *
from app.models import parser


class StufGeo:
    def __init__(self,input_xml,input_pbp_xml):
        self.input_xml = input_xml
        self.input_pbp_xml = input_pbp_xml

        self.root = self.make_base_root(input_xml)

        self.obj_count = 0
        self.pbp_count = 0

    def make_base_root(self,src):
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
    
    def extract_objects(self,input_shape):
        
        for _,el in etree.iterparse(self.input_xml,huge_tree=True,tag=IMGEO_OBJ):
            parent = el.getparent()
            
            if pygeos.intersects(input_shape,parser.geom2shape(el,make_bound=True)):
                self.root.append(copy.deepcopy(parent))
                self.obj_count +=1

            if (orl_el:=el.find(IMGEO_ORL)) is not None:
                orl_points = parser.get_labels(orl_el)[2]
                if pygeos.intersects(input_shape,pygeos.multipoints(orl_points)):
                    self.root.append(copy.deepcopy(parent))
                    self.obj_count +=1

            print(f"Objects found: {self.obj_count}",end='\r')
            parser.cleanup(el)

        print(f"Total objects found: {self.obj_count}")
        return self.root
    
    def extract_pbp(self):
        
        all_points = []
        for _,el in etree.iterwalk(self.root,tag=IMGEO_OBJ):
            if (sum_points := parser.sum_geom(el,xp_geometrie2d)):
                for p in sum_points:
                    all_points.append(p)
        all_points = np.array(all_points)

        for _,el in etree.iterparse(self.input_pbp_xml,huge_tree=True,tag=IMGEO_OBJ):
            sum_point = parser.sum_geom(el,xp_geometrie)[0]
            if sum_point in all_points :
                parent = el.getparent()
                self.root.append(copy.deepcopy(parent))

                self.pbp_count +=1
                print(f"PBP found: {self.pbp_count}",end='\r')
            parser.cleanup(el)

        print(f"Total PBP found: {self.pbp_count}")

        return self.root
    
        
        
            
 
            
        









