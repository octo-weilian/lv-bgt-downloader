
from .api import API
# from .stufgeo.parse_xml import StufgeoXML
# from .stufgeo.parse_gml import StufgeoGML
# from .stufgeo.parse_cad import StufgeoCAD
# from .stufgeo import xml_utils

from pathlib import Path
import shapely
from typing import Union,Iterable
import os

class BGT(API):

    def __init__(self,geofilter:Union[str, os.PathLike]) -> None:
        self.geofilter = self._read_geofilter(geofilter)
        
    def _read_geofilter(self,geofilter:Union[str,os.PathLike]) -> Union[shapely.Polygon,shapely.MultiPolygon]:
        if Path(geofilter).is_file() and Path(geofilter).suffix == '.geojson':
            with open(geofilter,"rb") as src:
                geofilter = shapely.from_geojson(src.read())
        else:
            geofilter = shapely.from_wkt(geofilter)
        
        if geofilter.geom_type == 'GeometryCollection':
            geofilter = shapely.get_parts(geofilter)
        
        return shapely.union_all(shapely.multipolygons(geofilter))

    def extract_stufgeo(self,features:Iterable[str], output:Union[str, os.PathLike],output_format) -> Path:
        extract_zip =  BGT.download_full_custom(features,'stufgeo',shapely.to_wkt(self.geofilter),output)
        extract_folder = BGT.unpack_zip(extract_zip,False)
        
        in_stufgeo = next(Path(extract_folder).glob('*.xml'))
        out_stufgeo = Path(in_stufgeo.parent,f"{in_stufgeo.stem}_filtered.xml")
        
        # if not out_stufgeo.exists():
        #     filtered_stufgeo = StufgeoXML(in_stufgeo).filter_objects(self.geofilter)
        #     xml_utils.export_document(filtered_stufgeo,str(out_stufgeo),False,False)
        #     print(f"Exported to {out_stufgeo}")
        # else:
        #     print(f"{out_stufgeo} already exists. Processing skipped.")

    # def add_stufgeo_pbp(self,input_xml,input_pbp_xml):
    #     if Path(input_xml).exists() and Path(input_pbp_xml).exists():
    #         doc = StufgeoXML.filter_pbp(input_xml,input_pbp_xml)
    #         xml_utils.export_document(doc,input_xml,False,False)
    #     else:
    #         print(f"{input_xml} and/or {input_pbp_xml} does not exists")
            
    #     return input_xml
    
    # # @staticmethod
    # def convert_stufgeo(input_xml,format,cleanup_cad=True):
    #     output_file = Path(input_xml).with_suffix(f".{format.lower()}")
    #     if not output_file.exists() and Path(input_xml).exists():
    #         if format == 'GML':
    #             doc = StufgeoGML(input_xml).build_gml()
    #         elif format =='DXF':
    #             doc = StufgeoCAD(input_xml).build_cad(cleanup_cad)

    #         xml_utils.export_document(doc,str(output_file))
    #         print(f"Exported to {output_file}")
    #     elif not Path(input_xml).exists():
    #         print(f"{input_xml} does not exists")

    
    
    
        