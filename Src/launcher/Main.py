'''
Created on 15 Mar 2024

@author: akapusti
'''

import abc
from enum import Enum

import tkinter as tk
import tkinter.ttk as ttk

class Dialog(abc.ABC):
    def __init__(self, parent: ttk.Widget, title: str):
        super().__init__()

        self.__parent = parent.winfo_toplevel()
        self.__root = tk.Toplevel(self.__parent, borderwidth = 4)
        self.__root.title(title)

    @property
    def parent(self):
        return self.__parent
    
    @property
    def root(self):
        return self.__root

    def center_in_parent(self):
        w = self.__root.winfo_width()
        h = self.__root.winfo_height()
        pw = self.__parent.winfo_width()
        ph = self.__parent.winfo_height()
        px = self.__parent.winfo_x()
        py = self.__parent.winfo_y()
        x = px + (pw/2) - (w/2)
        y = py + (ph/2) - (h/2)
        self.__root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def do_modal(self):
        print('opened dialog window, about to wait')
        self.__parent.wait_window(self.__root)   # <<< NOTE
        print('end wait_window, back in MainWindow code')

class AboutDialogResult(Enum):
    """ The result of modal invocation of the AboutDialog. """
    OK = 1      #   Dialog closed, by whatever means necessary

class AboutDialog(Dialog):
    """ The modal 'about...' dialog. """

    ##########
    #   Construction    
    def __init__(self, parent: ttk.Widget):
        super().__init__(parent, 'About PyTT')

        self.__result = AboutDialogResult.OK
        
        self.__pan0 = ttk.Label(self.root, text="")
        self.__pan1 = ttk.Label(self.__pan0, text="")
        self.__pan2 = ttk.Label(self.__pan0, text="")
        
        self.__pic1 = ttk.Label(self.__pan1, text="Pic")
        self.__msg1 = ttk.Label(self.__pan2, text="PyTT")
        self.__msg2 = ttk.Label(self.__pan2, text="PyTT")
        self.__msg3 = ttk.Label(self.__pan2, text="PyTT dddddddddddddd fffffffff")
        self.__separator = ttk.Separator(self.root, orient='horizontal')
        self.__closeButton = ttk.Button(self.root, text="Close")

        self.__pan0.config(background="cyan")
        self.__pan1.config(background="yellow")
        self.__pan2.config(background="blue")
        self.__msg1.config(background="white")
        self.__msg2.config(background="green")
        self.__msg3.config(background="red")

        self.__pan1.pack(fill=tk.NONE, padx=8, pady=2)
        self.__pan2.pack(fill=tk.X, padx=8, pady=2)

        #self.__root.pack(padx=8, pady=8)
        self.__pan0.pack(fill=tk.X, padx=0, pady=0)
        self.__pan1.pack(side=tk.LEFT, padx=0, pady=0)
        self.__pan2.pack(fill=tk.X, padx=0, pady=0)

        self.__pic1.pack(fill=tk.NONE, padx=2, pady=2)
        self.__msg1.pack(fill=tk.X, padx=2, pady=2)
        self.__msg2.pack(fill=tk.X, padx=2, pady=2)
        self.__msg3.pack(fill=tk.X, padx=2, pady=2)
        
        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__closeButton.pack(side=tk.RIGHT, padx=0, pady=0)

        self.root.bind('<Escape>', self.__close)
        self.root.bind('<Return>', self.__close)
        self.__closeButton.bind("<Button-1>", self.__close)
        self.root.protocol("WM_DELETE_WINDOW", self.__close)
        
        # Modal window.
        # Wait for visibility or grab_set doesn't seem to work.
        self.root.wait_visibility()         # <<< NOTE
        self.root.grab_set()                # <<< NOTE
        self.root.transient(self.parent)    # <<< NOTE

        self.center_in_parent()
        
        #self.__root.tkraise()
        #self.__root.update_idletasks()
        #self.__root.focus_force()
        self.__closeButton.focus_set()

    ##########
    #   Properties    
    @property
    def result(self) -> AboutDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Implementation helpers
    def __close(self, evt = None):
        self.root.grab_release()      # <<< NOTE
        self.root.destroy()

    def __enter__(self):
        print('AboutDialog.__enter__() called')
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        print('AboutDialog.__exit__() called')
        pass

class MainWindow(ttk.Frame):
    def __init__(self, window):
        window.geometry('600x400')
        self.popupButton = ttk.Button(window, text='popup', command=self.popup)
        self.quitButton = ttk.Button(window, text='quit', command=self.closeme)

        self.popupButton.pack()
        self.quitButton.pack()

        self.window = window
        window.bind('<Key>', self.handle_key)
                    
    def handle_key(self, event):
        k = event.keysym
        print(f"got k: {k}")

    def popup(self):
        with AboutDialog(self.popupButton) as dlg:
            print('opened dialog window, about to wait')
            #self.window.wait_window(dlg.root)   # <<< NOTE
            dlg.do_modal()
            if dlg.result is AboutDialogResult.OK:
                print('OK')
            print('end wait_window, back in MainWindow code')

    def closeme(self):
        self.window.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
    print('exit main loop')            
