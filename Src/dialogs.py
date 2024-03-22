from typing import TypeAlias

import dialogs_impl.AboutDialog
import dialogs_impl.LoginDialog

AboutDialog: TypeAlias = dialogs_impl.AboutDialog.AboutDialog
AboutDialogResult: TypeAlias = dialogs_impl.AboutDialog.AboutDialogResult

LoginDialog: TypeAlias = dialogs_impl.LoginDialog.LoginDialog
LoginDialogResult: TypeAlias = dialogs_impl.LoginDialog.LoginDialogResult
