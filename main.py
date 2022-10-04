from app import APP_CONFIG
from app.bgt import BGT

MAKE_CAD = APP_CONFIG["transformer"]["make_cad"]
MAKE_GML = APP_CONFIG["transformer"]["make_gml"]

if __name__=="__main__":
    print("Running BGT-downloader...")
    
    bgt_processor = BGT()
    extract_xml, extract_pbp_xml = bgt_processor.download_extract()
    filtered_xml = bgt_processor.make_stufgeo_xml(extract_xml,extract_pbp_xml)
    
    if bool(int(MAKE_GML)):
        filtered_gml = bgt_processor.transform_stufgeo(filtered_xml,'gml')

    if bool(int(MAKE_CAD)): 
        filtered_topo = bgt_processor.transform_stufgeo(filtered_xml,'dxf')
    
   


   

    
    

    
    
    




  
        





        

