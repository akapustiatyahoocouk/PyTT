from typing import  Any
import inspect

class FriendlyMeta(type):
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
            self.__friends = []

    def __getattr__(cls: type, attr: str) -> Any:
        for friend in cls.__friends:
            an = attr.replace(friend, cls.__name__)
            try:
                return type.__getattribute__(cls, an)
            except Exception as ex:
                print(ex)
                pass
        return type.__getattribute__(cls, attr)
