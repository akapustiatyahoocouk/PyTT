""" Defines the "PyTT Help Content" action. """
#   Python standard library
from typing import final
import os.path
import webbrowser

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from ..dialogs.AboutDialog import AboutDialog
from .ActionBase import ActionBase

##########
#   Public entities
@final
class HelpContentAction(ActionBase):
    """ The "PyTT Help Content" action. """

    ##########
    #   Construction
    def __init__(self):
        ActionBase.__init__(self, "Actions.HelpContent")

    ##########
    #   Action - Operations
    def execute(self, evt: ActionEvent) -> None:
        pytt_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        help_directory = os.path.abspath(os.path.join(pytt_directory, "Doc/Help"))
        print("Loading help from", help_directory)
        op = help_directory.replace("\\", "/") + "/index.html"
        webbrowser.open('file://' + op)

