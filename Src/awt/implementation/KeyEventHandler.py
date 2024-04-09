
#   Internal dependencies on modules within the same component
from .KeyEventType import KeyEventType
from .KeyEvent import KeyEvent

##########
#   Public entities
class KeyEventHandler:

    ##########
    #   Operations
    def on_key_work(self, evt: KeyEvent) -> None:
        pass

    def on_key_up(self, evt: KeyEvent) -> None:
        pass

    def on_key_char(self, evt: KeyEvent) -> None:
        pass
