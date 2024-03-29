"""
    The workspace abstraction priovides the API to "workspaces" - 
    persistent storages of data that implement business rules.
    Workspaces provide a layer over the low-level "database" layer -
    while "databases" perform phycal storage of the data, "workspaces"
    implement business rules for the stored data.
"""

from workspace_impl.Credentials import *
from workspace_impl.CurrentCredentials import *

