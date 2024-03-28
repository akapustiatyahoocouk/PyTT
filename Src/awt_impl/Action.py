from typing import Optional
from abc import ABC, abstractmethod

from util import ABCWithConstants
import awt_impl.KeyStroke
import awt_impl.ActionEvent
import awt_impl.PropertyChangeEventProcessorMixin
import awt_impl.PropertyChangeEvent

class Action(ABCWithConstants,
             awt_impl.PropertyChangeEventProcessorMixin.PropertyChangeEventProcessorMixin):
    """ A generic "action" is an agent that encapsulates properties 
        of an activity that can be triggered by the user. """
        
    ##########
    #   Constants (observable property names)
    NAME_PROPERTY_NAME = "name"
    """ The name of the "name" property of an Action. """
    
    DESCRIPTION_PROPERTY_NAME = "description"
    """ The name of the "description" property of an Action. """

    SHORTCUT_PROPERTY_NAME = "shortcut"
    """ The name of the "shortcut" property of an Action. """
    
    ##########
    #   Construction
    def __init__(self, 
                 name: str, 
                 description: Optional[str] = None, 
                 shortcut: Optional[awt_impl.KeyStroke.KeyStroke] = None) -> None:
        """
            Constructs the action.
            
            @param name:
                The short user-readable name of the action.
            @param description:
                The 1-line user-readable description of the action (optional).
            @param shortcut:
                The keyboard shortcut of the action (optional).
        """
        ABCWithConstants.__init__(self)
        awt_impl.PropertyChangeEventProcessorMixin.PropertyChangeEventProcessorMixin.__init__(self)

        assert isinstance(name, str)
        assert (description is None) or isinstance(description, str)
        assert (shortcut is None) or isinstance(shortcut, awt_impl.KeyStroke.KeyStroke)

        self.__name = name
        self.__description = description
        self.__shortcut = shortcut

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
            self.__name
            #   Notify interested listeners
            evt = awt_impl.PropertyChangeEvent.PropertyChangeEvent(self, self, Action.NAME_PROPERTY_NAME)
            self._process_property_change_event(evt)

    @property   # TODO add setter
    def description(self) -> Optional[str]:
        """ The 1-line user-readable description of the action (optional, can be None). """
        return self.__description
    
    @property   # TODO add setter
    def shortcut(self) -> Optional[awt_impl.KeyStroke.KeyStroke]:    
        """ The keyboard shortcut of the action (optional, can be None). """
        return self.__shortcut

    ##########
    #   Operations
    @abstractmethod
    def execute(self, evt: awt_impl.ActionEvent) -> None:
        """ 
            Called by framework to "execute" this action.
            
            @param evt:
                The ActionEvent that has triggered the execution of this action.
        """
        raise NotImplementedError()
