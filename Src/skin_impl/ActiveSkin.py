from typing import final, Optional

import skin_impl.ISkin

@final
class ActiveSkin:
    """ The "currently active" skin. """

    ##########
    #   Implementation
    __activeSkin : skin_impl.ISkin.ISkin = None
    
    ##########
    #   Construction - disable (this is an utility class)
    def __init__(self):
        assert False, str(self.__class__) + ' is a utility class'
        
    @staticmethod
    def get() -> Optional[skin_impl.ISkin.ISkin]:
        """
            Returns the currently "active" skin (if there is one).

            @return:
                The currently "active" skin or None if there isn't one.
        """
        return ActiveSkin.__activeSkin

    @staticmethod
    def set(skin: skin_impl.ISkin.ISkin) -> None:
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

