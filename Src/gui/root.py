from typing import final

import platform

import tkinter as tk

import util.resources as utilres

class _GuiRootType(type):
    ##########
    #   object
    def __getattribute__(cls, name):
        attribute = super().__getattribute__(name)
        try:
            return attribute.__get__(cls, type(cls))
        except AttributeError:
            return attribute
@final
class GuiRoot(metaclass=_GuiRootType):
    """ Provider of the one and only tkinter.Tk instance. """

    ##########
    #   Implementation helpers
    __tk = None

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + ' is a utility class'

    ##########
    #   Properties (all static)    
    @property
    def tk(cls) -> tk.Tk:
        """ The one and only tkinter.Tk instance. """
        if GuiRoot.__tk is None:
            GuiRoot.__tk = tk.Tk()
            GuiRoot.__tk.title(utilres.UtilResources.PRODUCT_NAME)
            GuiRoot.__tk.wm_iconphoto(True, utilres.UtilResources.PRODUCT_ICON)

            print('Platfom is', platform.system())
            
            if 'windows' in platform.system().lower():
                #   Windows family
                GuiRoot.__tk.withdraw()
                GuiRoot.__tk.wm_attributes('-alpha',0.5)
                GuiRoot.__tk.state('zoomed')
                GuiRoot.__tk.update()
                GuiRoot.__usable_x = GuiRoot.__tk.winfo_x()
                GuiRoot.__usable_y = GuiRoot.__tk.winfo_y()
                GuiRoot.__usable_width = GuiRoot.__tk.winfo_width()
                GuiRoot.__usable_height = GuiRoot.__tk.winfo_height()
                GuiRoot.__screen_width = GuiRoot.__tk.winfo_screenwidth()
                GuiRoot.__screen_height = GuiRoot.__tk.winfo_screenheight()
                GuiRoot.__tk.state('normal')
            else:
                #   Linux, etc.
                GuiRoot.__tk.wm_attributes('-alpha',0.5)    #   doesn't seem to work, though
                GuiRoot.__tk.update()
                GuiRoot.__usable_x = 0
                GuiRoot.__usable_y = 0
                GuiRoot.__usable_width = GuiRoot.__tk.winfo_screenwidth()
                GuiRoot.__usable_height = GuiRoot.__tk.winfo_screenheight()
                GuiRoot.__screen_width = GuiRoot.__tk.winfo_screenwidth()
                GuiRoot.__screen_height = GuiRoot.__tk.winfo_screenheight()

            GuiRoot.__tk.geometry(f"16x16+{GuiRoot.__screen_width+16000}+{GuiRoot.__screen_height+16000}")

        return GuiRoot.__tk

    @property
    def usable_x(cls) -> int:
        return GuiRoot.__usable_x

    @property
    def usable_y(cls) -> int:
        return GuiRoot.__usable_y

    @property
    def usable_width(cls) -> int:
        return GuiRoot.__usable_width

    @property
    def usable_height(cls) -> int:
        return GuiRoot.__usable_height

    @property
    def screen_width(cls) -> int:
        return GuiRoot.__screen_width

    @property
    def screen_height(cls) -> int:
        return GuiRoot.__screen_height
 