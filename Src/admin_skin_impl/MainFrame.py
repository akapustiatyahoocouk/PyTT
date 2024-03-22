
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
        self.__popupButton = ttk.Button(self, text="popup", command=self.__popup)
        self.__quitButton = ttk.Button(self, text="quit", command=self.destroy)

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
        self.bind("<Visibility>", self.__onInitialLogin)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        self.bind("<KeyPress>", self.keydown)
        self.bind("<KeyRelease>", self.keyup)
    
        self.add_key_event_listener(lambda e: print(e))
        self.add_key_event_listener(self.xxx)
        
    def xxx(self, e):
        print('XXX:', e)
        
    def keydown(self, evt: tk.Event):
        #print(evt)
        ke = awt.KeyEvent(self, awt.KeyEventType.KEY_DOWN, evt)
        self._process_key_event(ke)
        if ke.keychar is not None:
            ce = awt.KeyEvent(self, awt.KeyEventType.KEY_CHAR, evt)
            self._process_key_event(ce)
        if ke.modifiers == awt.InputEvent.MODIFIER_CONTROL and ke.keycode == awt.VirtualKey.VK_F1:  # ctrl+F1
            self.__popup()
        self.remove_key_event_listener(self.xxx)
    
    def keyup(self, evt: tk.Event):
        #print(evt)
        ke = awt.KeyEvent(self, awt.KeyEventType.KEY_UP, evt)
        self._process_key_event(ke)

    ##########
    #   Properties
    @property
    def is_active(self) -> bool:
        return self.state() == "normal"

    ##########
    #   Operations
    def activate(self):
        self.state("normal")
    
    def deactivate(self):
        self.state("withdrawn")

    def destroy(self):
        if not self.__destroy_underway:
            self.__destroy_underway =True
            self.protocol("WM_DELETE_WINDOW", lambda: None)
            for child in self.winfo_children():
                child.destroy()
            awt.GuiRoot.tk.quit()
    
    ##########
    #   Implementation helpers    
    def __popup(self) -> None:
        with dialogs.AboutDialog(self.__popupButton) as dlg:
            dlg.do_modal()

    ##########
    #   Event handlers    
    def __onInitialLogin(self, *args) -> None:
        if (ws.CurrentCredentials.get() is None) and (not self.__initialLoginPerformed):
            #   Need the (not self.__initialLoginPerformed) guard because the 
            #   frame will generate several <Visibility> events when shown
            self.__initialLoginPerformed = True
            with dialogs.LoginDialog(self, 'asdf') as dlg:
                dlg.do_modal()
                if dlg.result is not dialogs.LoginDialogResult.OK:
                    sys.exit()
                ws.CurrentCredentials.set(dlg.credentials)
