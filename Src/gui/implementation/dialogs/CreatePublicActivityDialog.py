""" Implements the "Create public activity" modal dialog. """

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
class CreatePublicActivityDialogResult(Enum):
    """ The result of modal invocation of the CreatePublicActivityDialog. """

    OK = 1
    """ A new BusinessPublicActivity has been created in the specified workspace. """

    CANCEL = 2
    """ Dialog cancelled by user. """

@final
class CreatePublicActivityDialog(Dialog):
    """ The modal "Create public activity " dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget,
                 workspace: Optional[Workspace] = None,
                 credentials: Optional[Credentials] = None):
        """
            Constructs the "create public activity" dialog.

            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used),
                None == no parent.
            @param workspace:
                The workspace to create a new public activity in; None == use
                the CurrentWorkspace.
            @param credentials:
                The credentials to use for workspace access; None == use
                the CurrentCredentials.
            @raise WorkspaceError:
                If a workspace access error occurs.
        """
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("CreatePublicActivityDialog.Title"))

        self.__result = CreatePublicActivityDialogResult.CANCEL
        self.__created_public_activity = None

        #   Resolve workspace & credentials
        assert (workspace is None) or isinstance(workspace, Workspace)
        assert (credentials is None) or isinstance(credentials, Credentials)
        self.__workspace = workspace if workspace is not None else CurrentWorkspace.get()
        self.__credentials = credentials if credentials is not None else CurrentCredentials.get()
        assert self.__workspace is not None
        assert self.__credentials is not None

        self.__validator = self.__workspace.validator

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__name_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreatePublicActivityDialog.NameLabel.Text"),
            anchor=tk.E)
        self.__name_text_field = TextField(self.__controls_panel, width=40)

        self.__description_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreatePublicActivityDialog.DescriptionLabel.Text"),
            anchor=tk.E)
        self.__description_text_area = TextArea(self.__controls_panel, height=4, width=40)

        self.__activity_type_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreatePublicActivityDialog.ActivityTypeLabel.Text"),
            anchor=tk.E)
        self.__activity_type_combo_box = ComboBox(self.__controls_panel)

        self.__timeout_label = Label(
            self.__controls_panel,
            text=GuiResources.string("CreatePublicActivityDialog.TimeoutLabel.Text"),
            anchor=tk.E)
        self.__timeout_panel = Panel(self.__controls_panel)
        self.__timeout_value_combo_box = ComboBox(self.__timeout_panel)
        self.__timeout_unit_combo_box = ComboBox(self.__timeout_panel)

        self.require_comment_on_start_check_box = CheckBox(
            self.__controls_panel,
            text=GuiResources.string("CreatePublicActivityDialog.RequireCommentOnStartCheckBox.Text"))
        self.require_comment_on_finish_check_box = CheckBox(
            self.__controls_panel,
            text=GuiResources.string("CreatePublicActivityDialog.RequireCommentOnFinishCheckBox.Text"))
        self.full_screen_reminder_check_box = CheckBox(
            self.__controls_panel,
            text=GuiResources.string("CreatePublicActivityDialog.FullScreenReminderCheckBox.Text"))

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("CreatePublicActivityDialog.OkButton.Text"),
            image=GuiResources.image("CreatePublicActivityDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("CreatePublicActivityDialog.CancelButton.Text"),
            image=GuiResources.image("CreatePublicActivityDialog.CancelButton.Icon"))

        #   Adjust controls
        self.__description_text_area.accept_tab = False

        for i in range(60):
            if i == 0:
                self.__timeout_value_combo_box.items.add(
                    GuiResources.string("CreatePublicActivityDialog.TimeoutNone"),
                    tag=i)
            else:
                self.__timeout_value_combo_box.items.add(str(i), tag=i)
        self.__timeout_value_combo_box.editable = False

        self.__timeout_unit_combo_box.items.add(
            GuiResources.string("CreatePublicActivityDialog.TimeoutMinutes"),
            tag=1)
        self.__timeout_unit_combo_box.items.add(
            GuiResources.string("CreatePublicActivityDialog.TimeoutHours"),
            tag=60)
        self.__timeout_unit_combo_box.editable = False

        self.__timeout_unit_combo_box.selected_index = 1
        self.__timeout_value_combo_box.selected_index = 1

        self.__activity_type_combo_box.editable = False
        self.__activity_type_combo_box.items.add("-", tag=None)
        activity_types = list(self.__workspace.get_activity_types(self.__credentials))
        activity_types.sort(key=lambda u: u.get_name(self.__credentials))
        for activity_type in activity_types:
            self.__activity_type_combo_box.items.add(activity_type.display_name, tag=activity_type)
        self.__activity_type_combo_box.selected_index = 0

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

        self.require_comment_on_start_check_box.grid(row=4, column=1, padx=2, pady=2, sticky="W")
        self.require_comment_on_finish_check_box.grid(row=5, column=1, padx=2, pady=2, sticky="W")
        self.full_screen_reminder_check_box.grid(row=6, column=1, padx=2, pady=2, sticky="W")

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
    def result(self) -> CreatePublicActivityDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    @property
    def created_public_activity(self) -> Optional[BusinessPublicActivity]:
        """ The BusinessPublicActivity created during dialog invocation;
            None if the dialog was cancelled. """
        return self.__created_public_activity

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
        require_comment_on_start = self.require_comment_on_start_check_box.checked
        require_comment_on_finish = self.require_comment_on_finish_check_box.checked
        full_screen_reminder = self.full_screen_reminder_check_box.checked

        try:
            self.__created_public_activity = self.__workspace.create_public_activity(
                    credentials=self.__credentials,
                    name=name,
                    description=description,
                    activity_type=activity_type,
                    timeout=timeout,
                    require_comment_on_start=require_comment_on_start,
                    require_comment_on_finish=require_comment_on_finish,
                    full_screen_reminder=full_screen_reminder)
            self.__result = CreatePublicActivityDialogResult.OK
            self.end_modal()
        except Exception as ex:
            ErrorDialog.show(self, ex)

    def __on_cancel(self, evt = None) -> None:
        self.__result = CreatePublicActivityDialogResult.CANCEL
        self.end_modal()
