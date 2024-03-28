import re
from abc import ABC, ABCMeta, abstractproperty

class ClassWithConstantsMeta(type):
    def __setattr__(cls: type, attr: str, value) -> None:
        #print(cls.__name__, attr, value)
        if re.match("^[A-Z0-9_]+$", attr):
            raise Exception("Cannot change class constant value " + cls.__name__ + "." + attr)
        type.__setattr__(cls, attr, value)

class ClassWithConstants(metaclass=ClassWithConstantsMeta):
    pass

class ABCWithConstantsMeta(ABCMeta, ClassWithConstantsMeta):
    pass

class ABCWithConstants(metaclass=ABCWithConstantsMeta):
    pass
