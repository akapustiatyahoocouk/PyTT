""" Implements the "Modify Private activity" modal dialog. """

#   Python standard library
from typing import final, Optional, Callable
from enum import Enum
import tkinter as tk

from requests import get

#   Dependencies on other PyTT components
from awt.interface.api import *
from workspace.interface.api import *

#   Internal dependencies on modules within the same component
from gui.resources.GuiResources import GuiResources
from ..misc.CurrentCredentials import CurrentCredentials
from ..misc.CurrentWorkspace import CurrentWorkspace
from ..controls.EmailAddressListEditor import EmailAddressListEditor

##########
#   Public entities
@final
class ModifyPrivateActivityDialogResult(Enum):
    """ The result of modal invocation of the ModifyPrivateActivityDialog. """

    OK = 1
    """ A BusinessPrivateActivity has been modified. """

    CANCEL = 2
    """ Dialog cancelled by user. """

@final
class ModifyPrivateActivityDialog(Dialog):
    """ The modal "Modify Private activity " dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget,
                 private_activity: BusinessPrivateActivity,
                 credentials: Optional[Credentials] = None):
        """
            Constructs the "Modify Private activity" dialog.

            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used),
                None == no parent.
            @param private_activity:
                The private activity to modify.
            @param credentials:
                The credentials to use for workspace access; None == use
                the CurrentCredentials.
            @raise WorkspaceError:
                If a workspace access error occurs.
        """
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("ModifyPrivateActivityDialog.Title",
                                            private_activity.display_name,
                                            private_activity.get_owner(credentials if credentials is not None else CurrentCredentials.get()).display_name))

        assert isinstance(private_activity, BusinessPrivateActivity)
        self.__private_activity = private_activity
        self.__result = ModifyPrivateActivityDialogResult.CANCEL

        #   Resolve credentials
        assert (credentials is None) or isinstance(credentials, Credentials)
        self.__credentials = credentials if credentials is not None else CurrentCredentials.get()
        assert self.__credentials is not None

        #   Save current private activity properties
        self.__private_activity_name = private_activity.get_name(self.__credentials)
        self.__private_activity_description = private_activity.get_description(self.__credentials)
        self.__private_activity_activity_type = private_activity.get_activity_type(self.__credentials)
        self.__private_activity_timeout = private_activity.get_timeout(self.__credentials)
        self.__private_activity_require_comment_on_start = private_activity.get_require_comment_on_start(self.__credentials)
        self.__private_activity_require_comment_on_finish = private_activity.get_require_comment_on_finish(self.__credentials)
        self.__private_activity_full_screen_reminder = private_activity.get_full_screen_reminder(self.__credentials)
        self.__validator = private_activity.workspace.validator

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__name_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyPrivateActivityDialog.NameLabel.Text"),
            anchor=tk.E)
        self.__name_text_field = TextField(self.__controls_panel, width=40)

        self.__description_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyPrivateActivityDialog.DescriptionLabel.Text"),
            anchor=tk.E)
        self.__description_text_area = TextArea(self.__controls_panel, height=4, width=40)

        self.__activity_type_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyPrivateActivityDialog.ActivityTypeLabel.Text"),
            anchor=tk.E)
        self.__activity_type_combo_box = ComboBox(self.__controls_panel)

        self.__timeout_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyPrivateActivityDialog.TimeoutLabel.Text"),
            anchor=tk.E)
        self.__timeout_panel = Panel(self.__controls_panel)
        self.__timeout_value_combo_box = ComboBox(self.__timeout_panel)
        self.__timeout_unit_combo_box = ComboBox(self.__timeout_panel)

        self.__require_comment_on_start_check_box = CheckBox(
            self.__controls_panel,
            text=GuiResources.string("ModifyPrivateActivityDialog.RequireCommentOnStartCheckBox.Text"))
        self.__require_comment_on_finish_check_box = CheckBox(
            self.__controls_panel,
            text=GuiResources.string("ModifyPrivateActivityDialog.RequireCommentOnFinishCheckBox.Text"))
        self.__full_screen_reminder_check_box = CheckBox(
            self.__controls_panel,
            text=GuiResources.string("ModifyPrivateActivityDialog.FullScreenReminderCheckBox.Text"))

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("ModifyPrivateActivityDialog.OkButton.Text"),
            image=GuiResources.image("ModifyPrivateActivityDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("ModifyPrivateActivityDialog.CancelButton.Text"),
            image=GuiResources.image("ModifyPrivateActivityDialog.CancelButton.Icon"))

        #   Adjust controls
        self.__name_text_field.text = self.__private_activity_name

        self.__description_text_area.accept_tab = False
        self.__description_text_area.text = self.__private_activity_description

        for i in range(60):
            if i == 0:
                self.__timeout_value_combo_box.items.add(
                    GuiResources.string("ModifyPrivateActivityDialog.TimeoutNone"),
                    tag=i)
            else:
                self.__timeout_value_combo_box.items.add(str(i), tag=i)
        self.__timeout_value_combo_box.editable = False

        self.__timeout_unit_combo_box.items.add(
            GuiResources.string("ModifyPrivateActivityDialog.TimeoutMinutes"),
            tag=1)
        self.__timeout_unit_combo_box.items.add(
            GuiResources.string("ModifyPrivateActivityDialog.TimeoutHours"),
            tag=60)
        self.__timeout_unit_combo_box.editable = False

        if self.__private_activity_timeout is None:
            self.__timeout_value_combo_box.selected_index = 0
            self.__timeout_unit_combo_box.selected_index = 1
        elif (self.__private_activity_timeout > 0 and
              self.__private_activity_timeout < 60):
            self.__timeout_value_combo_box.selected_index = self.__private_activity_timeout
            self.__timeout_unit_combo_box.selected_index = 0
        elif (self.__private_activity_timeout % 60 == 0 and
              self.__private_activity_timeout // 60 > 0 and
              self.__private_activity_timeout // 60 <= 60):
            self.__timeout_value_combo_box.selected_index = self.__private_activity_timeout // 60
            self.__timeout_unit_combo_box.selected_index = 1
        else:
            self.__timeout_value_combo_box.selected_index = 1
            self.__timeout_unit_combo_box.selected_index = 1

        self.__activity_type_combo_box.editable = False
        self.__activity_type_combo_box.items.add("-", tag=None)
        activity_types = list(self.__private_activity.workspace.get_activity_types(self.__credentials))
        activity_types.sort(key=lambda u: u.display_name)
        for activity_type in activity_types:
            self.__activity_type_combo_box.items.add(activity_type.display_name, tag=activity_type)
        self.__activity_type_combo_box.selected_index = (
            0 if self.__private_activity_activity_type is None
            else activity_types.index(self.__private_activity_activity_type) + 1)

        self.__require_comment_on_start_check_box.checked = self.__private_activity_require_comment_on_start
        self.__require_comment_on_finish_check_box.checked = self.__private_activity_require_comment_on_finish
        self.__full_screen_reminder_check_box.checked = self.__private_activity_full_screen_reminder

        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__controls_panel.columnconfigure(1, weight=10)

        self.__name_label.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__name_text_field.grid(row=0, column=1, padx=2, pady=2, sticky="WE")

        self.__description_label.grid(row=1, column=0, padx=2, pady=2, sticky="W")
        self.__description_text_area.grid(row=1, column=1, padx=2, pady=2, sticky="WE")

        self.__activity_type_label.grid(row=2, column=0, padx=2, pady=2, sticky="W")
        self.__activity_type_combo_box.grid(row=2, column=1, padx=2, pady=2, sticky="WE")

        self.__timeout_label.grid(row=3, column=0, padx=2, pady=2, sticky="W")
        self.__timeout_panel.grid(row=3, column=1, padx=0, pady=0, sticky="W")
        self.__timeout_value_combo_box.pack(side=tk.LEFT, padx=2, pady=2)
        self.__timeout_unit_combo_box.pack(side=tk.LEFT, padx=2, pady=2)

        self.__require_comment_on_start_check_box.grid(row=4, column=1, padx=2, pady=2, sticky="W")
        self.__require_comment_on_finish_check_box.grid(row=5, column=1, padx=2, pady=2, sticky="W")
        self.__full_screen_reminder_check_box.grid(row=6, column=1, padx=2, pady=2, sticky="W")

        self.__separator.pack(fill=tk.X, padx=0, pady=4)
        self.__cancel_button.pack(side=tk.RIGHT, padx=2, pady=2)
        self.__ok_button.pack(side=tk.RIGHT, padx=2, pady=2)

        #   Set up event handlers
        self.ok_button = self.__ok_button
        self.cancel_button = self.__cancel_button

        self.__name_text_field.add_property_change_listener(self.__text_field_change_listener)
        self.__description_text_area.add_property_change_listener(self.__text_field_change_listener)
        self.__activity_type_combo_box.add_item_listener(self.__combo_box_listener)
        self.__timeout_value_combo_box.add_item_listener(self.__combo_box_listener)
        self.__timeout_unit_combo_box.add_item_listener(self.__combo_box_listener)

        self.__ok_button.add_action_listener(self.__on_ok)
        self.__cancel_button.add_action_listener(self.__on_cancel)

        #   Done
        self.wait_visibility()
        self.center_in_parent()
        self.request_refresh()

    ##########
    #   Refreshable
    def refresh(self) -> None:
        self.__timeout_unit_combo_box.enabled = \
            ((self.__timeout_value_combo_box.selected_item is not None) and
             (self.__timeout_value_combo_box.selected_item.tag != 0))
        self.__ok_button.enabled = (
            self.__validator.activity.is_valid_name(self.__name_text_field.text) and
            self.__validator.activity.is_valid_description(self.__description_text_area.text))

    ##########
    #   Properties
    @property
    def result(self) -> ModifyPrivateActivityDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Event listeners
    def __text_field_change_listener(self, evt: PropertyChangeEvent) -> None:
        assert isinstance(evt, PropertyChangeEvent)
        self.request_refresh()

    def __combo_box_listener(self, evt: ItemEvent) -> None:
        assert isinstance(evt, ItemEvent)
        self.request_refresh()

    def __on_ok(self, evt = None) -> None:
        name = self.__name_text_field.text.strip()
        description = self.__description_text_area.text.rstrip()
        activity_type = self.__activity_type_combo_box.selected_item.tag
        timeout = (self.__timeout_value_combo_box.selected_item.tag *
                   self.__timeout_unit_combo_box.selected_item.tag)
        if timeout == 0:
            timeout = None
        require_comment_on_start = self.__require_comment_on_start_check_box.checked
        require_comment_on_finish = self.__require_comment_on_finish_check_box.checked
        full_screen_reminder = self.__full_screen_reminder_check_box.checked

        try:
            #   TODO only if there are changes!!!
            if name != self.__private_activity_name:
                self.__private_activity.set_name(self.__credentials, name)
            if description != self.__private_activity_description:
                self.__private_activity.set_description(self.__credentials,description)
            if activity_type != self.__private_activity_activity_type:
                self.__private_activity.set_activity_type(self.__credentials, activity_type)
            if timeout != self.__private_activity_timeout:
                self.__private_activity.set_timeout(self.__credentials, timeout)
            if require_comment_on_start != self.__private_activity_require_comment_on_start:
                self.__private_activity.set_require_comment_on_start(self.__credentials, require_comment_on_start)
            if require_comment_on_finish != self.__private_activity_require_comment_on_finish:
                self.__private_activity.set_require_comment_on_finish(self.__credentials, require_comment_on_finish)
            if full_screen_reminder != self.__private_activity_full_screen_reminder:
                self.__private_activity.set_full_screen_reminder(self.__credentials, full_screen_reminder)
            self.__result = ModifyPrivateActivityDialogResult.OK
            self.end_modal()
        except Exception as ex:
            ErrorDialog.show(self, ex)

    def __on_cancel(self, evt = None) -> None:
        self.__result = ModifyPrivateActivityDialogResult.CANCEL
        self.end_modal()


