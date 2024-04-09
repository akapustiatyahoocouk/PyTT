
#   Internal dependencies on modules within the same component
from .WidgetEventType import WidgetEventType
from .WidgetEvent import WidgetEvent

##########
#   Public entities
class WidgetEventHandler:

    ##########
    #   Operations
    def on_widget_shown(self, evt: WidgetEvent) -> None:
        pass

    def on_widget_hidden(self, evt: WidgetEvent) -> None:
        pass

    def on_widget_moved(self, evt: WidgetEvent) -> None:
        pass

    def on_widget_resized(self, evt: WidgetEvent) -> None:
        pass
