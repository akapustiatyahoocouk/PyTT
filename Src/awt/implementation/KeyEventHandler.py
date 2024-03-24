""" An interface to an agent handling KeyEvents. """

#   Internal dependencies on modules within the same component
from .KeyEvent import KeyEvent

##########
#   Public entities
class KeyEventHandler:
    """ An interface to an agent handling KeyEvents. """

    ##########
    #   Operations
    def on_key_down(self, evt: KeyEvent) -> None:
        """ Called to handle a "key pressed" key event. """
        pass

    def on_key_up(self, evt: KeyEvent) -> None:
        """ Called to handle a "key released" key event. """
        pass

    def on_key_char(self, evt: KeyEvent) -> None:
        """ Called to handle a "character typed" key event. """
        pass
