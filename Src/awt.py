from typing import TypeAlias

import resources

import awt_impl.InputEvent
import awt_impl.VirtualKey
import awt_impl.KeyEvent
import awt_impl.KeyEventListener
import awt_impl.ActionEvent
import awt_impl.ActionEventListener
import awt_impl.KeyEventProcessorMixin

import awt_impl.Button

import awt_impl.GuiRoot
import awt_impl.TopFrame
import awt_impl.Dialog

InputEvent: TypeAlias = awt_impl.InputEvent.InputEvent
VirtualKey: TypeAlias = awt_impl.VirtualKey.VirtualKey
KeyEventType: TypeAlias = awt_impl.KeyEvent.KeyEventType
KeyEvent: TypeAlias = awt_impl.KeyEvent.KeyEvent
KeyEventListener: TypeAlias = awt_impl.KeyEventListener.KeyEventListener
ActionEvent: TypeAlias = awt_impl.ActionEvent.ActionEvent
ActionEventListener: TypeAlias = awt_impl.ActionEventListener.ActionEventListener

KeyEventProcessorMixin: TypeAlias = awt_impl.KeyEventProcessorMixin.KeyEventProcessorMixin

Button: TypeAlias = awt_impl.Button.Button

GuiRoot: TypeAlias = awt_impl.GuiRoot.GuiRoot
TopFrame: TypeAlias = awt_impl.TopFrame.TopFrame
Dialog: TypeAlias = awt_impl.Dialog.Dialog
