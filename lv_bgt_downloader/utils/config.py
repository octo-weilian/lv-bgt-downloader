from . import *

class appConfig:
    def __init__(self,config_file):
        self.config_file = config_file
        self.parser = self.read_config()
        
    def get(self,section,option):
        return self.parser[section][option]
    
    def read_config(self):
        if Path(self.config_file).exists():
            parser = ConfigParser()
            parser.read(self.config_file)
            return parser
        else:
            return None
            
    def save_config(self,section,values):
        options = [option for option,_ in self.parser.items(section)]
        for i in range(len(options)):
            self.parser.set(section, options[i], str(values[i]))

        with open(self.config_file, 'w+') as dst:
            self.parser.write(dst)
       