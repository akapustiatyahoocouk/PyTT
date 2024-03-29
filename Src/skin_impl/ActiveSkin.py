from typing import final, Optional

from skin_impl.Skin import Skin

@final
class ActiveSkin:
    """ The "currently active" skin. """

    ##########
    #   Implementation
    __activeSkin : Skin = None
    
    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + " is a utility class"
    
    #   TODO can we move this functionality to "Skin.current" static property ?
    @staticmethod
    def get() -> Optional[Skin]:
        """
            Returns the currently "active" skin (if there is one).

            @return:
                The currently "active" skin or None if there isn't one.
        """
        return ActiveSkin.__activeSkin

    @staticmethod
    def set(skin: Optional[Skin]) -> None:
        """
            Sets the currently "active" skin.

            @param skin:
                The skin to select as a currently "active" skin,
                None to make sure there is no currently "active" skin.
        """
        assert (skin is None) or isinstance(skin, Skin)

        if (ActiveSkin.__activeSkin is skin):
            return  # Nothing to do!

        if ActiveSkin.__activeSkin is not None:
            ActiveSkin.__activeSkin.deactivate()
        ActiveSkin.__activeSkin = skin
        if ActiveSkin.__activeSkin is not None:
            ActiveSkin.__activeSkin.activate()
