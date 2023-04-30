from lv_bgt import BGT

drop_features = ['plaatsbepalingspunt','buurt','wijk']
features = BGT.get_features(drop_features)

bgt = BGT("aoi.geojson")
bgt.extract_stufgeo(features,'.')






