
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

        file_menu = awt.Submenu('&File')
        fi1 = file_menu.items.append('E&xit')
        fi2 = file_menu.items.append('Exit&1')
        fi3 = file_menu.items.append('Exit&2')
        fi4 = file_menu.items.append('Exit&3')
        file_menu.items.remove_at(2)
        
        help_menu = awt.Submenu('&Help')
        ha = help_menu.items.append('A&bout')
        ha.add_action_listener(self.__popup)

        menu_bar = awt.MenuBar()
        menu_bar.items.append(file_menu)
        menu_bar.items.append(help_menu)

        mb1 = self.menu_bar
        self.menu_bar = menu_bar
        mb2 = self.menu_bar
        #self.menu_bar = None

        #self.__menu_bar = tk.Menu(self)
        #self["menu"] = self.__menu_bar
        
        #self.__file_menu = tk.Menu(tearoff=False)
        #self.__help_menu = tk.Menu(tearoff=False)
        #self.__menu_bar.add_cascade(label='File', underline=0, menu=self.__file_menu)

        #self.__menu_bar.add_cascade(label='Help', underline=0, menu=self.__help_menu)
        #self.__help_menu.add_command(label='About', underline=1, accelerator="Ctrl+F1", command=self.__popup)
        
        #   Set up control structure
        self.__popupButton.pack()
        self.__quitButton.pack()

        #   Set up event handlers
        self.__initialLoginPerformed = False
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        self.__popupButton.add_action_listener(self.__popup)
        self.__quitButton.add_action_listener(self.__quit)
    
        self.add_key_listener(lambda e: print(e))

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
