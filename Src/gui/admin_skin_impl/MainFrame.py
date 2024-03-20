
from typing import final
import sys

import tkinter as tk
import tkinter.ttk as ttk

import util.resources as utilres
import gui.dialogs as dialogs
import workspace.api as wsapi

@final
class MainFrame(tk.Frame):
    """ The main frame of the "Admin" skin. """
    
    def __init__(self):
        self.__tk = tk.Tk()
        self.__tk.title(utilres.UtilResources.PRODUCT_NAME)
        self.__tk.wm_iconphoto(True, utilres.UtilResources.PRODUCT_ICON)
        self.__tk.geometry('600x400')

        #   Create controls
        self.__popupButton = ttk.Button(self.__tk, text='popup', command=self.__popup)
        self.__quitButton = ttk.Button(self.__tk, text='quit', command=self.destroy)

        #   Set up control structure
        self.__popupButton.pack()
        self.__quitButton.pack()

        #   Set up event handlers
        self.__initialLoginPerformed = False
        self.__tk.bind('<Visibility>', self.__onInitialLogin)
        self.__tk.protocol("WM_DELETE_WINDOW", self.destroy)

    ##########
    #   Properties
    @property
    def is_destroyed(self):
        return self.__tk is None

    ##########
    #   Operations
    def activate(self):
        if self.__tk is not None:
            self.__tk.tkraise()
            self.__tk.focus_force()
    
    def destroy(self):
        if self.__tk is not None:
            self.__tk.destroy()
            self.__tk = None
            
    ##########
    #   Implementation helpers    
    @property
    def tk(self):   #   seems to be needed by tkinter
        return self.__tk

    def __popup(self) -> None:
        with dialogs.AboutDialog(self.__popupButton) as dlg:
            dlg.do_modal()

    ##########
    #   Event handlers    
    def __onInitialLogin(self, *args) -> None:
        if (wsapi.CurrentCredentials.get() is None) and (not self.__initialLoginPerformed):
            #   Need the (not self.__initialLoginPerformed) guard because the 
            #   frame will generate several <Visibility> events when shown
            self.__initialLoginPerformed = True
            with dialogs.LoginDialog(self.tk, 'asdf') as dlg:
                dlg.do_modal()
                if dlg.result is not dialogs.LoginDialogResult.OK:
                    sys.exit()
                wsapi.CurrentCredentials.set(dlg.credentials)
