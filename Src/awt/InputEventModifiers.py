from typing import final

from util_api import staticproperty, ClassWithConstants

@final
class InputEventModifiers(ClassWithConstants):
    """ 
        An instance of this class represents a combination of zero
        or more "input event modifiers".
        IMPORTANT: Uses tk.Event - style encoding!
    """

    ##########
    #   Implementation
    __SHIFT_FLAG = 0x00000001
    __LOCK_FLAG = 0x00000002
    __CONTROL_FLAG = 0x00000004
    __ALT_FLAG = 0x00020000
    __NUMPAD_FLAG = 0x00040000
    __NONE_FLAGS = 0x00000000
    __ALL_FLAGS = 0x00060007

    __FLAG_NAMES = {
        __SHIFT_FLAG: "Shift",
        __LOCK_FLAG: "Lock",
        __CONTROL_FLAG: "Ctrl",
        __ALT_FLAG: "Alt",
        __NUMPAD_FLAG: "NumPad"
    }
    
    __shift_instance = None
    __lock_instance = None
    __control_instance = None
    __alt_instance = None
    __numpad_instance = None
    __none_instance = None
    __all_instance = None

    ##########
    #   Constants (indifidual modifiers)
    @staticproperty
    def SHIFT() -> 'InputEventModifiers':
        if InputEventModifiers.__shift_instance is None:
            InputEventModifiers.__shift_instance = InputEventModifiers(InputEventModifiers.__SHIFT_FLAG)
        return InputEventModifiers.__shift_instance
    
    @staticproperty
    def LOCK() -> 'InputEventModifiers':
        if InputEventModifiers.__lock_instance is None:
            InputEventModifiers.__lock_instance = InputEventModifiers(InputEventModifiers.__LOCK_FLAG)
        return InputEventModifiers.__lock_instance

    @staticproperty
    def CONTROL() -> 'InputEventModifiers':
        if InputEventModifiers.__control_instance is None:
            InputEventModifiers.__control_instance = InputEventModifiers(InputEventModifiers.__CONTROL_FLAG)
        return InputEventModifiers.__control_instance

    @staticproperty
    def ALT() -> 'InputEventModifiers':
        if InputEventModifiers.__alt_instance is None:
            InputEventModifiers.__alt_instance = InputEventModifiers(InputEventModifiers.__ALT_FLAG)
        return InputEventModifiers.__alt_instance

    @staticproperty
    def NUMPAD() -> 'InputEventModifiers':
        if InputEventModifiers.__numpad_instance is None:
            InputEventModifiers.__numpad_instance = InputEventModifiers(InputEventModifiers.__NUMPAD_FLAGS)
        return InputEventModifiers.__numpad_instance

    ##########
    #   Constants (modifier sets)
    @staticproperty
    def NONE() -> 'InputEventModifiers':
        if InputEventModifiers.__none_instance is None:
            InputEventModifiers.__none_instance = InputEventModifiers(InputEventModifiers.__NONE_FLAGS)
        return InputEventModifiers.__none_instance

    @staticproperty
    def ALL() -> 'InputEventModifiers':
        if InputEventModifiers.__all_instance is None:
            InputEventModifiers.__all_instance = InputEventModifiers(InputEventModifiers.__ALL_FLAGS)
        return InputEventModifiers.__all_instance

    ##########
    #   Construction
    def __init__(self, bitmask: int):
        self.__bitmask = bitmask & InputEventModifiers.__ALL_FLAGS

    ##########
    #   object (operators)
    def __str__(self) -> str:
        #   TODO cache for performance in a __bitmask -> result dict
        result = ''
        for flag in [InputEventModifiers.__CONTROL_FLAG,
                     InputEventModifiers.__SHIFT_FLAG,
                     InputEventModifiers.__ALT_FLAG,
                     InputEventModifiers.__LOCK_FLAG,
                     InputEventModifiers.__NUMPAD_FLAG]:
            if (self.__bitmask & flag) != 0:
                result += "+"
                result += InputEventModifiers.__FLAG_NAMES[flag];
        return result if len(result) == 0 else result[1:]
    
    def __contains__(self, item: 'InputEventModifiers') -> bool:
        assert isinstance(self, InputEventModifiers)
        assert isinstance(item, InputEventModifiers)
        return (self.__bitmask & item.__bitmask) == item.__bitmask

    #   TODO cache instances for flag combinations to avoid creating
    #   multiple InputEventModifiers instances with the same __bitmask    
    def __eq__(self, op2: 'InputEventModifiers') -> bool:
        assert isinstance(self, InputEventModifiers)
        if not isinstance(op2, InputEventModifiers):
            return False
        return self.__bitmask == op2.__bitmask

    def __ne__(self, op2: 'InputEventModifiers') -> bool:
        assert isinstance(self, InputEventModifiers)
        if not isinstance(op2, InputEventModifiers):
            return True
        return self.__bitmask != op2.__bitmask

    def __and__(self, op2: 'InputEventModifiers') -> 'InputEventModifiers':
        assert isinstance(self, InputEventModifiers)
        assert isinstance(op2, InputEventModifiers)
        return InputEventModifiers(self.__bitmask & op2.__bitmask)

    def __or__(self, op2: 'InputEventModifiers') -> 'InputEventModifiers':
        assert isinstance(self, InputEventModifiers)
        assert isinstance(op2, InputEventModifiers)
        return InputEventModifiers(self.__bitmask | op2.__bitmask)

    def __xor__(self, op2: 'InputEventModifiers') -> 'InputEventModifiers':
        assert isinstance(self, InputEventModifiers)
        assert isinstance(op2, InputEventModifiers)
        return InputEventModifiers(self.__bitmask ^ op2.__bitmask)
