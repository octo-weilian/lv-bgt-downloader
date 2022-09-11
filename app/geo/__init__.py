from app import *

#set up GDAL environment
VENV_PATH = os.environ["VIRTUAL_ENV"] 
OSGEO_PATH = VENV_PATH + "\Lib\site-packages\osgeo"

os.environ["PATH"] += ';'+ OSGEO_PATH
os.environ["GDAL_DATA"]= OSGEO_PATH+"\data\gdal"
os.environ["PROJ_LIB"]= OSGEO_PATH+"\data\proj"
os.environ["GDAL_UTILS"] = VENV_PATH+ "\Lib\site-packages\osgeo_utils"