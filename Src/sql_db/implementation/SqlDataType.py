""" SQL data types. """
#   Python standard library
from typing import final
from enum import Enum

##########
#   Public entities
@final
class SqlDataType(Enum):
    """ A SQL data type. """

    INTEGER = 1
    """ An INT(n) BINDING. """

    REAL = 2
    """ A FLOAT(n,d), DOUBLE(n,d) or DECIMAL(n,d) binding. """

    STRING = 3
    """ A CHAR(n), VARCHAR(n) or TEXT SQL binding."""

    BOOLEAN = 4
    """ A CHAR(1) that uses 'Y' for tyue and 'N' for false."""
    