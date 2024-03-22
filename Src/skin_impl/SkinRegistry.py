from typing import final, Optional

import skin_impl.ISkin
import admin_skin_impl.AdminSkin

@final
class SkinRegistry:
    """ The registry of known skins. 
        This is an utility class, never to be instantiated."""

    ##########
    #   Implementation data
    __registry : dict[str, skin_impl.ISkin.ISkin] = {}

    ##########
    #   Construction - not allowed - this is an utility class
    def __init__(self):
        raise NotImplementedError()

    ##########
    #   Operations
    @staticmethod
    def register_skin(skin: skin_impl.ISkin.ISkin) -> bool:
        """ "Registers" the specified skin.
            Returns True on  success, False on failure. """
        print("Registering", skin.display_name, "skin [" + skin.mnemonic + "]")
        if skin.mnemonic in SkinRegistry.__registry:
            return SkinRegistry.__registry[skin.mnemonic] is skin
        else:
            SkinRegistry.__registry[skin.mnemonic] = skin
            return True
        
    @staticmethod
    def find_skin(mnemonic: str) -> Optional[skin_impl.ISkin.ISkin]:
        """ Finds a registered skinby mnemonic;
            returns None if not found. """
        return SkinRegistry.__registry.get(mnemonic, None)

    @staticmethod
    def get_all_skins() -> set[skin_impl.ISkin.ISkin]:
        """ Returns a 'set' of all registered skins. """
        return set(SkinRegistry.__registry.values())

    @staticmethod
    def get_default_skin() -> skin_impl.ISkin.ISkin:
        #return SkinRegistry.find_skin("admin")
        return admin_skin_impl.AdminSkin.AdminSkin.instance

