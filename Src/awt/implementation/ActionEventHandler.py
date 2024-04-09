
#   Internal dependencies on modules within the same component
from .ActionEvent import ActionEvent

##########
#   Public entities
class ActionEventHandler:

    ##########
    #   Operations
    def on_action(self, evt: ActionEvent) -> None:
        #   TODO use action event's "command" property to try to locate
        #   the on_<command>_action method and call it
        pass
