import os,re,sys,time,json
from zipfile import ZipFile
import requests
from pathlib import Path
from datetime import datetime
from .utils.logger import appLogger

APP_NAME = Path(__file__).parent.resolve().stem
LOGGER = appLogger(APP_NAME).logger
LOGGER.addHandler(appLogger.console_handler())

RLOGGER = appLogger(f"R_{APP_NAME}").logger
RLOGGER.addHandler(appLogger.console_handler("\r"))