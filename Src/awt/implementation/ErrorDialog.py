""" The error report modal dialog. """
#   Python standard library
import tkinter as tk
import tkinter.ttk as ttk
import traceback

from .ActionEvent import ActionEvent
from .ItemEvent import ItemEvent

#   Internal dependencies on modules within the same component
from .Dialog import Dialog
from .Panel import Panel
from .Label import Label
from .ListBox import ListBox
from .TabbedPane import TabbedPane
from .Separator import Separator
from .Button import Button
from .MessageBox import MessageBox, MessageBoxIcon, MessageBoxButtons
from ..resources.AwtResources import AwtResources

##########
#   Public entities
class ErrorDialog(Dialog):
    """ The dialog that presents an error or exception message
        to the user. """

    ##########
    #   Construction
    def __init__(self,
                 parent: tk.BaseWidget,
                 ex: Exception):
        Dialog.__init__(self, parent, AwtResources.string("ErrorDialog.Title") + " - " + str(ex))

        assert isinstance(ex, Exception)
        self.__ex = ex

        #   Create control styles
        style = ttk.Style()
        style.layout('Tabless.TNotebook.Tab', []) # new style with tabs turned off

        #   Create controls
        self.__controls_panel = Panel(self)
        self.__list_box = ListBox(self.__controls_panel)

        self.__tabbed_pane = TabbedPane(self.__controls_panel, style="Tabless.TNotebook")

        self.__separator = Separator(self, orient="horizontal")

        self.__save_button = Button(self,
            text=AwtResources.string("ErrorDialog.SaveButton.Text"),
            image=AwtResources.image("ErrorDialog.SaveButton.Icon"))
        self.__ok_button = Button(self,
            text=AwtResources.string("ErrorDialog.OkButton.Text"),
            image=AwtResources.image("ErrorDialog.OkButton.Icon"))

        #   Adjust controls
        self.__tabbed_pane.focusable = False

        while isinstance(ex, Exception):
            details = traceback.format_exception(ex, chain=False)

            text = Label(self.__tabbed_pane, text="\n".join(details))
            self.__tabbed_pane.add(text, state="normal", text=type(ex).__name__)

            list_item_text = type(ex).__name__
            if ex != self.__ex:
                list_item_text = 'caused by ' + list_item_text
            self.__list_box.items.add(list_item_text)
            ex = ex.__cause__

        self.__list_box.selected_index = 0
        self.__tabbed_pane.select(0)

        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__list_box.pack(side=tk.LEFT, padx=0, pady=0, fill=tk.Y)
        self.__tabbed_pane.pack(fill=tk.X, padx=0, pady=0)

        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__save_button.pack(side=tk.LEFT, padx=0, pady=0)
        self.__ok_button.pack(side=tk.RIGHT, padx=0, pady=0)

        #   Set up event handlers
        self.__list_box.add_item_listener(self.__list_box_item_listener)

        self.__save_button.add_action_listener(self.__on_save)
        self.__ok_button.add_action_listener(self.__on_ok)

        self.ok_button = self.__ok_button
        self.cancel_button = self.__ok_button

        #   Done
        self.wait_visibility()
        self.center_in_parent()

    ##########
    #   Operations
    @staticmethod
    def show(parent: tk.BaseWidget, error: [str|Exception]):
        """
            Displays the error message modally.
            
            @param parent:
                The parent window for the dialog shown to the user.
            @param error:
                The error ti display. Can be one of:
                *   str - a simple error message to display as a MessageBox.
                *   Exception - an exception to display with its traceback
                    and causes.
        """
        if isinstance(error, str):
            MessageBox.show(parent,
                            'Error',
                            error,
                            icon=MessageBoxIcon.ERROR,
                            buttons=MessageBoxButtons.OK)
        else:
            assert isinstance(error, Exception)
            with ErrorDialog(parent, error) as dlg:
                dlg.do_modal()

    ##########
    #   Event listeners
    def __list_box_item_listener(self, evt: ItemEvent) -> None:
        assert isinstance(evt, ItemEvent)
        self.__tabbed_pane.select(self.__list_box.selected_index)

    def __on_save(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        MessageBox.show(self, "Save", "Not yet implemented", MessageBoxIcon.INFORMATION)

    def __on_ok(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        self.end_modal()
