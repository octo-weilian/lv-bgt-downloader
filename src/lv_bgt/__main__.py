# from lv_bgt._bgt import LV_BGT
# from lv_bgt.pdok import BGT_API
# from lv_bgt.utils.config import appConfig

# #load app configfile 
# APP_CONFIG = appConfig("appConfig.ini").parser

# #project config
# OUTPUT_DIR = APP_CONFIG.get("project","output_dir")
# INPUT_AOI = APP_CONFIG.get("project","input_aoi")
# DROP_FEATURES = list(filter(None,APP_CONFIG.get("project","drop_features").split(";")))

# #processing config
# ADD_PBP = APP_CONFIG.getboolean("processing","add_pbp")
# MAKE_GML = APP_CONFIG.getboolean("processing","make_gml")
# MAKE_CAD = APP_CONFIG.getboolean("processing","make_cad")
# CLEANUP_CAD = APP_CONFIG.getboolean("processing","cleanup_cad")

# if __name__=="__main__":
#     lv_bgt = LV_BGT(INPUT_AOI,OUTPUT_DIR)
    
#     #download stufgeo extract and build new stufgeo
#     all_features =  BGT_API.get_features().keys()
#     selected_features = sorted(list(set(all_features)-set(DROP_FEATURES)))
#     extract_xml = lv_bgt.download_stufgeo(selected_features)
#     stufgeo_xml = lv_bgt.build_stufgeo(extract_xml)

#     #add PBPs
#     if ADD_PBP:
#         pbp_xml = lv_bgt.download_stufgeo(["plaatsbepalingspunt"])
#         lv_bgt.add_stufgeo_pbp(stufgeo_xml,pbp_xml)
    
#     #convert stufgeo XML to GML
#     if MAKE_GML:
#         lv_bgt.convert_stufgeo(stufgeo_xml,"GML")

#     #convert stufgeo XML to DXF
#     if MAKE_CAD:
#         lv_bgt.convert_stufgeo(stufgeo_xml,"DXF",CLEANUP_CAD)
    



   

    
    

    
    
    




  
        





        

