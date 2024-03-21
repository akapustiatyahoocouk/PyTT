
from typing import final
import sys

import tkinter as tk
import tkinter.ttk as ttk

import util.resources as utilres
import gui.dialogs as dialogs
import gui.frames as frames
import gui.events as events
from gui.root import GuiRoot
import workspace.api as wsapi

@final
class MainFrame(frames.TopFrame):
    """ The main frame of the "Admin" skin. """
    
    def __init__(self):
        super().__init__()
        self.__destroy_underway = False
        
        #  self.state('iconified') withdrawn
        #   Create controls
        self.__popupButton = ttk.Button(self, text='popup', command=self.__popup)
        self.__quitButton = ttk.Button(self, text='quit', command=self.destroy)

        self.__menu_bar = tk.Menu(self)
        self['menu'] = self.__menu_bar
        
        self.__file_menu = tk.Menu(tearoff=False)
        self.__help_menu = tk.Menu(tearoff=False)
        self.__menu_bar.add_cascade(label='File', underline=0, menu=self.__file_menu)

        self.__menu_bar.add_cascade(label='Help', underline=0, menu=self.__help_menu)
        self.__help_menu.add_command(label='About', underline=1, accelerator="^F", command=self.__popup)
        
        #   Set up control structure
        self.__popupButton.pack()
        self.__quitButton.pack()

        #   Set up event handlers
        self.__initialLoginPerformed = False
        self.bind('<Visibility>', self.__onInitialLogin)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        self.bind("<KeyPress>", self.keydown)
    
    def keydown(self, evt: tk.Event):
        print(evt)
        ke = events.KeyEvent(self, evt)
        #if evt.state == 'Control' and evt.keysym == 'F1':
        #if (evt.char is not None) and (len(evt.char) == 1):
        #    ch = evt.char[0]
        #    ke = events.KeyEvent(self, keycode=events.VirtualKey.from_tk_string(evt.keysym), keychar=ch, modifiers=evt.state)
        #else:
        #    ch = None
        #    ke = events.KeyEvent(self, keycode=events.VirtualKey.from_tk_string(evt.keysym), keychar=ch, modifiers=evt.state)
        print(ke)
        if ke.modifiers == events.InputEvent.MODIFIER_CONTROL and ke.keycode == events.VirtualKey.VK_F1:  # ctrl+F1
            self.__popup()
    
    ##########
    #   Properties
    @property
    def is_active(self) -> bool:
        return self.state() == 'normal'

    ##########
    #   Operations
    def activate(self):
        self.state('normal')
    
    def deactivate(self):
        self.state('withdrawn')

    def destroy(self):
        if not self.__destroy_underway:
            self.__destroy_underway =True
            self.protocol("WM_DELETE_WINDOW", lambda: None)
            for child in self.winfo_children():
                child.destroy()
            GuiRoot.tk.quit()
    
    ##########
    #   Implementation helpers    
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
            with dialogs.LoginDialog(self, 'asdf') as dlg:
                dlg.do_modal()
                if dlg.result is not dialogs.LoginDialogResult.OK:
                    sys.exit()
                wsapi.CurrentCredentials.set(dlg.credentials)
