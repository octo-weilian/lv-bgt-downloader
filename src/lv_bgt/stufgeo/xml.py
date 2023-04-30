from . import *

class XML:
    def __init__(self,filename):
        self.filename = filename
        
    def cleanup_element(element):
        element.clear()
        for ancestor in element.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
    
    def export_document(input_doc,output_file,cleanup_ns=True,indent_by=' '):
        if isinstance(input_doc,lxml.etree._Element):
            if cleanup_ns:
                etree.cleanup_namespaces(input_doc)
            tree = input_doc.getroottree()
            if indent_by:
                etree.indent(tree,indent_by)
                
            tree.write(output_file,pretty_print=True, encoding='UTF-8')
        
        if isinstance(input_doc,ezdxf.document.Drawing):
            input_doc.saveas(output_file)



