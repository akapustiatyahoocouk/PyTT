
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *

##########
#   Public entities
@final
class MainFrame(TopFrame):
    """ The main frame of the "Admin" skin. """
    
    def __init__(self):
        TopFrame.__init__(self)

        self.__destroy_underway = False
        
        from gui.implementation.actions.ActionSet import ActionSet
        action_set = ActionSet()
        
        file_menu = Submenu('File', hotkey='F')
        fi1 = file_menu.items.append(action_set.exit)
        fi2 = file_menu.items.append('Exit&1')
        fi3 = file_menu.items.append('Exit&2')
        fi4 = file_menu.items.append('Exit&3')
        file_menu.items.remove_at(2)
        
        help_menu = Submenu('Help', hotkey='H')
        help_menu.items.append('Help', hotkey="H")
        ha = help_menu.items.append(action_set.about)
        hi = help_menu.items.append('&Index')
        help_menu.items.append('&Search').enabled = False

        #action_set.about.enabled = False
        #action_set.about.name = 'About PyTT... 1234567890'
        #action_set.about.hotkey = "A"
        hi.shortcut = KeyStroke(VirtualKey.VK_F1, InputEventModifiers.ALT)
        action_set.about.shortcut = KeyStroke(VirtualKey.VK_F1)
        
        menu_bar = MenuBar()
        menu_bar.items.append(file_menu)
        menu_bar.items.append(help_menu)

        mb1 = self.menu_bar
        self.menu_bar = menu_bar
        mb2 = self.menu_bar

        #   Create controls
        self.__aboutButton = Button(self, action=action_set.about)
        self.__quitButton = Button(self, action=action_set.exit)

        #self.menu_bar = None

        #self.__menu_bar = tk.Menu(self)
        #self["menu"] = self.__menu_bar
        
        #self.__file_menu = tk.Menu(tearoff=False)
        #self.__help_menu = tk.Menu(tearoff=False)
        #self.__menu_bar.add_cascade(label='File', underline=0, menu=self.__file_menu)

        #self.__menu_bar.add_cascade(label='Help', underline=0, menu=self.__help_menu)
        #self.__help_menu.add_command(label='About', underline=1, accelerator="Ctrl+F1", command=self.__popup)
        
        #   Set up control structure
        self.__aboutButton.pack()
        self.__quitButton.pack()

        #   Set up event handlers
        self.__initialLoginPerformed = False
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
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
            GuiRoot.tk.quit()
    
    ##########
    #   Implementation helpers    
    def __quit(self, *args) -> None:
        self.destroy()
