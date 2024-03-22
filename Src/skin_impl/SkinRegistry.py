from typing import final, Optional

@final
class SkinRegistry:
    """ The registry of known skins. 
        This is an utility class, never to be instantiated."""

    ##########
    #   Implementation data
    __registry : dict[str, 'skin.ISkin'] = {}

    ##########
    #   Construction - not allowed - this is an utility class
    def __init__(self):
        raise NotImplementedError()

    ##########
    #   Operations
    @staticmethod
    def register_skin(skin: 'skin.ISkin') -> bool:
        """ 'Registers' the specified skin.
            Returns True on  success, False on failure. """
        print('Registering', skin.display_name, 'skin [' + skin.mnemonic + ']')
        if skin.mnemonic in SkinRegistry.__registry:
            return SkinRegistry.__registry[skin.mnemonic] is skin
        else:
            SkinRegistry.__registry[skin.mnemonic] = skin
            return True
        
    @staticmethod
    def find_skin(mnemonic: str) -> Optional['skin.ISkin']:
        """ Finds a registered skinby mnemonic;
            returns None if not found. """
        return SkinRegistry.__registry.get(mnemonic, None)

    @staticmethod
    def get_all_skins() -> set['skin.ISkin']:
        """ Returns a 'set' of all registered skins. """
        return set(SkinRegistry.__registry.values())

    @staticmethod
    def get_default_skin() -> 'skin.ISkin':
        return SkinRegistry.find_skin('admin')

