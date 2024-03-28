"""
    PyTT launcher.
"""
from typing import final
from abc import abstractproperty

import atexit
import sys
import os.path

import awt
import ws
import skin
import dialogs
import pnp
import util

from util import staticproperty, ABCWithConstants

@final
class SplashScreen:
    #   TODO a simple private function would do!
    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"
        
    ##########
    #   Operations
    @staticmethod
    def show():
        # Create objects
        splash_screen = awt.TopFrame()
        splash_screen.geometry("320x100")
        splash_screen.wait_visibility()
        splash_screen.configure(borderwidth=1, relief='solid', bg="white",)
        #pp = splash_screen.pack_propagate()
        splash_screen.pack_propagate(1)

        splash_icon = awt.Label(splash_screen, image = util.UtilResources.PRODUCT_ICON_LARGE, background="white")
        splash_label1 = awt.Label(splash_screen, text=util.UtilResources.PRODUCT_NAME, font="Helvetica 18", background="white", foreground="blue", anchor="center")
        splash_label2 = awt.Label(splash_screen, text='Version ' + util.UtilResources.PRODUCT_VERSION, font="Helvetica 12", background="white", foreground="blue", anchor="center")
        splash_separator = awt.Separator(splash_screen, orient="horizontal")
        splash_label3 = awt.Label(splash_screen, text=util.UtilResources.PRODUCT_COPYRIGHT, font="Helvetica 10", background="white", foreground="gray", anchor="center")

        splash_screen.rowconfigure(0, weight=1)
        splash_screen.rowconfigure(4, weight=1)
        splash_screen.columnconfigure(1, weight=10)
        splash_icon.grid(row=1, column=0, padx=8, pady=2, rowspan=2, sticky="W")
        splash_label1.grid(row=1, column=1, padx=(2, 32), pady=0, sticky="WE")
        splash_label2.grid(row=2, column=1, padx=(2, 32), pady=0, sticky="WE")
        splash_separator.grid(row=3, column=0, columnspan=2, padx=2, pady=(8, 0), sticky="WE")
        splash_label3.grid(row=4, column=0, columnspan=2, padx=2, pady=0, sticky="WE")

        splash_screen.overrideredirect(True)
        #splash_screen.wm_attributes("-alpha",0.5)
        splash_screen.attributes("-topmost", True)
        splash_screen.after(3000, lambda: splash_screen.destroy())
        splash_screen.center_in_screen()
        splash_screen.wait_window()

# TODO kill off
# def test1():
#     f1 = tk.Toplevel(master=GuiRoot.tk)
#     f1.transient(GuiRoot.tk)
#     f1.title(util.UtilResources.PRODUCT_NAME + ' - Administrator mode')
#     f1.btn1 = ttk.Button(f1, text='popup', command=GuiRoot.tk.destroy)
#     f1.btn1.pack()
#     f1.geometry("600x400")

#     f2 = tk.Toplevel(master=GuiRoot.tk)
#     f2.overrideredirect(True)
#     f2.wm_attributes("-alpha",0.5)
#     f2.attributes("-topmost", True)
#     f2.title('Frame 2')
#     f2.geometry(f"320x200+{GuiRoot.usable_width-320}+{GuiRoot.usable_height-200}")

#     f2.canvas = tk.Canvas(f2, bg="green") # , width=200, height=100)
#     f2.canvas.pack(side="top", fill="both", expand=True, ipadx=0, pady=0)
#     f2.canvas.create_rectangle(20,10,100,50, fill="red", outline="black")

#     def start_move(event):
#         f2.x = event.x
#         f2.y = event.y

#     def stop_move(event):
#         f2.x = None
#         f2.y = None

#     def do_move(event):
#         deltax = event.x - f2.x
#         deltay = event.y - f2.y
#         x = f2.winfo_x() + deltax
#         y = f2.winfo_y() + deltay
#         f2.geometry(f"+{x}+{y}")

#     f2.canvas.bind("<ButtonPress-1>", start_move)
#     f2.canvas.bind("<ButtonRelease-1>", stop_move)
#     f2.canvas.bind("<B1-Motion>", do_move)

#     def xxx(*args):
#         f1.deiconify()
#         f2.deiconify()
#         f1.focus_force()
#         f2.attributes("-topmost", True)
#         f2.geometry(f"320x200+{awt.GuiRoot.usable_width-320}+{awt.GuiRoot.usable_height-200}")

#     def yyy(*args):
#         f1.withdraw()
#         f2.withdraw()

#     awt.GuiRoot.tk.bind("<Unmap>", yyy)
#     awt.GuiRoot.tk.bind("<Map>", xxx)

#     #GuiRoot.tk.tkraise()
#     #GuiRoot.tk.focus()
#     #f1.focus_set()

#     #f1.attributes("-topmost", True)
#     #f1.attributes("-topmost", False)

#     #GuiRoot.tk.withdraw()
#     #GuiRoot.tk.deiconify()

#     awt.GuiRoot.tk.mainloop()

#     sys.exit()

##########
#   Implementation helpers
def __exit_handler():
    print('My application is ending!')

##########
#   PyTT entry point
if __name__ == "__main__":

    print("sys.argv", sys.argv)
    root_directory = os.path.dirname(__file__)
    print("Starting PyTT from", root_directory)
    sys.path.insert(0, root_directory)

    SplashScreen.show()    
    pnp.PluginManager.load_plugins(root_directory)
    
    atexit.register(__exit_handler)

    #   Perform initial login
    #   TODO use last successful login by default
    with dialogs.LoginDialog(awt.GuiRoot.tk) as dlg:
        dlg.transient(awt.GuiRoot.tk)
        dlg.attributes("-topmost", True)
        dlg.do_modal()
        #try:
        #    awt.GuiRoot.tk.mainloop()
        #except:
        #    pass
        if dlg.result is not dialogs.LoginDialogResult.OK:
            sys.exit()
        ws.CurrentCredentials.set(dlg.credentials)
    awt.GuiRoot.tk.withdraw()
    
    #   Select the initial skin TODO properly - use active skin from previous session!
    skin.ActiveSkin.set(skin.SkinRegistry.get_default_skin())

    #   Go!
    awt.GuiRoot.tk.mainloop()

    #   Cleanup & exit
    skin.ActiveSkin.set(None)
    print('exit main loop')
    awt.GuiRoot.tk.destroy()
