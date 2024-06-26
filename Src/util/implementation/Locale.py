""" Defines a Locale - a specification of a culture/language
    to which aspects of the system can be localized. """

#   Python standard library
from __future__ import annotations  #   MUST be 1st in a module!
from typing import final, Optional, Union, Callable
from inspect import signature

#   Internal dependencies on modules within the same component
from .Annotations import staticproperty
from .Metaclasses import ClassWithConstantsMeta
from .PropertyChangeEvent import PropertyChangeEvent
from .PropertyChangeEventListener import PropertyChangeEventListener
from .PropertyChangeEventHandler import PropertyChangeEventHandler

##########
#   Public entities
@final
class LocaleMeta(ClassWithConstantsMeta):

    @property
    def system(cls):
        if cls._Locale__system_locale is None:
            import locale
            dl = locale.getdefaultlocale()
            try:
                cls._Locale__system_locale = Locale.parse(dl[0])
            except ValueError:
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
        if value != cls._Locale__default_locale:
            from .PropertyChangeEvent import PropertyChangeEvent
            cls._Locale__default_locale = value
            evt = PropertyChangeEvent(cls, cls, Locale.DEFAULT_LOCALE_PROPERTY_NAME)
            cls.process_property_change_event(evt)

@final
class Locale(metaclass=LocaleMeta):
    """ A specification of a culture/language to which aspects
        of the system can be localized. """

    ##########
    #   Implementation
    __root_locale = None    #   TODO try to move these to the LocaleMeta
    __system_locale = None
    __default_locale = None

    __property_change_listeners = []    #   This stays here in Locale class

    ##########
    #   Constants
    @staticproperty
    def ROOT() -> Locale:
        """ The root (invariant) locale. """
        if Locale.__root_locale is None:
            Locale.__root_locale = Locale()
        return Locale.__root_locale

    ##########
    #   Constants (observable property names)
    DEFAULT_LOCALE_PROPERTY_NAME = "default"
    """ The name of the "default: Locale" static property of a Locale. """

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
        from ..resources.UtilResources import UtilResources
        if self.__language is None:
            return UtilResources.string("Locale.Invariant")
        elif self.__country is None:
            #   Language only
            try:
                language_string = UtilResources.string("Language." + self.__language)
            except:
                language_string = self.__language
            return language_string
        elif self.__variant is None:
            #   Language+country
            try:
                language_string = UtilResources.string("Language." + self.__language)
            except:
                language_string = self.__language
            try:
                country_string = UtilResources.string("Country." + self.__country)
            except:
                country_string = self.__country
            return language_string + " (" + country_string + ")"
        else:
            #   Language+country+variant
            try:
                language_string = UtilResources.string("Language." + self.__language)
            except:
                language_string = self.__language
            try:
                country_string = UtilResources.string("Country." + self.__country)
            except:
                country_string = self.__country
            try:
                variant_string = UtilResources.string("Variant." + self.__variant)
            except:
                variant_string = self.__variant
            return language_string + " (" + country_string + ") " + variant_string

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
        """ The 2-letter ISO-639 language code (lowercase) or 
            None if this Locale does not specify the language. """
        return self.__language

    @property
    def country(self) -> Optional[str]:
        """ The 2-letter ISO-3166 country code (uppercase) or 
            None if this Locale does not specify the country. """
        return self.__country

    @property
    def variant(self) -> Optional[str]:
        """ The locale variant string or None if this Locale 
            does not specify the locale variant. """
        return self.__variant

    @property
    def parent(self) -> Locale:
        """ The immediate parent locale of this Locale.
            The parent of a "root" locale it the "root" locale tself. """
        if self.__language is None:
            return Locale.ROOT
        elif self.__country is None:
            return Locale.ROOT
        elif self.__variant is None:
            return Locale(self.__language)
        else:
            return Locale(self.__language, self.__country)

    @staticmethod
    def parse(locale_string: str) -> Locale:
        """
            Attempts to parse a string representation of a locale
            (that uses the same format as repr(Locale).
        
            @param locale_string:
                The locale string to parse.
            @return:
                The parsed locale.
            @raise ValueError:
                If an error occurs.
        """
        try:
            import re
            mlc = re.search(r"^([a-zA-Z]{2})_([a-zA-Z]{2})", locale_string)
            ml = re.search(r"^([a-zA-Z]{2})", locale_string)
            if mlc:
                language = mlc[1]
                country = mlc[2]
                variant = None
            elif ml:
                language = ml[1]
                country = None
                variant = None
            else:
                language = None
                country = None
                variant = None
            return Locale(language, country, variant)
        except:
            raise ValueError(locale_string)

    ##########
    #   Operations (static property change handling)
    @staticmethod
    def add_property_change_listener(l: Union[PropertyChangeEventListener, PropertyChangeEventHandler]) -> None:
        """ Registers the specified listener or handler to be
            notified when a static property change event is
            processed.
            A given listener can be registered at most once;
            subsequent attempts to register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, PropertyChangeEventHandler))
        if l not in Locale.__property_change_listeners:
            Locale.__property_change_listeners.append(l)

    @staticmethod
    def remove_property_change_listener(l: Union[PropertyChangeEventListener, PropertyChangeEventHandler]) -> None:
        """ Un-registers the specified listener or handler to no
            longer be notified when a static property change
            event is processed.
            A given listener can be un-registered at most once;
            subsequent attempts to un-register the same listener
            again will have no effect. """
        assert ((isinstance(l, Callable) and len(signature(l).parameters) == 1) or
                isinstance(l, PropertyChangeEventHandler))
        if l in Locale.__property_change_listeners:
            Locale.__property_change_listeners.remove(l)

    @staticproperty
    def property_change_listeners() -> list[Union[PropertyChangeEventListener, PropertyChangeEventHandler]]:
        """ The list of all static property change listeners registered so far. """
        return Locale.__property_change_listeners.copy()

    @staticmethod
    def process_property_change_event(event : PropertyChangeEvent) -> bool:
        """
            Called to process an PropertyChangeEvent for a
            change made to a static property.

            @param event:
                The property change event to process.
        """
        assert isinstance(event, PropertyChangeEvent)
        for l in Locale.property_change_listeners:
            try:
                if isinstance(l, PropertyChangeEventHandler):
                    l.on_property_change(event)
                else:
                    l(event)
            except Exception as ex:
                pass    #   TODO log the exception
        return event.processed
