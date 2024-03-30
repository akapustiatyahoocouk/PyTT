"""
    The AWT API.
"""

#   Events & event listeners
from awt.InputEventModifiers import *
from awt.InputEvent import *
from awt.VirtualKey import *
from awt.KeyStroke import *
from awt.KeyEvent import *
from awt.ActionEvent import *
from awt.PropertyChangeEvent import *

#   Events processing mixing
from awt.KeyEventProcessorMixin import *
from awt.ActionEventProcessorMixin import *
from awt.PropertyChangeEventProcessorMixin import *

#   UI widgets
from awt.Widget import *
from awt.Label import *
from awt.Button import *
from awt.Entry import *
from awt.Separator import *

#   UI top-level windows
from awt.GuiRoot import *
from awt.TopFrame import *
from awt.Dialog import *

#   TODO how to name this section?
from awt.Action import *
from awt.MenuItem import *
from awt.Menu import *
from awt.MenuBar import *
from awt.Submenu import *
from awt.SimpleMenuItem import *
