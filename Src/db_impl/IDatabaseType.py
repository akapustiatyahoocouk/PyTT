class IDatabaseType(ABC):
    """ A "database type" corresponds to a technology used to
        keep the data persistent (database engine type, etc.)"""
    
    ##########
    #   object
    def __str__(self) -> str:
        return self.display_name

    ##########
    #   Properties (general)
    @abstractproperty
    def mnemonic(self) -> str:
        """ The mnemonic identifier of this database type. """
        raise NotImplementedError()

    @abstractproperty
    def display_name(self) -> str:
        """ The user-readable display name of this database type. """
        raise NotImplementedError()

    ##########
    #   Database address handling
    @abstractmethod
    def parse_database_address(self, externa_form: str) -> "IDatabaseAddress":
        """
            Parses an external (re-parsable) form of a database address
            of this type.
            
            @param externa_form:
                The external (re-parsable) form of a database address.
            @return:
                The parsed database address.
            @raise InvalidDatabaseAddressException:
                If the specified external form of a database address
                doesnot make sense for this database type.
        """
        raise NotImplementedError()

    @abstractproperty
    def default_database_address(self) -> "IDatabaseAddress":
        raise NotImplementedError()

