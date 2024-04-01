"""
    Defines the Action API.
"""
#   Python standard library
from typing import Optional
from abc import abstractmethod
import tkinter as tk

#   Dependencies on other PyTT components
from util.api import *

#   Internal dependencies on modules within the same component
from awt.KeyStroke import KeyStroke
from awt.ActionEvent import ActionEvent
from awt.PropertyChangeEventProcessorMixin import PropertyChangeEventProcessorMixin
from awt.PropertyChangeEvent import PropertyChangeEvent

class Action(ABCWithConstants, PropertyChangeEventProcessorMixin):
    """ A generic "action" is an agent that encapsulates properties 
        of an activity that can be triggered by the user. """

    ##########
    #   Constants (observable property names)
    NAME_PROPERTY_NAME = "name"
    """ The name of the "name: str" property of an Action. """

    HOTKEY_PROPERTY_NAME = "hotkey"
    """ The name of the "hotkey: str" property of an Action. """

    DESCRIPTION_PROPERTY_NAME = "description"
    """ The name of the "description: str" property of an Action. """

    SHORTCUT_PROPERTY_NAME = "shortcut"
    """ The name of the "shortcut: KeyStroke" property of an Action. """

    ENABLED_PROPERTY_NAME = "enabled"
    """ The name of the "enabled: bool" property of an Action. """

    SMALL_IMAGE_PROPERTY_NAME = "small_image"
    """ The name of the "small_image: tk.PhotoImage" property of an Action. """

    LARGE_IMAGE_PROPERTY_NAME = "large_image"
    """ The name of the "large_image: tk.PhotoImage" property of an Action. """

    ##########
    #   Construction
    def __init__(self,
                 name: str,
                 hotkey: Optional[str] = None,
                 description: Optional[str] = None,
                 shortcut: Optional[KeyStroke] = None,
                 enabled: Optional[bool] = True,
                 small_image: Optional[tk.PhotoImage] = None,
                 large_image: Optional[tk.PhotoImage] = None) -> None:
        """
            Constructs the action.
            
            @param name:
                The short user-readable name of the action; canot be None.
            @param hotkey:
                The character to display as underlined when the action name
                appears in e.g. menu item, buttion text, etc. (optional, can be None).
            @param description:
                The 1-line user-readable description of the action (optional, can be None).
            @param shortcut:
                The keyboard shortcut of the action (optional, can be None).
            @param enabled:
                True to construct an initially enabled property, False to
                construct an initially disabled property (default True,
                cannot be None).
            @param small_image:
                The small (typically 16x16) image representing this action
                (optional, can be None).
            @param large_image:
                The large (typically 32x32) image representing this action
                (optional, can be None).
        """
        ABCWithConstants.__init__(self)
        PropertyChangeEventProcessorMixin.__init__(self)

        assert isinstance(name, str)
        assert (hotkey is None) or isinstance(hotkey, str)
        assert (description is None) or isinstance(description, str)
        assert (shortcut is None) or isinstance(shortcut, KeyStroke)
        assert isinstance(enabled, bool)
        assert (small_image is None) or isinstance(small_image, tk.PhotoImage)
        assert (large_image is None) or isinstance(large_image, tk.PhotoImage)

        self.__name = name
        self.__hotkey = None if hotkey is None or len(hotkey) != 1 else hotkey
        self.__description = description
        self.__shortcut = shortcut
        self.__enabled = enabled
        self.__small_image = small_image
        self.__large_image = large_image

    ##########
    #   Properties
    @property
    def name(self) -> str:
        """ The short user-readable name of the action; never None. """
        return self.__name

    @name.setter
    def name(self, new_name: str):
        """ 
            Sets the short user-readable name of the action.
            
            @param new_name:
                The new short user-readable name of the action; cannot be None.
        """
        assert isinstance(new_name, str)
        if new_name != self.__name:
            self.__name = new_name
            #   Notify interested listeners
            evt = PropertyChangeEvent(self, self, Action.NAME_PROPERTY_NAME)
            self._process_property_change_event(evt)

    @property
    def hotkey(self) -> str:
        """ The character to display as underlined when the action name
            appears in e.g. menu item, buttion text, etc. (optional, can be None). """
        return self.__hotkey

    @hotkey.setter
    def hotkey(self, new_hotkey: str):
        """ 
            Sets the hotkey of the action.
            
            @param new_hotkey:
                The new hotkey of the action; None for none.
        """
        assert (new_hotkey is None) or isinstance(new_hotkey, str)
        if new_hotkey != self.__hotkey:
            self.__hotkey = new_hotkey
            #   Notify interested listeners
            evt = PropertyChangeEvent(self, self, Action.HOTKEY_PROPERTY_NAME)
            self._process_property_change_event(evt)

    @property   # TODO add setter
    def description(self) -> Optional[str]:
        """ The 1-line user-readable description of the action (optional, can be None). """
        return self.__description

    @property   # TODO add setter
    def shortcut(self) -> Optional[KeyStroke]:
        """ The keyboard shortcut of the action (optional, can be None). """
        return self.__shortcut

    @shortcut.setter
    def shortcut(self, new_shortcut: Optional[KeyStroke]):
        """ Sets the kryboard shortcut of this Action, None == bo shortcut. """
        assert (new_shortcut is None) or isinstance(new_shortcut, KeyStroke)
        if new_shortcut != self.__shortcut:
            self.__shortcut = new_shortcut
            #   Notify interested listeners
            evt = PropertyChangeEvent(self, self, Action.SHORTCUT_PROPERTY_NAME)
            self._process_property_change_event(evt)

    @property   # TODO add setter
    def enabled(self) -> bool:
        """ True if this action is enabled, false if disabled; cannot be None. """
        return self.__enabled

    @enabled.setter
    def enabled(self, new_enabled: bool):
        """ True to enable this action, false to disable; cannot be None. """
        assert isinstance(new_enabled, bool)
        if new_enabled != self.__enabled:
            self.__enabled = new_enabled
            #   Notify interested listeners
            evt = PropertyChangeEvent(self, self, Action.ENABLED_PROPERTY_NAME)
            self._process_property_change_event(evt)

    @property   # TODO add setter
    def small_image(self) -> Optional[tk.PhotoImage]:
        """ The small (typically 16x16) image representing this action
            (optional, can be None). """
        return self.__small_image

    @property   # TODO add setter
    def large_image(self) -> Optional[tk.PhotoImage]:
        """ The large (typically 32x32) image representing this action
            (optional, can be None). """
        return self.__large_image

    ##########
    #   Operations
    @abstractmethod
    def execute(self, evt: ActionEvent) -> None:
        """ 
            Called by framework to "execute" this action.
            
            @param evt:
                The ActionEvent that has triggered the execution of this action.
        """
        raise NotImplementedError()
