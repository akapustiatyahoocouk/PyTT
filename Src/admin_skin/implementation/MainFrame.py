
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from admin_skin.resources.AdminSkinResources import AdminSkinResources

##########
#   Public entities
@final
class MainFrame(TopFrame):
    """ The main frame of the "Admin" skin. """
    
    def __init__(self):
        TopFrame.__init__(self)

        self.__destroy_underway = False
        
        from gui.implementation.actions.ActionSet import ActionSet
        self.__action_set = ActionSet()
        
        file_menu = ResourceAwareSubmenu(AdminSkinResources.factory,
                                         DefaultLocaleProvider.instance,
                                         "FileMenu")
        fi1 = file_menu.items.append(self.__action_set.exit)
        fi2 = file_menu.items.append('Exit&1')
        fi3 = file_menu.items.append('Exit&2')
        fi4 = file_menu.items.append('Exit&3')
        file_menu.items.remove_at(2)
        
        help_menu = ResourceAwareSubmenu(AdminSkinResources.factory,
                                         DefaultLocaleProvider.instance,
                                         "HelpMenu")
        help_menu.items.append('Help', hotkey="H")
        help_menu.items.append('Search', hotkey="S").enabled = False
        help_menu.items.append('Index', hotkey="I")
        help_menu.items.append(self.__action_set.about)
        
        menu_bar = MenuBar()
        menu_bar.items.append(file_menu)
        menu_bar.items.append(help_menu)

        self.menu_bar = menu_bar

        #   Create controls
        self.__aboutButton = Button(self, action=self.__action_set.about)
        self.__quitButton = Button(self, action=self.__action_set.exit)

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
            evt = ActionEvent(self)
            self.__action_set.exit.execute(evt)
            #GuiRoot.tk.quit()
    
    ##########
    #   Implementation helpers    
    def __quit(self, *args) -> None:
        self.destroy()
