from app import APP_CONFIG
from app.models.stufgeo import StufGeo,IMGEO_OBJ
from app.models import parser
from app.models.gml import GML
from app.bgt import BGT
from app.geo import transformer

INPUT_SHAPES = APP_CONFIG["shapes"]["input"]
MAKE_TOPO = APP_CONFIG["transformer"]["make_topo"]
DISCARD_FEATURES = list(filter(None,APP_CONFIG["api"]["discard_features"].split(";")))

if __name__=="__main__":
    print("Running BGT-downloader...")
    
    bgt_processor = BGT(INPUT_SHAPES,DISCARD_FEATURES)
    input_xml, input_pbp_xml = bgt_processor.download_extract()
    filtered_xml = bgt_processor.make_stufgeo(input_xml,input_pbp_xml)
    
    if bool(int(MAKE_TOPO)):
        filtered_gml = bgt_processor.make_topo(filtered_xml)
        filtered_topo = transformer.gml2dxf(filtered_gml)
    
   


   

    
    

    
    
    




  
        





        

