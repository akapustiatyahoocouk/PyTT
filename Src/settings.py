from typing import final
from abc import ABC

__ini_file_path = pathlib.Path.home() / ".pytt.ini"
__config = configparser.ConfigParser()
__config.read(__ini_file_path)

@final
class Settings(ABC):

    ##########
    #   Implementation details
    
    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"
