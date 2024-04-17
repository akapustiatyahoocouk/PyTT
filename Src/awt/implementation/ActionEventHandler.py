"""
    Defines the categorising handler of ActionEvents.
"""
#   Internal dependencies on modules within the same component
from .ActionEvent import ActionEvent

##########
#   Public entities
class ActionEventHandler:
    """ An abstract handler which does not have to analyse the event
        type but gets called on an appropriate methid directly. """

    ##########
    #   Operations
    def on_action(self, evt: ActionEvent) -> None:
        """ Called by AWT when an ActionEvent occurs for which this
            handler is registered to listen. """
        #   TODO use action event's "command" property to try to locate
        #   the on_<command>_action method and call it
        pass
