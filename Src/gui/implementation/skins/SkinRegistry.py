#   Python standard library
from typing import final, Optional

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from .Skin import Skin

##########
#   Public entities
@final
class SkinRegistry: #   TODO move static services to Skin!
    """ The registry of known skins.
        This is an utility class, never to be instantiated."""

    ##########
    #   Implementation data
    __registry : dict[str, Skin] = {}

    ##########
    #   Construction - not allowed - this is an utility class
    def __init__(self):
        raise NotImplementedError()

    ##########
    #   Operations
    @staticmethod
    def register_skin(skin: Skin) -> bool:
        """
            "Registers" the specified skin.

            @param skin:
                The skin to register.
            @return:
                True on successful registration, False on failure.
        """
        assert isinstance(skin, Skin) and (skin.mnemonic is not None)

        #   Use some sort of progress bar on a splash screen instead ?
        print("Registering", skin.display_name, "skin [" + skin.mnemonic + "]")

        if skin.mnemonic in SkinRegistry.__registry:
            return SkinRegistry.__registry[skin.mnemonic] is skin
        else:
            SkinRegistry.__registry[skin.mnemonic] = skin
            return True

    @staticmethod
    def find_skin(mnemonic: str) -> Optional[Skin]:
        """
            Finds a registered skin by mnemonic.

            @param mnemonic:
                The mnemonic to look for.
            @return:
                The skin with the required mnemonic, None if not found.
        """
        return SkinRegistry.__registry.get(mnemonic, None)

    @staticproperty
    def all_skins() -> set[Skin]:
        """ The set of all registered skins. """
        return set(SkinRegistry.__registry.values())

    @staticproperty
    def default_skin() -> Skin:
        """ The "default" skin to use. """
        from admin_skin.implementation.AdminSkin import AdminSkin
        return AdminSkin.instance

