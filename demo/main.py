from lv_bgt_downloader.lv_bgt import LV_BGT
from lv_bgt_downloader.pdok import BGT_API
from lv_bgt_downloader.utils.config import appConfig

#load app configfile 
APP_INI = "appConfig.ini"
APP_CONFIG = appConfig(APP_INI)

if APP_CONFIG.parser is not None:
    #project config
    OUTPUT_DIR = APP_CONFIG.get("app","output_dir")
    INPUT_AOI = APP_CONFIG.get("app","input_aoi")
    FEATURES = list(filter(None,APP_CONFIG.get("app","features").split(";")))

    #processing config
    ADD_PBP = bool(int(APP_CONFIG.get("processing","add_pbp")))
    MAKE_GML = bool(int(APP_CONFIG.get("processing","make_gml")))
    MAKE_CAD = bool(int(APP_CONFIG.get("processing","make_cad")))
    CLEANUP_CAD = bool(int(APP_CONFIG.get("processing","cleanup_cad")))

if __name__=="__main__":
    lv_bgt = LV_BGT(INPUT_AOI,OUTPUT_DIR)
    
    #download all features except
    drop_features = ["plaatsbepalingspunt","buurt","wijk"]
    extract_features = BGT_API.get_features().keys()
    extract_features = sorted(list(set(extract_features)-set(drop_features)))
    extract_xml = lv_bgt.download_stufgeo(extract_features)
    
    #build stufgeo
    stufgeo_xml = lv_bgt.build_stufgeo(extract_xml)

    if ADD_PBP:
        pbp_xml = lv_bgt.download_stufgeo(["plaatsbepalingspunt"])
        lv_bgt.add_stufgeo_pbp(stufgeo_xml,pbp_xml)
    
    if MAKE_GML:
        lv_bgt.convert_stufgeo(stufgeo_xml,"GML")

    if MAKE_CAD:
        lv_bgt.convert_stufgeo(stufgeo_xml,"DXF",CLEANUP_CAD)
    
    
    
    



    

    


   



   

    
    

    
    
    




  
        





        

