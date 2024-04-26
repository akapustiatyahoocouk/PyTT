""" A handler of window events, pre-categorized by event type. """

#   Internal dependencies on modules within the same component
from .WindowEvent import WindowEvent

##########
#   Public entities
class WindowEventHandler:
    """ A handler of window events, pre-categorized by event type. """

    ##########
    #   Operations
    def on_window_minimized(self, evt: WindowEvent) -> None:
        """
            Called when a Window has been minimized.

            @param evt:
                The WindowEvent descrining the window state change.
        """
        pass

    def on_window_maximized(self, evt: WindowEvent) -> None:
        """
            Called when a Window has been maximized.

            @param evt:
                The WindowEvent descrining the window state change.
        """
        pass

    def on_window_restored(self, evt: WindowEvent) -> None:
        """
            Called when a Window has been restored.

            @param evt:
                The WindowEvent descrining the window state change.
        """
        pass

    def on_window_closing(self, evt: WindowEvent) -> None:
        """
            Called when user attempts to close the window via UI means.
            Mark the "evt" as processed to stop the window from closing.

            @param evt:
                The WindowEvent descrining the window state change.
        """
        pass
