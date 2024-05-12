""" PyTT Client launcher. """

#   Python standard library
from typing import final
import sys
import os.path
from datetime import datetime, UTC
import threading

#   Dependencies on other PyTT components.
#   IMPORTANT: We need to adjust the sys.path to find them!
if __name__ == "__main__":
    root_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    print("Starting PyTT from", root_directory)
    sys.path.insert(0, root_directory)  #   TODO THIS HAPPENS TWICE - HERE AND FROM PLUGINLOADER

from gui.interface.api import *
from awt.interface.api import *
from workspace.interface.api import *
from pnp.interface.api import *
from util.interface.api import *

#   Internal dependencies on modules within the same component
#   NOTE that we can't use relative import "from .CommandLine ...",
#   because when __name__ == "__main__" (PyTT client invoked as
#   an application) there is no root module to be relative to.
from client.implementation.CommandLine import CommandLine
from client.implementation.GeneralStartupPreferences import GeneralStartupPreferences
from client.implementation.GeneralAppearancePreferences import GeneralAppearancePreferences

@final
class SplashScreen: #   TODO move to a separate file

    ##########
    #   Implementation
    __splash_screen = None

    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"

    ##########
    #   Operations
    @staticmethod
    def show():
        # Create objects
        SplashScreen.__splash_screen = Frame()
        SplashScreen.__splash_screen.geometry("320x100")
        SplashScreen.__splash_screen.wait_visibility()
        SplashScreen.__splash_screen.configure(borderwidth=1, relief='solid', bg="white",)
        SplashScreen.__splash_screen.pack_propagate(1)

        splash_icon = Label(SplashScreen.__splash_screen, image=UtilResources.image("PyTT.LargeImage"), background="white")
        splash_label1 = Label(SplashScreen.__splash_screen, text=UtilResources.string("PyTT.ProductName"), font="Helvetica 18", background="white", foreground="blue", anchor="center")
        splash_label2 = Label(SplashScreen.__splash_screen, text=UtilResources.string("PyTT.ProductVersion"), font="Helvetica 12", background="white", foreground="blue", anchor="center")
        splash_separator = Separator(SplashScreen.__splash_screen, orient="horizontal")
        splash_label3 = Label(SplashScreen.__splash_screen, text=UtilResources.string("PyTT.ProductCopyright"), font="Helvetica 10", background="white", foreground="gray", anchor="center")

        SplashScreen.__splash_screen.rowconfigure(0, weight=1)
        SplashScreen.__splash_screen.rowconfigure(4, weight=1)
        SplashScreen.__splash_screen.columnconfigure(1, weight=10)
        splash_icon.grid(row=1, column=0, padx=8, pady=2, rowspan=2, sticky="W")
        splash_label1.grid(row=1, column=1, padx=(2, 32), pady=0, sticky="WE")
        splash_label2.grid(row=2, column=1, padx=(2, 32), pady=0, sticky="WE")
        splash_separator.grid(row=3, column=0, columnspan=2, padx=2, pady=(8, 0), sticky="WE")
        splash_label3.grid(row=4, column=0, columnspan=2, padx=2, pady=0, sticky="WE")

        SplashScreen.__splash_screen.overrideredirect(True)
        SplashScreen.__splash_screen.topmost = True
        SplashScreen.__splash_screen.center_in_screen()
        #SplashScreen.__splash_screen.wait_window()

    @staticmethod
    def hide():
        SplashScreen.__splash_screen.destroy()

    @staticmethod
    def update():
        SplashScreen.__splash_screen.update()

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
#         f2.geometry(f"320x200+{GuiRoot.usable_width-320}+{GuiRoot.usable_height-200}")

#     def yyy(*args):
#         f1.withdraw()
#         f2.withdraw()

#     GuiRoot.tk.bind("<Unmap>", yyy)
#     GuiRoot.tk.bind("<Map>", xxx)

#     #GuiRoot.tk.tkraise()
#     #GuiRoot.tk.focus()
#     #f1.focus_set()

#     #GuiRoot.tk.withdraw()
#     #GuiRoot.tk.deiconify()

#     GuiRoot.tk.mainloop()

#     sys.exit()

##########
#   Implementation yhelpers
def load_plugins():
    if CommandLine.show_splash_screen:
        splash_start_time = datetime.now(UTC)
        SplashScreen.show()

    PluginManager.load_plugins(root_directory)

    if CommandLine.show_splash_screen:
        while True:
            SplashScreen.update()
            utc_now = datetime.now(UTC)
            if (utc_now - splash_start_time).seconds >= 3:
                SplashScreen.hide()
                break
    
def perform_initial_login():
    login = ""
    if GeneralStartupPreferences.instance.use_last_login.value:
        login = GuiSettings.last_login
    with LoginDialog(GuiRoot.tk, login=login) as dlg:
        dlg.topmost = True
        dlg.do_modal()
        if dlg.result is not LoginDialogResult.OK:
            sys.exit()
        CurrentCredentials.set(dlg.credentials)

def open_last_used_workspace():
    workspace_address = WorkspaceSettings.last_workspace_address
    if workspace_address is None:
        return
    workspace = None
    while True:
        try:
            if workspace is None:
                workspace = workspace_address.workspace_type.open_workspace(workspace_address)
            workspace.login(credentials=CurrentCredentials.get())
            CurrentWorkspace.set(workspace)
            return
        except WorkspaceAccessDeniedError as ex:
            title = GuiResources.string("CannotAccessLastWorkspaceDialog.Title")
            message = GuiResources.string("CannotAccessLastWorkspaceDialog.Message",
                                          workspace_address.display_form)
            if MessageBox.show(None, 
                               title,
                               message,
                               MessageBoxIcon.QUESTION,
                               MessageBoxButtons.YES_NO) == MessageBoxResult.YES:
                perform_initial_login()
                continue
            workspace.close()
            return
        except Exception as ex:
            if workspace:
                workspace.close()
            ErrorDialog.show(None, ex)
            title = GuiResources.string("CannotReopenLastWorkspaceDialog.Title")
            message = GuiResources.string("CannotReopenLastWorkspaceDialog.Message",
                                          workspace_address.display_form)
            if MessageBox.show(None, 
                               title,
                               message,
                               MessageBoxIcon.QUESTION,
                               MessageBoxButtons.YES_NO) == MessageBoxResult.YES:
                pass    # TODO do it!
            return
    
##########
#   PyTT entry point
if __name__ == "__main__":

    print('Python is', sys.version_info)
    print('System locale is', Locale.default)
    print("Main thread is " + str(threading.current_thread().ident))

    CommandLine.parse()

    #   Load plugins (showing splash screen if necessary)
    load_plugins()
    
    #   Now that all plugins are loaded, the Preferences
    #   tree is complete, so we can load all Preferences        
    Preferences.load()
    ui_locale = GeneralAppearancePreferences.instance.ui_locale.value
    if ui_locale in LocalizableSubsystem.all_supported_locales():
        Locale.default = ui_locale

    #   Perform initial login; use last successful login if necessary
    perform_initial_login()

    #   Do we need to re-load the last used workspace?
    if GeneralStartupPreferences.instance.restore_workspace.value:
        open_last_used_workspace()

    #   Select the initial skin TODO properly - use active skin from previous session!
    ActiveSkin.set(SkinRegistry.default_skin)

    #   Go!
    GuiRoot.tk.mainloop()

    #   Cleanup & exit
    Preferences.save()
    ActiveSkin.set(None)
    print('exit main loop')
    GuiRoot.tk.destroy()
