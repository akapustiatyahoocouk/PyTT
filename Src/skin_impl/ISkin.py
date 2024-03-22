from abc import ABC, abstractmethod, abstractproperty

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

