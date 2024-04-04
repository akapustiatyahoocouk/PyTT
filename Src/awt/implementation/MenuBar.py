"""
    Defines a MenuBar - a menu that can be assigned to a
    top-level window (e.g. a frame or a dialog) to appear at
    the top of that top-level window.
"""
#   Python standard library

#   Internal dependencies on modules within the same component
from awt.implementation.Menu import Menu

##########
#   Public entities
class MenuBar(Menu):

    ##########
    #   Construction
    def __init__(self):
        """ Constructs a Menu8Bar, initially with no menu items. """
        Menu.__init__(self)
