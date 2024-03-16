'''
Created on 15 Mar 2024

@author: akapusti
'''

import tkinter as tk
import tkinter.ttk as ttk
from gui.AboutDialog import *

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
