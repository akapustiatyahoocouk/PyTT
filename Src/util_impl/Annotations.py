"""
    Various annotations used throughout the code base.
    These will typically be imported via "from util import <annotation(s)>".
"""
from typing import Any

class classproperty():
    """ A property annotation for a static (class-level) property """
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner) -> Any:
        return self.f(owner)

    def __setattr__(self, attr, value) -> None:
        #print(self, attr, value)
        super().__setattr__(attr, value)


class staticproperty():
    """ A property annotation for a static (class-level wth no "cls") property """
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner) -> Any:
        return self.f()

    def __setattr__(self, attr, value) -> None:
        #print(self, attr, value)
        super().__setattr__(attr, value)
