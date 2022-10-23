from . import *

FORMAT  = '%(asctime)s %(funcName)s [%(levelname)s] - %(message)s'
FORMATE_DATE = '%d-%b %H:%M:%S'
FORMATTER = logging.Formatter(fmt =FORMAT,datefmt=FORMATE_DATE)

class appLogger:
    def __init__(self,name):
        self.logger_name = name
        self.logger = self.get_logger()
        
    @staticmethod
    def console_handler(terminator=None):
        handler = StreamHandler(sys.stdout)
        if terminator:
            handler.terminator = terminator
        handler.setFormatter(FORMATTER)
        return handler
        
    @staticmethod
    def file_handler(log_file):
        handler = RotatingFileHandler(log_file,maxBytes=1e3,backupCount=1,mode='w+')
        handler.setFormatter(FORMATTER)
        return handler

    def get_logger(self):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        return logger
