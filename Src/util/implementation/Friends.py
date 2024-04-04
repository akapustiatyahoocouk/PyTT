#   Python standard library
from typing import  Any
from abc import ABC, ABCMeta

##########
#   Public entities
class FriendlyClassMeta(type):
    """ TODO document """

    ##########
    #   object (methods for class properties access from friends)
    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        return super().__prepare__(name, bases, **kwargs)

    def __new__(metacls, name, bases, namespace, **kwargs):
        return super().__new__(metacls, name, bases, namespace)

    def __init__(self, *args, **kwargs):
        if "friends" in kwargs:
            self.__friends = kwargs["friends"];
            if not isinstance(self.__friends, tuple):
                raise NotImplementedError("Friends declaration must be a tuple")
            for i in range(len(self.__friends)):
                friend = self.__friends[i]
                if isinstance(friend, str):
                    pass    # use type name "as is"
                elif isinstance(friend, type):
                    self.__friends[i] = friend.__name__
                else:
                    raise NotImplementedError(str(friend) + " cannot be used as a friend declarator")
        else:
            self.__friends = ()

    def __getattr__(cls: type, attr: str) -> Any:
        for friend in cls.__friends:
            an = attr.replace(friend, cls.__name__)
            try:
                return type.__getattribute__(cls, an)
            except Exception as ex:
                print(ex)
                pass
        return type.__getattribute__(cls, attr)


class FriendlyClass(metaclass=FriendlyClassMeta, friends = ()):
    """ 
        The base class for non-abstract classes that allow declared
        "friend" casses to access private properties of the dclared 
        class.
        
        In addition to allowing "friend" classes to access static
        private properties of the declared class (which is provided
        by FriendlyMeta), the Friendly base class also includes 
        support for instance properties.
        
        @param friends:
            A tuple whose elements are either friend classes or
            names of friend classes.
    """
    ##########
    #   object (methods for instance properties access from friends)
    def __getattr__(self, name: str) -> Any:
        if name != "__name__":
            for friend in self.__class__._FriendlyMeta__friends:
                an = name.replace(friend, self.__class__.__name__)
                try:
                    return super().__getattribute__(an)
                except:
                    pass
        return super().__getattribute__(name)


#   TODO FriendlyABC, etc.

class FriendlyABCMeta(ABCMeta, FriendlyClassMeta):
    """ TODO document """
    #def __new__(mcls, name, bases, namespace, /, **kwargs):
    #    ABCMeta.__new__(mcls, name, bases, namespace, **kwargs)
    #    FriendlyMeta.__new__(mcls, name, bases, namespace, **kwargs)
    pass

class FriendlyABC(ABC, metaclass=FriendlyABCMeta, friends = ()):
    """ 
        A FriendlyClass that is also abstract, i.e. cannot be
        instantiated directly.

        @param friends:
            A tuple whose elements are either friend classes or
            names of friend classes.
     """
    pass
