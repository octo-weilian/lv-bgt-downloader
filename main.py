from app import APP_CONFIG
from app.models.stufgeo import StufGeo,IMGEO_OBJ
from app.models import parser
from app.models.gml import GML
from app.bgt import BGT
from app.geo import transformer

MAKE_TOPO = APP_CONFIG["transformer"]["make_topo"]

if __name__=="__main__":
    print("Running BGT-downloader...")
    
    bgt_processor = BGT()
    input_xml,input_pbp_xml = bgt_processor.fetch_data()
    filtered_xml,filtered_pbp_xml = bgt_processor.make_stufgeo()
    
    if bool(int(MAKE_TOPO)):
        filtered_gml = bgt_processor.make_topo(filtered_xml)
        filtered_topo = transformer.gml2dxf(filtered_gml)
    
   


   

    
    

    
    
    




  
        





        

