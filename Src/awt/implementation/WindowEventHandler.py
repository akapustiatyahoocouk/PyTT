
#   Internal dependencies on modules within the same component
from .WindowEventType import WindowEventType
from .WindowEvent import WindowEvent

##########
#   Public entities
class WindowEventHandler:

    ##########
    #   Operations
    def on_window_minimized(self, evt: WindowEvent) -> None:
        pass

    def on_window_maximized(self, evt: WindowEvent) -> None:
        pass

    def on_window_restored(self, evt: WindowEvent) -> None:
        pass

    def on_window_closing(self, evt: WindowEvent) -> None:
        pass
