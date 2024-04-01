#   Python standard library
from typing import final, Optional

#   Internal dependencies on modules within the same component
from util.Annotations import staticproperty

##########
#   Public entities
class LocaleMeta(type):
    
    @property
    def system(cls):
        if cls._Locale__system_locale is None:
            try:
                import locale, re
                dl = locale.getdefaultlocale()
                mlc = re.search(r"^([a-zA-Z]{2})_([a-zA-Z]{2})", dl[0])
                ml = re.search(r"^([a-zA-Z]{2})", dl[0])
                if mlc:
                    language = mlc[1]
                    country = mlc[2]
                    variant = None
                elif ml:
                    language = mlc[1]
                    country = None
                    variant = None
                else:
                    language = None
                    country = None
                    variant = None
                cls._Locale__system_locale = Locale(language, country, variant)
            except:
                cls._Locale__system_locale = Locale.ROOT
        return cls._Locale__system_locale

    @property
    def default(cls):
        if cls._Locale__default_locale is None:
            cls._Locale__default_locale = cls.system
        return cls._Locale__default_locale
        
    @default.setter
    def default(cls, value):
        assert isinstance(value, Locale)
        cls._Locale__default_locale = value

@final
class Locale(metaclass=LocaleMeta):

    __root_locale = None
    __system_locale = None
    __default_locale = None

    ##########
    #   Constants
    @staticproperty
    def ROOT() -> "Locale":
        """ The "root: (invariant) locale. """
        if Locale.__root_locale is None:
            Locale.__root_locale = Locale()
        return Locale.__root_locale

    ##########
    #   Construction
    def __init__(self,
                 language: Optional[str] = None, 
                 country: Optional[str] = None,
                 variant: Optional[str] = None):
        """
            Constructs the locale.
        
            @param language:
                The 2-letter ISO-639 language code (optional, default None).
            @param country:
                The 2-letter ISO-3166 country code (optional, default None).
            @param variant:
                The locale variant (optional, default None).
        """    
        assert (language is None) or isinstance(language, str)
        assert (country is None) or isinstance(country, str)
        assert (variant is None) or isinstance(variant, str)
        
        self.__language = None if (language is None or len(language.strip()) != 2) else language.strip().lower()
        self.__country = None if (country is None or len(country.strip()) != 2) else country.strip().upper()
        self.__variant = None if (variant is None or len(variant.strip()) == 0) else variant.strip().lower()

    ##########
    #   object
    def __hash__(self) -> int:
        return hash(repr(self))
    
    def __str__(self) -> str:
        if self.__language is None:
            return "Invariant"
        return self.__repr__()  #   TODO for now...

    def __repr__(self) -> str:
        if self.__language is None:
            return ""
        elif self.__country is None:
            return self.__language
        elif self.__variant is None:
            return self.__language + "_" + self.__country
        else:
            return self.__language + "_" + self.__country + "_" + self.__variant
        
    def __eq__(self, op2: "Locale") -> bool:
        if not isinstance(op2, Locale):
            return False
        return (self.__language == op2.__language and
                self.__country == op2.__country and
                self.__variant == op2.__variant)
    
    def __ne__(self, op2: "Locale") -> bool:
        if not isinstance(op2, Locale):
            return True
        return (self.__language != op2.__language or
                self.__country != op2.__country or
                self.__variant != op2.__variant)
    
    ##########
    #   Properties
    @property
    def language(self) -> Optional[str]:
        return self.__language

    @property
    def country(self) -> Optional[str]:
        return self.__country

    @property
    def variant(self) -> Optional[str]:
        return self.__variant

    @property    
    def parent(self) -> "Locale":
        """ The immediate parent locale of this Locale.
            The parent of a "root" locale it the "root" locale tself. """
        if self.__language is None:
            return self
        elif self.__country is None:
            return Locale.ROOT
        elif self.__variant is None:
            return Locale(self.__language)
        else:
            return Locale(self.__language, self.__country)
