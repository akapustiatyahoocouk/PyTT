
from time import sleep
from typing import final

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from admin_skin.resources.AdminSkinResources import AdminSkinResources

##########
#   Public entities
@final
class AdminSkinMainFrame(TopFrame):
    """ The main frame of the "Admin" skin. """

    def __init__(self):
        TopFrame.__init__(self)
        self.title(AdminSkinResources.string("MainFrame.Title"))

        from gui.implementation.actions.ActionSet import ActionSet
        self.__action_set = ActionSet()

        file_menu = ResourceAwareSubmenu(AdminSkinResources.factory,
                                         DefaultLocaleProvider.instance,
                                         "FileMenu")
        file_menu.items.add(self.__action_set.create_workspace)
        file_menu.items.add(self.__action_set.open_workspace)
        file_menu.items.add_seperator()
        file_menu.items.add(self.__action_set.close_workspace)
        file_menu.items.add_seperator()
        file_menu.items.add(self.__action_set.destroy_workspace)
        file_menu.items.add_seperator()
        file_menu.items.add(self.__action_set.exit)

        help_menu = ResourceAwareSubmenu(AdminSkinResources.factory,
                                         DefaultLocaleProvider.instance,
                                         "HelpMenu")
        help_menu.items.add('Help', hotkey="H")
        help_menu.items.add('Search', hotkey="S").enabled = False
        help_menu.items.add('Index', hotkey="I")
        help_menu.items.add_seperator()
        help_menu.items.add(self.__action_set.about)

        menu_bar = MenuBar()
        menu_bar.items.add(file_menu)
        menu_bar.items.add(help_menu)

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
        self.protocol("WM_DELETE_WINDOW", self.destroy) # TODO move handling to TopFrame

        self.add_key_listener(lambda e: print(e))
        
        DefaultLocaleProvider.instance.add_property_change_listener(self.__on_locale_changed)

    ##########
    #   Properties
    @property
    def is_active(self) -> bool:
        return self.window_state == WindowState.NORMAL

    ##########
    #   Operations
    def activate(self): # TODO replace with a setter property for "active" ?
        self.window_state = WindowState.NORMAL
        #TODO kill off when confirmed not needed self.tkraise()
        self.focus_force()

    def deactivate(self):   # TODO replace with a setter property for "active" ?
        self.window_state = WindowState.WITHDRAWN

    def destroy(self):
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.__action_set.exit.execute(ActionEvent(self))

    ##########
    #   Implementation helpers
    def __quit(self, *args) -> None:
        self.destroy()

    ##########
    #   Event listeners    
    def __on_locale_changed(self, evt) -> None:
        self.title(AdminSkinResources.string("MainFrame.Title"))
