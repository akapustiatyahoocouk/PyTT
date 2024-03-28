from typing import TypeAlias

import util

##########
#   AWT implementation

#   Events & event listeners
import awt_impl.InputEventModifiers
import awt_impl.InputEvent
import awt_impl.VirtualKey
import awt_impl.KeyStroke
import awt_impl.KeyEvent
import awt_impl.ActionEvent

#   Events processing mixing
import awt_impl.KeyEventProcessorMixin
import awt_impl.ActionEventProcessorMixin

#   UI widgets
import awt_impl.Widget
import awt_impl.Label
import awt_impl.Button
import awt_impl.Entry
import awt_impl.Separator

#   UI top-level windows
import awt_impl.GuiRoot
import awt_impl.TopFrame
import awt_impl.Dialog

#   TODO how to name this section?
import awt_impl.Action
import awt_impl.MenuItem
import awt_impl.Menu
import awt_impl.MenuBar
import awt_impl.Submenu
import awt_impl.TextMenuItem


##########
#   AWT aliases

#   Events & event listeners
InputEventModifiers: TypeAlias = awt_impl.InputEventModifiers.InputEventModifiers
InputEvent: TypeAlias = awt_impl.InputEvent.InputEvent
VirtualKey: TypeAlias = awt_impl.VirtualKey.VirtualKey
KeyStroke: TypeAlias = awt_impl.KeyStroke.KeyStroke
KeyEventType: TypeAlias = awt_impl.KeyEvent.KeyEventType
KeyEvent: TypeAlias = awt_impl.KeyEvent.KeyEvent
KeyListener: TypeAlias = awt_impl.KeyEvent.KeyListener
ActionEvent: TypeAlias = awt_impl.ActionEvent.ActionEvent
ActionListener: TypeAlias = awt_impl.ActionEvent.ActionListener

#   Events processing mixing
KeyEventProcessorMixin: TypeAlias = awt_impl.KeyEventProcessorMixin.KeyEventProcessorMixin
ActionEventProcessorMixin: TypeAlias = awt_impl.ActionEventProcessorMixin.ActionEventProcessorMixin

#   UI widgets
Widget: TypeAlias = awt_impl.Widget.Widget
Label: TypeAlias = awt_impl.Label.Label
Button: TypeAlias = awt_impl.Button.Button
Entry: TypeAlias = awt_impl.Entry.Entry
Separator: TypeAlias = awt_impl.Separator.Separator

#   UI top-level windows
GuiRoot: TypeAlias = awt_impl.GuiRoot.GuiRoot
TopFrame: TypeAlias = awt_impl.TopFrame.TopFrame
Dialog: TypeAlias = awt_impl.Dialog.Dialog

#   TODO how to name this section?
Action: TypeAlias = awt_impl.Action.Action
MenuItem: TypeAlias = awt_impl.MenuItem.MenuItem
Menu: TypeAlias = awt_impl.Menu.Menu
MenuBar: TypeAlias = awt_impl.MenuBar.MenuBar
Submenu: TypeAlias = awt_impl.Submenu.Submenu
TextMenuItem: TypeAlias = awt_impl.TextMenuItem.TextMenuItem
