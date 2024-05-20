""" Implements the "Modify public task" modal dialog. """

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
class ModifyPublicTaskDialogResult(Enum):
    """ The result of modal invocation of the ModifyPublicTaskDialog. """

    OK = 1
    """ A BusinessPublicTask has been modified. """

    CANCEL = 2
    """ Dialog cancelled by user. """

@final
class ModifyPublicTaskDialog(Dialog):
    """ The modal "Modify public task " dialog. """

    ##########
    #   Construction
    def __init__(self, parent: tk.BaseWidget,
                 public_task: BusinessPublicTask,
                 credentials: Optional[Credentials] = None):
        """
            Constructs the "Modify public task" dialog.

            @param parent:
                The parent widget for the dialog (actually the closest
                enclosing top-level widget or frame is used),
                None == no parent.
            @param public_task:
                The public task to modify.
            @param credentials:
                The credentials to use for workspace access; None == use
                the CurrentCredentials.
            @raise WorkspaceError:
                If a workspace access error occurs.
        """
        Dialog.__init__(self,
                        parent,
                        GuiResources.string("ModifyPublicTaskDialog.Title"))

        self.__result = ModifyPublicTaskDialogResult.CANCEL

        assert isinstance(public_task, BusinessPublicTask)
        self.__public_task = public_task

        #   Resolve credentials
        assert (credentials is None) or isinstance(credentials, Credentials)
        self.__credentials = credentials if credentials is not None else CurrentCredentials.get()
        assert self.__credentials is not None

        #   Save current public task properties
        self.__public_task_name = public_task.get_name(self.__credentials)
        self.__public_task_description = public_task.get_description(self.__credentials)
        self.__public_task_activity_type = public_task.get_activity_type(self.__credentials)
        self.__public_task_timeout = public_task.get_timeout(self.__credentials)
        self.__public_task_require_comment_on_start = public_task.get_require_comment_on_start(self.__credentials)
        self.__public_task_require_comment_on_finish = public_task.get_require_comment_on_finish(self.__credentials)
        self.__public_task_full_screen_reminder = public_task.get_full_screen_reminder(self.__credentials)
        self.__public_task_completed = public_task.is_completed(self.__credentials)
        self.__public_task_parent_task = public_task.get_parent(self.__credentials)
        self.__validator = public_task.workspace.validator

        #   Create controls
        self.__controls_panel = Panel(self)

        self.__name_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyPublicTaskDialog.NameLabel.Text"),
            anchor=tk.E)
        self.__name_text_field = TextField(self.__controls_panel, width=40)

        self.__description_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyPublicTaskDialog.DescriptionLabel.Text"),
            anchor=tk.E)
        self.__description_text_area = TextArea(self.__controls_panel, height=4, width=40)

        self.__subtask_of_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyPublicTaskDialog.SubtaskOfLabel.Text"),
            anchor=tk.E)
        self.__subtask_of_combo_box = ComboBox(self.__controls_panel)

        self.__activity_type_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyPublicTaskDialog.ActivityTypeLabel.Text"),
            anchor=tk.E)
        self.__activity_type_combo_box = ComboBox(self.__controls_panel)

        self.__timeout_label = Label(
            self.__controls_panel,
            text=GuiResources.string("ModifyPublicTaskDialog.TimeoutLabel.Text"),
            anchor=tk.E)
        self.__timeout_panel = Panel(self.__controls_panel)
        self.__timeout_value_combo_box = ComboBox(self.__timeout_panel)
        self.__timeout_unit_combo_box = ComboBox(self.__timeout_panel)

        self.__require_comment_on_start_check_box = CheckBox(
            self.__controls_panel,
            text=GuiResources.string("ModifyPublicTaskDialog.RequireCommentOnStartCheckBox.Text"))
        self.__require_comment_on_finish_check_box = CheckBox(
            self.__controls_panel,
            text=GuiResources.string("ModifyPublicTaskDialog.RequireCommentOnFinishCheckBox.Text"))
        self.__full_screen_reminder_check_box = CheckBox(
            self.__controls_panel,
            text=GuiResources.string("ModifyPublicTaskDialog.FullScreenReminderCheckBox.Text"))

        self.__completed_check_box = CheckBox(
            self.__controls_panel,
            text=GuiResources.string("ModifyPublicTaskDialog.CompletedCheckBox.Text"))

        self.__separator = Separator(self, orient="horizontal")

        self.__ok_button = Button(self,
            text=GuiResources.string("ModifyPublicTaskDialog.OkButton.Text"),
            image=GuiResources.image("ModifyPublicTaskDialog.OkButton.Icon"))
        self.__cancel_button = Button(self,
            text=GuiResources.string("ModifyPublicTaskDialog.CancelButton.Text"),
            image=GuiResources.image("ModifyPublicTaskDialog.CancelButton.Icon"))

        #   Adjust controls
        self.__name_text_field.text = self.__public_task_name
        
        self.__description_text_area.text = self.__public_task_description
        self.__description_text_area.accept_tab = False

        self.__subtask_of_combo_box.editable = False
        self.__subtask_of_combo_box.items.add(
            GuiResources.string("ModifyPublicTaskDialog.SubtaskOfComboBox.None"),
            tag=None)
        self.__fill_subtask_of_combo_box(self.__public_task.workspace.get_root_public_tasks(self.__credentials), 0)
        for i in range(len(self.__subtask_of_combo_box.items)):
            if self.__subtask_of_combo_box.items[i].tag == self.__public_task_parent_task:
                self.__subtask_of_combo_box.selected_index = i
                break

        for i in range(60):
            if i == 0:
                self.__timeout_value_combo_box.items.add(
                    GuiResources.string("ModifyPublicTaskDialog.TimeoutNone"),
                    tag=i)
            else:
                self.__timeout_value_combo_box.items.add(str(i), tag=i)
        self.__timeout_value_combo_box.editable = False

        self.__timeout_unit_combo_box.items.add(
            GuiResources.string("ModifyPublicTaskDialog.TimeoutMinutes"),
            tag=1)
        self.__timeout_unit_combo_box.items.add(
            GuiResources.string("ModifyPublicTaskDialog.TimeoutHours"),
            tag=60)
        self.__timeout_unit_combo_box.editable = False

        if self.__public_task_timeout is None:
            self.__timeout_value_combo_box.selected_index = 0
            self.__timeout_unit_combo_box.selected_index = 1
        elif (self.__public_task_timeout > 0 and
              self.__public_task_timeout < 60):
            self.__timeout_value_combo_box.selected_index = self.__public_task_timeout
            self.__timeout_unit_combo_box.selected_index = 0
        elif (self.__public_task_timeout % 60 == 0 and
              self.__public_task_timeout // 60 > 0 and
              self.__public_task_timeout // 60 <= 60):
            self.__timeout_value_combo_box.selected_index = self.__public_task_timeout // 60
            self.__timeout_unit_combo_box.selected_index = 1
        else:
            self.__timeout_value_combo_box.selected_index = 1
            self.__timeout_unit_combo_box.selected_index = 1

        self.__activity_type_combo_box.editable = False
        self.__activity_type_combo_box.items.add("-", tag=None)
        activity_types = list(self.__public_task.workspace.get_activity_types(self.__credentials))
        activity_types.sort(key=lambda u: u.display_name)
        for activity_type in activity_types:
            self.__activity_type_combo_box.items.add(activity_type.display_name, tag=activity_type)
        self.__activity_type_combo_box.selected_index = (
            0 if self.__public_task_activity_type is None
            else activity_types.index(self.__public_task_activity_type) + 1)

        self.__require_comment_on_start_check_box.checked = self.__public_task_require_comment_on_start
        self.__require_comment_on_finish_check_box.checked = self.__public_task_require_comment_on_finish
        self.__full_screen_reminder_check_box.checked = self.__public_task_full_screen_reminder
        self.__completed_check_box.checked = self.__public_task_completed
        
        #   Set up control structure
        self.__controls_panel.pack(fill=tk.X, padx=0, pady=0)
        self.__controls_panel.columnconfigure(1, weight=10)

        self.__name_label.grid(row=0, column=0, padx=2, pady=2, sticky="W")
        self.__name_text_field.grid(row=0, column=1, padx=2, pady=2, sticky="WE")

        self.__description_label.grid(row=1, column=0, padx=2, pady=2, sticky="W")
        self.__description_text_area.grid(row=1, column=1, padx=2, pady=2, sticky="WE")

        self.__subtask_of_label.grid(row=2, column=0, padx=2, pady=2, sticky="W")
        self.__subtask_of_combo_box.grid(row=2, column=1, padx=2, pady=2, sticky="WE")

        self.__activity_type_label.grid(row=3, column=0, padx=2, pady=2, sticky="W")
        self.__activity_type_combo_box.grid(row=3, column=1, padx=2, pady=2, sticky="WE")

        self.__timeout_label.grid(row=4, column=0, padx=2, pady=2, sticky="W")
        self.__timeout_panel.grid(row=4, column=1, padx=0, pady=0, sticky="W")
        self.__timeout_value_combo_box.pack(side=tk.LEFT, padx=2, pady=2)
        self.__timeout_unit_combo_box.pack(side=tk.LEFT, padx=2, pady=2)

        self.__require_comment_on_start_check_box.grid(row=5, column=1, padx=2, pady=2, sticky="W")
        self.__require_comment_on_finish_check_box.grid(row=6, column=1, padx=2, pady=2, sticky="W")
        self.__full_screen_reminder_check_box.grid(row=7, column=1, padx=2, pady=2, sticky="W")
        self.__completed_check_box.grid(row=8, column=1, padx=2, pady=2, sticky="W")

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
    def result(self) -> ModifyPublicTaskDialogResult:
        """ The dialog result after a modal invocation. """
        return self.__result

    ##########
    #   Implementation helpers    
    def __fill_subtask_of_combo_box(self, public_tasks: Set[BusinessPublicTask], level: int) -> None:
        public_tasks = list(public_tasks)
        try:
            public_tasks.sort(key=lambda u: u.display_name)
        except Exception as ex:
            pass    #   TODO log the exception
        for public_task in public_tasks:
            if public_task is not self.__public_task:
                text = "    " * level + public_task.display_name
                self.__subtask_of_combo_box.items.add(text, tag=public_task)
                self.__fill_subtask_of_combo_box(public_task.get_children(self.__credentials), level + 1)
            
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
        parent_task = self.__subtask_of_combo_box.selected_item.tag
        activity_type = self.__activity_type_combo_box.selected_item.tag
        timeout = (self.__timeout_value_combo_box.selected_item.tag *
                   self.__timeout_unit_combo_box.selected_item.tag)
        if timeout == 0:
            timeout = None
        require_comment_on_start = self.__require_comment_on_start_check_box.checked
        require_comment_on_finish = self.__require_comment_on_finish_check_box.checked
        full_screen_reminder = self.__full_screen_reminder_check_box.checked
        completed = self.__completed_check_box.checked

        try:
            if name != self.__public_task_name:
                self.__public_task.set_name(self.__credentials, name)
            if description != self.__public_task_description:
                self.__public_task.set_description(self.__credentials,description)
            if activity_type != self.__public_task_activity_type:
                self.__public_task.set_activity_type(self.__credentials, activity_type)
            if timeout != self.__public_task_timeout:
                self.__public_task.set_timeout(self.__credentials, timeout)
            if require_comment_on_start != self.__public_task_require_comment_on_start:
                self.__public_task.set_require_comment_on_start(self.__credentials, require_comment_on_start)
            if require_comment_on_finish != self.__public_task_require_comment_on_finish:
                self.__public_task.set_require_comment_on_finish(self.__credentials, require_comment_on_finish)
            if full_screen_reminder != self.__public_task_full_screen_reminder:
                self.__public_task.set_full_screen_reminder(self.__credentials, full_screen_reminder)
            if completed != self.__public_task_completed:
                self.__public_task.set_completed(self.__credentials, completed)
            if parent_task != self.__public_task_parent_task:
                self.__public_task.set_parent(self.__credentials, parent_task)
            self.__result = ModifyPublicTaskDialogResult.OK
            self.end_modal()
        except Exception as ex:
            ErrorDialog.show(self, ex)

    def __on_cancel(self, evt = None) -> None:
        self.__result = ModifyPublicTaskDialogResult.CANCEL
        self.end_modal()
