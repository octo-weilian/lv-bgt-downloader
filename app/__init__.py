import os,re,sys,time,copy,configparser
from datetime import datetime
from glob import glob
import lxml
from lxml import etree
import pygeos
import numpy as np
import ezdxf

#load app configfile (create template if not exists)
APP_INI = "appConfig.ini"
APP_CONFIG = configparser.ConfigParser()
if os.path.exists(APP_INI):
    APP_CONFIG.read(APP_INI)
else:
    sys.exit()

DATA_INPUT = "data\input"
DATA_OUTPUT = "data\output"
os.makedirs(DATA_INPUT,exist_ok=True)
os.makedirs(DATA_OUTPUT,exist_ok=True)

