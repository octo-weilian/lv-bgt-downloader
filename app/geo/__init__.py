from app import *

#set up GDAL environment
OSGEO_PATH = os.environ["VIRTUAL_ENV"] + "\Lib\site-packages\osgeo"
OSGEO_UTILS = os.environ["VIRTUAL_ENV"] + "\Lib\site-packages\osgeo_utils"
GDAL_DATA = OSGEO_PATH+"\data\gdal"
PROJ_LIB = OSGEO_PATH+"\data\proj"
GDAL_PATHS = [OSGEO_PATH,GDAL_DATA,PROJ_LIB]

os.environ["PATH"] += ';'+OSGEO_PATH
os.environ["GDAL_DATA"]= GDAL_DATA
os.environ["PROJ_LIB"]= PROJ_LIB
os.environ["GDAL_UTILS"] = OSGEO_UTILS