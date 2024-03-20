import re
from typing import Any

class ReadOnlyClassConstantsMetaclass(type):  # TODO rename ?
    def __setattr__(cls: type, attr: str, value) -> None:
        #print(cls.__name__, attr, value)
        if re.match('^[A-Z0-9_]+$', attr):
            raise Exception('Cannot change class constant value ' + cls.__name__ + '.' + attr)
        type.__setattr__(cls, attr, value)

class classproperty():
    """ A property annotation for a static (class-level) property """
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner) -> Any:
        return self.f(owner)

    def __setattr__(self, attr, value) -> None:
        #print(self, attr, value)
        super().__setattr__(attr, value)
