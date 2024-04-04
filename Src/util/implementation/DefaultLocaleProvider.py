
#   Internal dependencies on modules within the same component
from util.implementation.Annotations import staticproperty
from util.implementation.Locale import Locale
from util.implementation.LocaleProvider import LocaleProvider

##########
#   Public entities
class DefaultLocaleProvider(LocaleProvider):
    
    ##########
    #   Singleton
    __instance_acquisition_in_progress = False
    __instance : LocaleProvider = None

    def __init__(self):
        assert DefaultLocaleProvider.__instance_acquisition_in_progress, "Use DefaultLocaleProvider.instance instead"
        LocaleProvider.__init__(self)

    @staticproperty
    def instance() -> "DefaultLocaleProvider":
        """
            Returns one and only instance of this class, creating
            it on the first call.
            
            @return:
                The one and only instance of this class.
        """
        if DefaultLocaleProvider.__instance is None:
            DefaultLocaleProvider.__instance_acquisition_in_progress = True
            DefaultLocaleProvider.__instance = DefaultLocaleProvider()
            DefaultLocaleProvider.__instance_acquisition_in_progress = False
        return DefaultLocaleProvider.__instance

    ##########
    #   LocaleProvider
    @property
    def locale(self) -> Locale:
        """ The locale currently "provided" by this locale provider. """
        return Locale.default

    @locale.setter
    def locale(self, new_locale: Locale):
        """
            Sets the short user-readable name of the action.

            @param new_locale:
                The new locale to be "provided" by this locale 
                provider; cannot be None.
        """
        assert isinstance(new_locale, Locale)
        Locale.default = new_locale
