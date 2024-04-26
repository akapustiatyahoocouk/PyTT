""" A handler of widget events, pre-categorized by event type. """

#   Internal dependencies on modules within the same component
from .WidgetEvent import WidgetEvent

##########
#   Public entities
class WidgetEventHandler:
    """ A handler of widget events, pre-categorized by event type. """

    ##########
    #   Operations
    def on_widget_shown(self, evt: WidgetEvent) -> None:
        """ Called after a widget has been shown. """
        pass

    def on_widget_hidden(self, evt: WidgetEvent) -> None:
        """ Called after a widget has been hidden. """
        pass

    def on_widget_moved(self, evt: WidgetEvent) -> None:
        """ Called after a widget has been moved. """
        pass

    def on_widget_resized(self, evt: WidgetEvent) -> None:
        """ Called after a widget has been resized. """
        pass
