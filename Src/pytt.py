import atexit
import sys

import tkinter as tk
import tkinter.ttk as ttk

import awt
import ws
import skin
import dialogs

def exit_handler():
    print('My application is ending!')

def test1():
    f1 = tk.Toplevel(master=GuiRoot.tk)
    f1.transient(GuiRoot.tk)
    f1.title(resources.Resources.PRODUCT_NAME + ' - Administrator mode')
    f1.btn1 = ttk.Button(f1, text='popup', command=GuiRoot.tk.destroy)
    f1.btn1.pack()
    f1.geometry("600x400")
    
    f2 = tk.Toplevel(master=GuiRoot.tk)
    f2.overrideredirect(True)
    f2.wm_attributes("-alpha",0.5)
    f2.attributes("-topmost", True)
    f2.title('Frame 2')
    f2.geometry(f"320x200+{GuiRoot.usable_width-320}+{GuiRoot.usable_height-200}")

    f2.canvas = tk.Canvas(f2, bg="green") # , width=200, height=100)
    f2.canvas.pack(side="top", fill="both", expand=True, ipadx=0, pady=0)
    f2.canvas.create_rectangle(20,10,100,50, fill="red", outline="black")

    def start_move(event):
        f2.x = event.x
        f2.y = event.y

    def stop_move(event):
        f2.x = None
        f2.y = None

    def do_move(event):
        deltax = event.x - f2.x
        deltay = event.y - f2.y
        x = f2.winfo_x() + deltax
        y = f2.winfo_y() + deltay
        f2.geometry(f"+{x}+{y}")

    f2.canvas.bind("<ButtonPress-1>", start_move)
    f2.canvas.bind("<ButtonRelease-1>", stop_move)
    f2.canvas.bind("<B1-Motion>", do_move)
        
    def xxx(*args):
        f1.deiconify()
        f2.deiconify()
        f1.focus_force()
        f2.attributes("-topmost", True)
        f2.geometry(f"320x200+{GuiRoot.usable_width-320}+{GuiRoot.usable_height-200}")
        
    def yyy(*args):
        f1.withdraw()
        f2.withdraw()

    GuiRoot.tk.bind("<Unmap>", yyy)
    GuiRoot.tk.bind("<Map>", xxx)
    
    #GuiRoot.tk.tkraise()
    #GuiRoot.tk.focus()
    #f1.focus_set()
    
    #f1.attributes("-topmost", True)
    #f1.attributes("-topmost", False)

    #GuiRoot.tk.withdraw()
    #GuiRoot.tk.deiconify()

    GuiRoot.tk.mainloop()
    
    exit()

def __perform_initial_login(login_dialog: dialogs.LoginDialog):
    login_dialog.quit()
    login_dialog.destroy()

def __abort_initial_login(login_dialog: dialogs.LoginDialog):
    sys.exit()
    
if __name__ == "__main__":

    atexit.register(exit_handler)
    
    #   Perform initial login
    with dialogs.LoginDialog(awt.GuiRoot.tk,
                             on_ok_callback=__perform_initial_login,
                             on_cancel_callback=__abort_initial_login) as dlg:
        dlg.transient(awt.GuiRoot.tk)
        dlg.attributes("-topmost", True)
        #dlg.focus_set()
        awt.GuiRoot.tk.mainloop()
        if dlg.result is not dialogs.LoginDialogResult.OK:
            sys.exit()
        ws.CurrentCredentials.set(dlg.credentials)
    #   Select the initial skin TODO properly!
    skin.ActiveSkin.set(skin.SkinRegistry.get_default_skin())
    
    #   Go!
    awt.GuiRoot.tk.mainloop()
    
    #   Cleanup & exit
    skin.ActiveSkin.set(None)
    print('exit main loop')
    awt.GuiRoot.tk.destroy()

