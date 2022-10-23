from . import *
from .pdok import BGT_API
from .stufgeo.stufgeo_xml import StufgeoXML
from .stufgeo.stufgeo_gml import StufgeoGML
from .stufgeo.stufgeo_cad import StufgeoCAD
from .stufgeo import xml_utils
import pygeos

TS = datetime.now().strftime("%Y%m%d")

class LV_BGT:
    def __init__(self,input_aoi,output_dir):

        self.input_aoi = self.read_geojson(input_aoi)
        
        #io dirs
        self.output_dir = Path(output_dir,f"{TS}_{APP_NAME.lower()}_data")
        self.output_dir.mkdir(parents=True,exist_ok=True)

        self.temp_dir = Path(self.output_dir,"temp")
        self.temp_dir.mkdir(parents=True,exist_ok=True)
        
        #export outputs
        self.stufgeo_xml = Path(self.output_dir,f'{Path(input_aoi).stem}_bgt.xml')
        
    def read_geojson(self,geojson):
        #read geojson as pygeos multipolygons
        with open(geojson,"rb") as src:
            geoms = pygeos.get_parts(pygeos.from_geojson(src.read()))
            try:
                return pygeos.multipolygons(geoms)
            except:
                return pygeos.multipolygons(geoms[0])
    
    def download_stufgeo(self,features):
        stufgeo_zip = Path(self.temp_dir,f"extract.zip")
        if len(features)==1:
            stufgeo_zip = Path(self.temp_dir,f"extract_{features[0]}.zip")

        stufgeo_dir = stufgeo_zip.with_suffix('')
        
        if not stufgeo_dir.exists():
            BGT_API.download_full_custom(features,str(self.input_aoi),"stufgeo",str(stufgeo_zip))
            BGT_API.extract_zip(stufgeo_zip,stufgeo_dir)

            LOGGER.info(f"Stufgeo successfully downloaded to {stufgeo_dir}")
            
        stufgeo_xml = list(stufgeo_dir.glob("*.xml"))[0]
        return stufgeo_xml
            
    def build_stufgeo(self,input_xml):
        if not self.stufgeo_xml.exists():
            doc = StufgeoXML(input_xml).filter_objects(self.input_aoi)

            xml_utils.export_document(doc,str(self.stufgeo_xml),False,False)
            LOGGER.info(f"Exported to {self.stufgeo_xml}")

        return self.stufgeo_xml

    def add_stufgeo_pbp(self,input_xml,input_pbp_xml):
        if Path(input_xml).exists() and Path(input_pbp_xml).exists():
            doc = StufgeoXML.filter_pbp(input_xml,input_pbp_xml)
            xml_utils.export_document(doc,input_xml,False,False)
            
        return input_xml
    
    @staticmethod
    def convert_stufgeo(stufgeo_xml,format,cleanup_cad=True):
        if format == 'GML':
            doc = StufgeoGML(stufgeo_xml).build_gml()
        elif format =='DXF':
            doc = StufgeoCAD(stufgeo_xml).build_cad(cleanup_cad)

        output_file = Path(stufgeo_xml).with_suffix(f".{format.lower()}")

        xml_utils.export_document(doc,str(output_file))
        LOGGER.info(f"Exported to {output_file}")

        