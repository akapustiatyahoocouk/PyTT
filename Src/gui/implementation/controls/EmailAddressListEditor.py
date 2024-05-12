#   Python standard library
import re
from tkinter import YES
from tkinter.messagebox import QUESTION, YESNO

#   Dependencies on other PyTT components
from awt.interface.api import *

#   Internal dependencies on modules within the same component
from gui.resources.GuiResources import GuiResources

##########
#   Piblic entities
class EmailAddressListEditor(Panel):

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget):
        Panel.__init__(self, parent)

        #   Create controls
        self.__email_addresses_list_box = ListBox(self, height=3)
        self.__actions_panel = Panel(self)
        self.__email_addresses = []

        self.__add_email_address_button = Button(
            self.__actions_panel,
            text=GuiResources.string("EmailAddressListEditor.AddEmailAddressButton.Text"),
            image=GuiResources.image("EmailAddressListEditor.AddEmailAddressButton.Image"))
        self.__modify_email_address_button = Button(
            self.__actions_panel,
            text=GuiResources.string("EmailAddressListEditor.ModifyEmailAddressButton.Text"),
            image=GuiResources.image("EmailAddressListEditor.ModifyEmailAddressButton.Image"))
        self.__remove_email_address_button = Button(
            self.__actions_panel,
            text=GuiResources.string("EmailAddressListEditor.RemoveEmailAddressButton.Text"),
            image=GuiResources.image("EmailAddressListEditor.RemoveEmailAddressButton.Image"))

        #   Adjust controls

        #   Set up control structure
        self.__actions_panel.pack(side=tk.RIGHT, padx=0, pady=0, fill=tk.Y)
        self.__email_addresses_list_box.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)

        self.__add_email_address_button.grid(row=0, column=0, padx=0, pady=2, sticky="WE")
        self.__modify_email_address_button.grid(row=1, column=0, padx=0, pady=2, sticky="WE")
        self.__remove_email_address_button.grid(row=2, column=0, padx=0, pady=2, sticky="WE")

        #   Set up event handlers
        self.__email_addresses_list_box.add_item_listener(self.__email_addresses_list_box_listener)
        self.__add_email_address_button.add_action_listener(self.__add_email_address_button_clicked)
        self.__modify_email_address_button.add_action_listener(self.__modify_email_address_button_clicked)
        self.__remove_email_address_button.add_action_listener(self.__remove_email_address_button_clicked)

        #   Done
        self.request_refresh()

    ##########
    #   Refreshable
    def refresh(self) -> None:
        self.__modify_email_address_button.enabled = (self.__email_addresses_list_box.selected_index is not None)
        self.__remove_email_address_button.enabled = (self.__email_addresses_list_box.selected_index is not None)

        #   Make sure the "e-mail addrsses: list has a proper number...
        while len(self.__email_addresses_list_box.items) > len(self.__email_addresses):
            #   Too many items in the list
            self.__email_addresses_list_box.items.remove_at(len(self.__email_addresses_list_box.items) - 1)
        while len(self.__email_addresses_list_box.items) < len(self.__email_addresses):
            #   Too few items in the list
            self.__email_addresses_list_box.items.add("")
        #   ...of proper items
        for i in range(len(self.__email_addresses)):
            self.__email_addresses_list_box.items[i].text = self.__email_addresses[i]
        
    ##########
    #   Properties
    @property
    def email_addresses(self) -> List[str]:
        return self.__email_addresses.copy()

    @email_addresses.setter
    def email_addresses(self, new_email_addresses: List[str]) -> None:
        assert isinstance(new_email_addresses, list)
        assert all(isinstance(a, str) for a in new_email_addresses)
        self.__email_addresses = new_email_addresses.copy()
        self.request_refresh()


    ##########
    #   Implementation helpers
    def __is_valid_email_address(self, s: str) -> bool: #   TODO use Workspace.validator
        assert isinstance(s, str)

        pattern = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"
        return re.match(pattern, s) is not None

    ##########
    #   Event listeners
    def __email_addresses_list_box_listener(self, evt: ItemEvent) -> None:
        assert isinstance(evt, ItemEvent)
        self.request_refresh()

    def __add_email_address_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)

        with EditStringDialog(self.winfo_toplevel(),
                              GuiResources.string("EmailAddressListEditor.AddEmailAddressDialog.Title"),
                              GuiResources.string("EmailAddressListEditor.AddEmailAddressDialog.Prompt"),
                              validator=self.__is_valid_email_address) as dlg:
            dlg.do_modal()
            if dlg.result is not EditStringDialogResult.OK:
                return
            email_address = dlg.value
            if email_address not in self.__email_addresses:
                self.__email_addresses.append(email_address)
            self.__email_addresses.sort()
            self.perform_refresh()
            #   TODO and select it as "current"
            index = self.__email_addresses.index(email_address)
            self.__email_addresses_list_box.selected_index = index

    def __modify_email_address_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        si = self.__email_addresses_list_box.selected_item
        old_email_address = si.text
        with EditStringDialog(self.winfo_toplevel(),
                              GuiResources.string("EmailAddressListEditor.ModifyEmailAddressDialog.Title"),
                              GuiResources.string("EmailAddressListEditor.ModifyEmailAddressDialog.Prompt"),
                              value=old_email_address,
                              validator=self.__is_valid_email_address) as dlg:
            dlg.do_modal()
            if dlg.result is not EditStringDialogResult.OK:
                return
            new_email_address = dlg.value
            self.__email_addresses[self.__email_addresses.index(old_email_address)] = new_email_address
            self.__email_addresses.sort()
            self.perform_refresh()
            index = self.__email_addresses.index(new_email_address)
            self.__email_addresses_list_box.selected_index = index

    def __remove_email_address_button_clicked(self, evt: ActionEvent) -> None:
        assert isinstance(evt, ActionEvent)
        si = self.__email_addresses_list_box.selected_item
        email_address = si.text
        if MessageBox.show(self.winfo_toplevel(),
                title=GuiResources.string("EmailAddressListEditor.RemoveEmailAddressDialog.Title"),
                message=GuiResources.string("EmailAddressListEditor.RemoveEmailAddressDialog.Prompt",
                                            args=(email_address,)),
                icon=MessageBoxIcon.QUESTION,
                buttons=MessageBoxButtons.YES_NO) == MessageBoxResult.YES:
            self.__email_addresses.remove(email_address)
            self.request_refresh()
            

