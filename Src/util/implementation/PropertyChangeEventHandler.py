
#   Internal dependencies on modules within the same component
from .PropertyChangeEvent import PropertyChangeEvent

##########
#   Public entities
class PropertyChangeEventHandler:

    ##########
    #   Operations
    def on_property_change(self, evt: PropertyChangeEvent) -> None:
        #   TODO use property change event's "property name" property to
        #   try to locate the on_<property name>_change method and call it
        pass
