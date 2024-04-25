""" An interface to an agent handling ItemEvents. """
#   Internal dependencies on modules within the same component
from .ItemEvent import ItemEvent

##########
#   Public entities
class ItemEventHandler:
    """ An interface to an agent handling ItemEvents. """
    
    ##########
    #   Operations
    def on_item_selected(self, evt: ItemEvent) -> None:
        """
            Called when an item within a container has been selected. 
            
            @param evt:
                The event describing the change.
        """
        pass

    def on_item_unselected(self, evt: ItemEvent) -> None:
        """
            Called when an item within a container has been unselected. 
            
            @param evt:
                The event describing the change.
        """
        pass

    def on_item_state_changed(self, evt: ItemEvent) -> None:
        """
            Called when the state of an item within a container has changed. 
            
            @param evt:
                The event describing the change.
        """
        pass
