""" PyTT Client General/Appearance preferences. """
#   Python standard library
import tkinter as tk

#   Dependencies on other PyTT components
from awt.interface.api import *
from util.interface.api import *

#   Internal dependencies on modules within the same component
from ..resources.ClientResources import ClientResources

##########
#   Public entities
class GeneralAppearancePreferences(Preferences):
    """ The "General/Appearance" preferences. """

    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : Preferences = None

    def __init__(self):
        assert GeneralAppearancePreferences.__instance_acquisition_in_progress, "Use GeneralAppearancePreferences.instance instead"
        Preferences.__init__(self, GeneralPreferences.instance, "Appearance")

    @staticproperty
    def instance() -> Preferences:
        """
            Returns one and only instance of this class, creating
            it on the first call.

            @return:
                The one and only instance of this class.
        """
        if GeneralAppearancePreferences.__instance is None:
            GeneralAppearancePreferences.__instance_acquisition_in_progress = True
            GeneralAppearancePreferences.__instance = GeneralAppearancePreferences()
            GeneralAppearancePreferences.__instance_acquisition_in_progress = False
        return GeneralAppearancePreferences.__instance

    ##########
    #   Preferences - Properties
    @property
    def display_name(self) -> str:
        return 'Appearance'

    @property
    def sort_order(self) -> Optional[int]:
        return 0

    ##########
    #   Preferences - Operations
    def create_editor(self, parent: tk.BaseWidget) -> tk.BaseWidget:
        assert isinstance(parent, tk.BaseWidget)
        return _Editor(parent)

    ##########
    #   Properties
    @property
    def use_last_login(self) -> BoolPreference:
        return self.__use_last_login

    @property
    def restore_workspace(self) -> BoolPreference:
        return self.__restore_workspace

GeneralAppearancePreferences.instance #   to instantiate it

##########
#   Implementation helpers
class _Editor(Panel):
    def __init__(self, parent: tk.BaseWidget, **kwargs):
        Panel.__init__(self, parent, **kwargs)

        #   Create controls        
        
        #   Set up control structure

        #   Adjust controls

        #   Set up event handlers

    ##########
    #   Event handlers
