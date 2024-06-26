#   Python standard library
from typing import TypeAlias

#   Dependencies on other PyTT components
import db.interface.api as dbapi

##########
#   Public entities
UserValidator: TypeAlias = dbapi.UserValidator
AccountValidator: TypeAlias = dbapi.AccountValidator
ActivityTypeValidator: TypeAlias = dbapi.ActivityTypeValidator
ActivityValidator: TypeAlias = dbapi.ActivityValidator
Validator: TypeAlias = dbapi.Validator
