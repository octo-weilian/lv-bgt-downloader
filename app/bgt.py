from app import *
from app.pdok.api import API
from app.models.stufgeo import StufGeo
from app.models import parser

TS = datetime.now().strftime("%Y%m%d")
EXTRACT_PATH = os.path.join(DATA_INPUT,f"{TS}_extract")
EXTRACT_PBP_PATH = EXTRACT_PATH+'_pbp'

FILTERED_XML = os.path.join(DATA_OUTPUT,f'{TS}_bgt_filtered.xml')

class BGT:
    def __init__(self,geojson,discard_features):
        self.shapes = self.read_shape(geojson)
        self.discard_features = discard_features

    def read_shape(self,geojson):
        with open(geojson,"rb") as src:
            shapes_geom = pygeos.from_geojson(src.read())
            return pygeos.multipolygons(pygeos.get_parts(shapes_geom))
             
    def pbp_check(self):
        if not 'plaatsbepalingspunt' in self.discard_features:
            return True
    
    def download_extract(self):

        input_xml = None
        input_pbp_xml = None
   
        bgt_api = API()
        shapes_wkt = pygeos.to_wkt(self.shapes)
        selected_features = bgt_api.get_featuretypes(self.discard_features)

        bgt_api.download(selected_features,shapes_wkt,EXTRACT_PATH)
        input_xml = glob(EXTRACT_PATH+"/*.xml")[0]

        if self.pbp_check():
            bgt_api.download(['plaatsbepalingspunt'],shapes_wkt,EXTRACT_PBP_PATH)
            input_pbp_xml = glob(EXTRACT_PBP_PATH+"/*.xml")[0]
        
        return input_xml,input_pbp_xml

    def make_stufgeo(self,input_xml,input_pbp_xml=""):
        print("Extracting objects from stufgeo...")

        stufgeo_model = StufGeo(input_xml,input_pbp_xml)

        if not os.path.exists(FILTERED_XML):
            doc = stufgeo_model.extract_objects(self.shapes)
        
            if self.pbp_check() and os.path.exists(input_pbp_xml):
                doc = stufgeo_model.extract_pbp()

            parser.export_document(doc,FILTERED_XML,False,False)

        return FILTERED_XML

    def make_topo(self,input_xml):

        output_gml = input_xml.replace(".xml",".gml")
        doc = parser.parse_gml(input_xml,output_gml)
        parser.export_document(doc,output_gml)
        return output_gml