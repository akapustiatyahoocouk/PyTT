import sys
import tkinter as tk
import tkinter.ttk as ttk
from util.resources import *
from gui.AboutDialog import *
from gui.LoginDialog import *

import db.exceptions as dbex
import db.api as dbapi
import util.resources

class MainWindow(ttk.Frame):
    def __init__(self, window):
        window.geometry('600x400')
        self.popupButton = ttk.Button(window, text='popup', command=self.popup)
        self.quitButton = ttk.Button(window, text='quit', command=self.closeme)

        self.popupButton.pack()
        self.quitButton.pack()

        self.window = window
        #window.bind('<Key>', self.handle_key)
        
        #   Set up event handler
        self.__loggedIn = False     #   Needed to perform login-at-first-open
        
        self.window.bind('<Visibility>', self.__onInitialLogin)
    
    #   TODO kill off
    def handle_key(self, event):
        k = event.keysym
        print(f"got k: {k}")

    def popup(self):
        with AboutDialog(self.popupButton) as dlg:
            dlg.do_modal()

    def closeme(self):
        self.window.destroy()

    ##########
    #   Event handlers    
    def __onInitialLogin(self, *args):
        if not self.__loggedIn:
            self.__loggedIn = True
            with LoginDialog(self.window, 'asdf') as dlg:
                dlg.do_modal()
                if dlg.result is not LoginDialogResult.OK:
                    sys.exit()

if __name__ == '__main__':

    dbt = dbapi.DatabaseTypeRegistry.find_database_type('sqlite')
    dba = dbt.parse_database_address('123')
    print(dba.database_type.mnemonic)
    print(dba.database_type.display_name)
    print(dba.display_form)
    print(dba.external_form)
    print(str(dba))
    
    root = tk.Tk()
    root.wm_iconphoto(True, util.resources.UtilResources.PRODUCT_ICON)
    
    app = MainWindow(root)
    root.mainloop()
    print('exit main loop')            
