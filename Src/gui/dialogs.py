from typing import TypeAlias

import gui.dlg_impl.Dialog
import gui.dlg_impl.AboutDialog
import gui.dlg_impl.LoginDialog

Dialog: TypeAlias = gui.dlg_impl.Dialog.Dialog

AboutDialog: TypeAlias = gui.dlg_impl.AboutDialog.AboutDialog
AboutDialogResult: TypeAlias = gui.dlg_impl.AboutDialog.AboutDialogResult

LoginDialog: TypeAlias = gui.dlg_impl.LoginDialog.LoginDialog
LoginDialogResult: TypeAlias = gui.dlg_impl.LoginDialog.LoginDialogResult
