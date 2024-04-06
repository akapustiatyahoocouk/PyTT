#   Python standard library
import tkinter as tk

##########
#   Public entities
class TopWindowMixin:

    ##########
    #   Properties
    @property
    def topmost(self):
        """ True if this is a topmost window, False if not. """
        return tk.Toplevel.attributes(self, "-topmost") == 1

    @topmost.setter
    def topmost(self, new_topmost: bool):
        """
            Makes this window topmost or not.

            @param new_topmost:
                True to make this the topmost window, False to
                make this a regular window.
        """
        assert isinstance(new_topmost, bool)
        tk.Toplevel.attributes(self, "-topmost", 1 if new_topmost else 0)
