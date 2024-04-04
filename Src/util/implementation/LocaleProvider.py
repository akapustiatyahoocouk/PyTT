#   Python standard library

#   Internal dependencies on modules within the same component
from abc import abstractproperty
from util.implementation.Metaclasses import ABCWithConstants
from util.implementation.Locale import Locale
from util.implementation.PropertyChangeEventProcessorMixin import PropertyChangeEventProcessorMixin

##########
#   Public entities
class LocaleProvider(ABCWithConstants, PropertyChangeEventProcessorMixin):

    ##########
    #   Constants (observable property names)
    LOCALE_PROPERTY_NAME = "locale"
    """ The name of the "locale: Locale" property of a LocaleProvider. """

    ##########
    #   Properties
    @abstractproperty
    def locale(self) -> Locale:
        """ The locale currently "provided" by this locale provider. """
        raise NotImplementedError()

    @locale.setter
    def locale(self, new_locale: str):
        """
            Sets the short user-readable name of the action.

            @param new_locale:
                The new locale to be "provided" by this locale 
                provider; cannot be None.
        """
        raise NotImplementedError()
