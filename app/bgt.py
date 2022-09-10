from app import *
from app.pdok.api import API

from app.models.stufgeo import StufGeo,IMGEO_OBJ
from app.models import parser
from app.models.gml import GML
import time

INPUT_SHAPES = APP_CONFIG["shapes"]["input"]
DISCARD_FEATURES = list(filter(None,APP_CONFIG["api"]["discard_features"].split(";")))

class BGT:
    def __init__(self):
        
        with open(INPUT_SHAPES,"rb") as src:
            shapes_geom = pygeos.from_geojson(src.read())
            shapes_polygons = pygeos.get_parts(shapes_geom)
            shapes_multipolygons = pygeos.multipolygons(shapes_polygons)
            self.shapes_wkt = pygeos.to_wkt(shapes_multipolygons,output_dimension=2)

        self.input_xml = None
        self.input_pbp_xml = None

        ts = datetime.now().strftime("%Y%m%d")
        self.extract_path = os.path.join(DATA_INPUT,f"{ts}_extract")
        self.filtered_xml = os.path.join(DATA_OUTPUT,f'{ts}_bgt_filtered.xml')
        self.filtered_pbp_xml = os.path.join(DATA_OUTPUT,f'{ts}_bgt_pbp_filtered.xml')

    def pbp_check(self):
        if not 'plaatsbepalingspunt' in DISCARD_FEATURES:
            return True

    def fetch_data(self):

        bgt_api = API()
        selected_features = bgt_api.get_featuretypes(DISCARD_FEATURES)
        extract_dir = bgt_api.download(selected_features,self.shapes_wkt,self.extract_path)
        self.input_xml = glob(extract_dir+"/*.xml")[0]

        if self.pbp_check():
            extract_pbp_dir = bgt_api.download(['plaatsbepalingspunt'],self.shapes_wkt,self.extract_path+'_pbp')
            self.input_pbp_xml = glob(extract_pbp_dir+"/*.xml")[0]

        return self.input_xml,self.input_pbp_xml

    def make_stufgeo(self):
        print("Extracting data from stufgeo...")

        stufgeo_model = StufGeo(self.input_xml)

        if not os.path.exists(self.filtered_xml):
            doc = stufgeo_model.extract_data(self.shapes_wkt)
            parser.export_document(doc,self.filtered_xml,cleanup_ns=False,indent_by=False)

        if not os.path.exists(self.filtered_pbp_xml) and self.pbp_check():
            pbp_doc = stufgeo_model.extract_pbp(self.filtered_xml,self.input_pbp_xml)
            parser.export_document(pbp_doc,self.filtered_pbp_xml,cleanup_ns=False,indent_by=False)

        return self.filtered_xml,self.filtered_pbp_xml

    def make_topo(self,input_xml):

        output_gml = input_xml.replace(".xml",".gml")
        doc = parser.parse_gml(input_xml,output_gml)
        parser.export_document(input_doc=doc,output_doc=output_gml)
        return output_gml