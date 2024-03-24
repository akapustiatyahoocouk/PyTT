#   Python standard library
from typing import final, Optional, Callable, Any, TypeAlias
from enum import Enum

#   Internal dependencies on modules within the same component
from util.implementation.Event import Event

##########
#   Public entities
class PropertyChangeEvent(Event):
    """ A "property change" event - signals that an observable
        property of some object has changed. """

    ##########
    #   Construction
    def __init__(self, source, affected_object: Any, changed_property: str):
        """
            Constructs the event.

            @param source:
                The event source, cannot be None.
            @param affected_object:
                The object whose property has changed; cannot be None.
            @param changed_property:
                The name of the property (of the affected_object) that has
                changed; cannot be None.
                It is recommended to name properties using "lower_case"
                naming scheme.
        """
        Event.__init__(self, source)

        assert affected_object is not None
        assert isinstance(changed_property, str)

        self.__affected_object = affected_object
        self.__changed_property = changed_property

    ##########
    #   object
    def __str__(self) -> str:
        result = ""
        if self.source is not None:
            result += "source="
            result += str(self.source)
        return ("PropertyChangeEvent(" + result + "," +
                repr(self.__affected_object) + "," +
                self.__changed_property + ")")

    ##########
    #   Properties
    @property
    def affected_object(self) -> Any:
        """ The object whose property has changed; cannot be None. """
        return self.__affected_object

    @property
    def changed_property(self) -> str:
        """ The name of the property (of the affected_object) that
            has changed; cannot be None. """
        return self.__changed_property
