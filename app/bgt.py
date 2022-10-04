from socket import fromshare
import ezdxf
from app import *
from app.pdok.api import API
from app.stufgeo.stufgeo_xml import StufgeoXML
from app.stufgeo.stufgeo_gml import StufgeoGML
from app.stufgeo.stufgeo_cad import StufgeoCAD
from app.stufgeo import parser

TS = datetime.now().strftime("%Y%m%d")
EXTRACT_PATH = os.path.join(DATA_INPUT,f"{TS}_extract")
INPUT_SHAPES = APP_CONFIG["shapes"]["input"]
DISCARD_FEATURES = list(filter(None,APP_CONFIG["api"]["discard_features"].split(";")))

EXTRACT_PBP_PATH = EXTRACT_PATH+'_pbp'

class BGT:
    def __init__(self):
        self.shapes_geom = self.read_shape(INPUT_SHAPES)
        self.discard_features = DISCARD_FEATURES

        input_shapes_fname = os.path.basename(INPUT_SHAPES).split(".")[0]
        self.stufgeo_xml = os.path.join(DATA_OUTPUT,f'{TS}_{input_shapes_fname}_bgt.xml')

    def read_shape(self,geojson):
        with open(geojson,"rb") as src:
            shapes_geom = pygeos.from_geojson(src.read())
            return pygeos.multipolygons(pygeos.get_parts(shapes_geom))
             
    def pbp_check(self):
        if not 'plaatsbepalingspunt' in self.discard_features:
            return True
    
    def download_extract(self):

        extract_xml = None
        extract_pbp_xml = None
   
        bgt_api = API()
        shapes_wkt = pygeos.to_wkt(self.shapes_geom)
        selected_features = bgt_api.get_featuretypes(self.discard_features)

        bgt_api.download(selected_features,shapes_wkt,EXTRACT_PATH)
        extract_xml = glob(EXTRACT_PATH+"/*.xml")[0]

        if self.pbp_check():
            bgt_api.download(['plaatsbepalingspunt'],shapes_wkt,EXTRACT_PBP_PATH)
            extract_pbp_xml = glob(EXTRACT_PBP_PATH+"/*.xml")[0]
        
        return extract_xml,extract_pbp_xml

    def make_stufgeo_xml(self,input_xml,input_pbp_xml=""):
        print("Extracting objects from stufgeo...")

        stufgeo_xml_model = StufgeoXML(input_xml,input_pbp_xml)

        if not os.path.exists(self.stufgeo_xml):
            doc_xml = stufgeo_xml_model.extract_objects(self.shapes_geom)
        
            if self.pbp_check() and os.path.exists(input_pbp_xml):
                doc_xml = stufgeo_xml_model.extract_pbp()

            parser.export_document(doc_xml,self.stufgeo_xml,False,False)

        return self.stufgeo_xml

    def transform_stufgeo(self,input_xml,doc_type):
        output_doc = input_xml.replace(".xml",f'.{doc_type}')
        if doc_type =='gml':
            doc = StufgeoGML(input_xml).build_gml()
        elif doc_type=='dxf':
            doc = StufgeoCAD(input_xml).build_cad()
        
        parser.export_document(doc,output_doc)

        