from app import *

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
GML_ARC = GML_NS + "Arc"
GML_EXTERIOR = GML_NS + "exterior"
GML_INTERIOR = GML_NS + "interior"

#xpath expressions
XP_GEOMETRIE2D = ".//*[contains(name(),'geometrie2d')]"
XP_GEOMETRIE = ".//*[contains(name(),'geometrie')]"
XP_POS = ".//*[contains(name(),'pos')]"
XP_POSLIST = ".//*[contains(name(),'posList')]"
XP_LOKAALID = ".//*[contains(name(),'lokaalID')]"
XP_GML = ".//*[contains(name(),'gml')]"
XP_TEKST = ".//*[local-name()='tekst']"
XP_POINT = ".//*[local-name()='Point']"
XP_HOEK = ".//*[local-name()='hoek']"
XP_ARC = ".//*[contains(name(),'Arc')]"