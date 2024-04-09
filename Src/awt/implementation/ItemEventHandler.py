
#   Internal dependencies on modules within the same component
from .ItemEventType import ItemEventType
from .ItemEvent import ItemEvent

##########
#   Public entities
class ItemEventHandler:

    ##########
    #   Operations
    def on_item_selected(self, evt: ItemEvent) -> None:
        pass

    def on_item_unselected(self, evt: ItemEvent) -> None:
        pass

    def on_item_state_changed(self, evt: ItemEvent) -> None:
        pass
