from app import *
from lxml import etree
import numpy as np
import pygeos
from app.models.gml import GML
import copy

#stufgeo elements
STUFGEO_NS = "{http://www.egem.nl/StUF/StUF0301}"
STUFGEO_ENT_TYPE = STUFGEO_NS + "entiteittype"

#imgeo elements
IMGEO_NS = "{http://www.geostandaarden.nl/imgeo/2.1/stuf-imgeo}"
IMGEO_STUUR = IMGEO_NS + "stuurgegevens"
IMGEO_BERICHT = IMGEO_NS + "mutatiebericht"
IMGEO_OBJ = IMGEO_NS + "object"

IMGEO_ORL = IMGEO_NS+"openbareRuimteNaam"
IMGEO_HOUSENR = IMGEO_NS + "nummeraanduidingreeks"
IMGEO_PBP = IMGEO_NS+"geometrie"
IMGEO_PLUSTYPE = IMGEO_NS+"plus-type"

#gml elements
GML_NS = "{http://www.opengis.net/gml}"
GML_POS = GML_NS+"pos"
GML_POSLIST = GML_NS+"posList"
GML_POINT = GML_NS +"Point"

#xpath expressions
xp_geometrie2d = ".//*[contains(name(),'geometrie2d')]"
xp_geometrie = ".//*[contains(name(),'geometrie')]"
xp_pos = ".//*[contains(name(),'pos')]"
xp_poslist = ".//*[contains(name(),'posList')]"
xp_lokaalid = ".//*[contains(name(),'lokaalID')]"
xp_gml = ".//*[contains(name(),'gml')]"
xp_tekst = ".//*[local-name()='tekst']"
xp_point = ".//*[local-name()='Point']"
xp_hoek = ".//*[local-name()='hoek']"


