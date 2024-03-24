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

        self.__ui_locale = LocalePreference("UiLocale", Locale.default)

        self.add_preference(self.__ui_locale)

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
    def apply(self) -> None:
        super().apply()
        Locale.default = self.__ui_locale.value
        
    ##########
    #   Preferences - Operations
    def create_editor(self, parent: tk.BaseWidget) -> tk.BaseWidget:
        assert isinstance(parent, tk.BaseWidget)
        return _Editor(parent)

    ##########
    #   Properties
    @property
    def ui_locale(self) -> LocalePreference:
        return self.__ui_locale

GeneralAppearancePreferences.instance #   to instantiate it

##########
#   Implementation helpers
class _Editor(Panel):
    def __init__(self, parent: tk.BaseWidget, **kwargs):
        Panel.__init__(self, parent, **kwargs)

        #   Create controls
        self.__language_label = Label(self, text=ClientResources.string("GeneralAppearancePreferences.LanguageLabel.Text"))
        self.__language_combo_box = ComboBox(self)

        #   Adjust controls
        all_locales = list(LocalizableSubsystem.all_supported_locales())
        all_locales.sort(key=lambda l: repr(l))

        self.__language_combo_box.editable = False
        for locale in all_locales:
            item = self.__language_combo_box.items.add(str(locale), tag=locale)

        locale_to_select = Locale.default
        while self.__language_combo_box.selected_item is None:
            for item in self.__language_combo_box.items:
                if item.tag == locale_to_select:
                    self.__language_combo_box.selected_item = item
                    break
            locale_to_select = locale_to_select.parent

        #   Set up control structure
        self.__language_label.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__language_combo_box.grid(row=0, column=1, padx=2, pady=2, sticky="W")

        #   Set up event handlers
        self.__language_combo_box.add_item_listener(self.__language_combo_box_item_changed)

    ##########
    #   Event handlers
    def __language_combo_box_item_changed(self, evt: ItemEvent) -> None:
        assert isinstance(evt, ItemEvent)
        new_locale = self.__language_combo_box.selected_item.tag
        GeneralAppearancePreferences.instance.ui_locale.value = new_locale
