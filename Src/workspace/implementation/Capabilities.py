#   Python standard library
#   Python standard library
from typing import TypeAlias

#   Dependencies on other PyTT components
from db.interface.api import Capability as DbCapability, Capabilities as DbCapabilities

##########
#   Public entities
Capability: TypeAlias = DbCapability
Capabilities: TypeAlias = DbCapabilities
