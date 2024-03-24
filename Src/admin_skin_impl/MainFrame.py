
from typing import final
import sys

import tkinter as tk
import tkinter.ttk as ttk

import awt
import ws
import dialogs
import settings

@final
class MainFrame(awt.TopFrame):
    """ The main frame of the "Admin" skin. """
    
    def __init__(self):
        awt.TopFrame.__init__(self)
        
        self.__destroy_underway = False
        
        #   Create controls
        self.__popupButton = awt.Button(self, text="popup")
        self.__quitButton = awt.Button(self, text="quit")

        self.__menu_bar = tk.Menu(self)
        self["menu"] = self.__menu_bar
        
        self.__file_menu = tk.Menu(tearoff=False)
        self.__help_menu = tk.Menu(tearoff=False)
        self.__menu_bar.add_cascade(label='File', underline=0, menu=self.__file_menu)

        self.__menu_bar.add_cascade(label='Help', underline=0, menu=self.__help_menu)
        self.__help_menu.add_command(label='About', underline=1, accelerator="Ctrl+F1", command=self.__popup)
        
        #   Set up control structure
        self.__popupButton.pack()
        self.__quitButton.pack()

        #   Set up event handlers
        self.__initialLoginPerformed = False
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        self.__popupButton.add_action_event_listener(self.__popup)
        self.__quitButton.add_action_event_listener(self.__quit)
    
        self.add_key_event_listener(lambda e: print(e))

    ##########
    #   Properties
    @property
    def is_active(self) -> bool:
        return self.state() == "normal"

    ##########
    #   Operations
    def activate(self): # TODO replace with a setter property for "active" ?
        self.state("normal")
        self.tkraise()
        self.focus_force()
    
    def deactivate(self):   # TODO replace with a setter property for "active" ?
        self.state("withdrawn")

    def destroy(self):
        if not self.__destroy_underway:
            self.__destroy_underway =True
            self.protocol("WM_DELETE_WINDOW", lambda: None)
            awt.GuiRoot.tk.quit()
    
    ##########
    #   Implementation helpers    
    def __popup(self, *args) -> None:
        with dialogs.AboutDialog(self.__popupButton) as dlg:
            dlg.do_modal()

    def __quit(self, *args) -> None:
        self.destroy()
