""" Implements "About PyTT" modal dialog. """
#   Python standard library
from typing import final
from enum import Enum
import tkinter as tk
import idlelib.redirector as rd

#   Dependencies on other PyTT components
from awt.interface.api import *
from util.interface.api import *

#   Internal dependencies on modules within the same component
from gui.resources.GuiResources import GuiResources

##########
#   Public entities
@final
class LicenseDialog(Dialog):
    """ The modal "License" dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget):
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("LicenseDialog.Title"))

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__license_text_area = TextArea(self.__controls_panel,
                                            height=20, width=80,
                                            text=UtilResources.string("PyTT.License"))    #   TODO ScrolledTextArea!

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("LicenseDialog.OkButton.Text"),
            image=GuiResources.image("LicenseDialog.OkButton.Icon"))

        #   Adjust controls
        self.__license_text_area.readonly = True

        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__license_text_area.pack(fill=tk.BOTH, padx=0, pady=0)
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__ok_button.pack(side=tk.RIGHT, padx=0, pady=0)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__ok_button

        self.__ok_button.add_action_listener(self.__on_ok)

        #   Done
        self.wait_visibility()
        self.center_in_parent()

    ##########
    #   Implementation helpers
    def __on_ok(self, evt = None) -> None:
        self.end_modal()
