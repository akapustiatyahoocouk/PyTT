#   Python standard library
from typing import final
import sys

#   Dependencies on other PyTT components
from util.api import *

##########
#   Public entities
@final
class CommandLine:
    """ The PyTT Client command line.. """
    
    ##########    
    #   Resources requiring lazy load
    __show_splash_screen = True
    
    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"

    ##########
    #   Properties
    @staticproperty    
    def show_splash_screen() -> bool:
        """ True if the splash screen should be displayed on 
            startup, False if not. """
        return CommandLine.__show_splash_screen
    
    ##########
    #   Operations
    @staticmethod
    def parse()-> None:
        """ Parses command line options as available in "sys.argv". """
        i = 1   #  to skip the program file name in [0]
        while i < len(sys.argv):
            if sys.argv[i] == "--splash":
                CommandLine.__show_splash_screen = True
                i += 1
            elif sys.argv[i] == "--nosplash":
                CommandLine.__show_splash_screen = False
                i += 1
            else:
                print("Invalid command line option ignored:", sys.argv[i])
                i += 1
