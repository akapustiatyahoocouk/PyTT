"""
    Defines a MenuBar - a menu that can be assigned to a
    top-level window (e.g. a frame or a dialog) to appear at
    the top of that top-level window.
"""
from awt.Menu import Menu

class MenuBar(Menu):

    ##########
    #   Construction
    def __init__(self):
        """ Constructs a Menu8Bar, initially with no menu items. """
        Menu.__init__(self)
