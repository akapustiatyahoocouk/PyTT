from typing import TypeAlias

import db_impl.exceptions
import db_impl.IDatabaseType
import db_impl.IDatabaseAddress

import db_impl.DatabaseTypeRegistry

IDatabaseType: TypeAlias = db_impl.IDatabaseType.IDatabaseType
IDatabaseAddress: TypeAlias = db_impl.IDatabaseAddress.IDatabaseAddress

DatabaseTypeRegistry: TypeAlias = db_impl.DatabaseTypeRegistry.DatabaseTypeRegistry

DatabaseException: TypeAlias = db_impl.exceptions.DatabaseException
InvalidDatabaseAddressException: TypeAlias = db_impl.exceptions.InvalidDatabaseAddressException


