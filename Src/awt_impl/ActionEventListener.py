from typing import TypeAlias, Callable

import awt_impl.ActionEvent

ActionEventListener: TypeAlias = Callable[[awt_impl.ActionEvent.ActionEvent], None]
""" A signature of a listener to action events - a function
    or a bound method. """

