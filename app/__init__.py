import os
import re
from datetime import datetime
import configparser
import sys
import time
import json
import pygeos
from glob import glob

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

