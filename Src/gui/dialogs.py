from typing import TypeAlias

import gui.dialogs_impl.Dialog
import gui.dialogs_impl.AboutDialog
import gui.dialogs_impl.LoginDialog

Dialog: TypeAlias = gui.dialogs_impl.Dialog.Dialog

AboutDialog: TypeAlias = gui.dialogs_impl.AboutDialog.AboutDialog
AboutDialogResult: TypeAlias = gui.dialogs_impl.AboutDialog.AboutDialogResult

LoginDialog: TypeAlias = gui.dialogs_impl.LoginDialog.LoginDialog
LoginDialogResult: TypeAlias = gui.dialogs_impl.LoginDialog.LoginDialogResult
