from . import *
import ezdxf
from ezdxf.addons import Importer

#set up GDAL environment
VENV_PATH = os.environ["VIRTUAL_ENV"] 
OSGEO_PATH = VENV_PATH + "\Lib\site-packages\osgeo"

os.environ["PATH"] += ';'+ OSGEO_PATH
os.environ["GDAL_DATA"]= OSGEO_PATH+"\data\gdal"
os.environ["PROJ_LIB"]= OSGEO_PATH+"\data\proj"
os.environ["GDAL_UTILS"] = VENV_PATH+ "\Lib\site-packages\osgeo_utils"

def merge_dxfs(files,outf):
    target_drawing = ezdxf.new(units=1)
    for file in files:
        importer = Importer(ezdxf.readfile(file),target_drawing)
        importer.import_modelspace()
        importer.import_paperspace_layouts()
        importer.import_tables()
        importer.finalize()
    target_drawing.saveas(outf)

def gml2dxf(input_gml):

    output_dxf_pnd = input_gml.replace(".gml","_pnd.dxf")
    output_dxf_line = input_gml.replace(".gml","_line.dxf")
    output_dxf_point = input_gml.replace(".gml","_point.dxf")
    output_dxf_label = input_gml.replace(".gml","_label.dxf")

    gml2pnd_cmd = f'ogr2ogr -f DXF {output_dxf_pnd} {input_gml} -dialect sqlite -sql "SELECT ST_Union(ST_LinesFromRings(geometry)),\'PEN(c:#FF0000,w:5px)\' OGR_STYLE,\'Topo\' as Layer FROM Topo WHERE OBJECT=\'PND\' "'
    gml2line_cmd = f'ogr2ogr -f DXF {output_dxf_line} {input_gml} -dialect sqlite -sql "SELECT ST_Union(ST_LinesFromRings(geometry)),OGR_STYLE,\'Topo\' as Layer FROM Topo WHERE OBJECT!=\'PND\'"'
    gml2point_cmd = f'ogr2ogr -f DXF {output_dxf_point} {input_gml} -sql "SELECT geometry,\'Topo\' as Layer FROM Topo_point"'
    gml2label_cmd = f'ogr2ogr -f DXF {output_dxf_label} {input_gml} -sql "SELECT geometry,\'Topo\' as Layer FROM Label"'
    
    for cmd in [gml2pnd_cmd,gml2line_cmd,gml2point_cmd,gml2label_cmd]:
        os.system(cmd)

    input_drawings = [output_dxf_line,output_dxf_pnd,output_dxf_point,output_dxf_label]
    output_topo_dxf = input_gml.replace(".gml","_topo.dxf")
    
    try:
        merge_dxfs(input_drawings,output_topo_dxf)
    except Exception as e:
        print(f"Error:{e}")
        sys.exit()
    else:
        if os.path.exists(output_topo_dxf):
            for drawing in input_drawings:
                os.remove(drawing)

            print(f"Exported to {output_topo_dxf}")
            return output_topo_dxf


        

