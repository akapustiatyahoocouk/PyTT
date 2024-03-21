"""
    GUI skin API.
"""
from abc import ABC, abstractmethod, abstractproperty
from typing import final, Optional

class ISkin(ABC):
    """ A common base class for all "skins" - GUI variants. """

    ##########
    #   object
    def __str__(self) -> str:
        return self.display_name

    ##########
    #   Properties
    @abstractproperty
    def mnemonic(self) -> str:
        """ The mnemonic identifier of this skin. """
        raise NotImplementedError()

    @abstractproperty
    def display_name(self) -> str:
        """ The user-readable display name of this skin. """
        raise NotImplementedError()

    @abstractproperty
    def is_active(self) -> bool:
        """ True if this skin is currently active, else false. """
        raise NotImplementedError()

    ##########
    #   Operations
    @abstractmethod
    def activate(self) -> None:
        """ "Activates" this skin by showing its UI. """
        raise NotImplementedError()

    @abstractmethod
    def deactivate(self) -> None:
        """ "Deactivates" this skin by hiding its UI. """
        raise NotImplementedError()


@final
class ActiveSkin:
    """ The "currently active" skin. """

    ##########
    #   Implementation
    __activeSkin : ISkin = None
    
    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + ' is a utility class'
        
    @staticmethod
    def get() -> Optional[ISkin]:
        """
            Returns the currently "active" skin (if there is one).

            @return:
                The currently "active" skin or None if there isn't one.
        """
        return ActiveSkin.__activeSkin

    @staticmethod
    def set(skin: ISkin) -> None:
        """
            Sets the currently "active" skin.

            @param skin:
                The skin to select as a currently "active" skin,
                None to make sure there is no currently "active" skin.
        """
        if (ActiveSkin.__activeSkin is skin):
            return  # Nothing to do!

        if ActiveSkin.__activeSkin is not None:
            ActiveSkin.__activeSkin.deactivate()
        ActiveSkin.__activeSkin = skin
        if ActiveSkin.__activeSkin is not None:
            ActiveSkin.__activeSkin.activate()


@final
class SkinRegistry:
    """ The registry of known skins. 
        This is an utility class, never to be instantiated."""

    ##########
    #   Implementation data
    __registry : dict[str, ISkin] = {}

    ##########
    #   Construction - not allowed - this is an utility class
    def __init__(self):
        raise NotImplementedError()

    ##########
    #   Operations
    @staticmethod
    def register_skin(skin: ISkin) -> bool:
        """ 'Registers' the specified skin.
            Returns True on  success, False on failure. """
        print('Registering', skin.display_name, 'skin [' + skin.mnemonic + ']')
        if skin.mnemonic in SkinRegistry.__registry:
            return SkinRegistry.__registry[skin.mnemonic] is skin
        else:
            SkinRegistry.__registry[skin.mnemonic] = skin
            return True
        
    @staticmethod
    def find_skin(mnemonic: str) -> Optional[ISkin]:
        """ Finds a registered skinby mnemonic;
            returns None if not found. """
        return SkinRegistry.__registry.get(mnemonic, None)

    @staticmethod
    def get_all_skins() -> set[ISkin]:
        """ Returns a 'set' of all registered skins. """
        return set(SkinRegistry.__registry.values())

    @staticmethod
    def get_default_skin() -> ISkin:
        return SkinRegistry.find_skin('admin')
