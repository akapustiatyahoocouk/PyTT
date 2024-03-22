from typing import TypeAlias, Callable

import awt_impl.KeyEvent

KeyEventListener: TypeAlias = Callable[[awt_impl.KeyEvent.KeyEvent], None]
""" A signature of a listener to key events - a function
    or a bound method. """

