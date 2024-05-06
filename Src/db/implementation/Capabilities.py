#   Python standard library
from typing import final
from enum import Enum

#   Dependencies on other PyTT components
from util.interface.api import *

#   Internal dependencies on modules within the same component
from ..resources.DbResources import DbResources

##########
#   Public entities
@final
class Capability(Enum):
    """ Capabilities that can be assigned to Accounts. """

    ##########
    #   Constants
    ADMINISTRATOR = 0x0001
    """ Permits bearer to do anything within the workspace
        except violating its integrity (e.g. deleting or disabling
        the last Account that has ADMINISTRATOR capability, etc. """

    MANAGE_USERS = 0x0002
    """ Permits bearers to create, manage and delete Users
        and Accounts. """

    MANAGE_STOCK_ITEMS = 0x0004
    """ Permits bearer to create, manage and delete stock items,
        such as ActivityTypes. """

    MANAGE_BENEFICIARIES = 0x0008
    """ Permits bearer to create, manage and delete Beneficiaries. """

    MANAGE_WORKLOADS = 0x0010
    """ Permits bearer to create, manage and delete Workloads. """

    MANAGE_PUBLIC_ACTIVITIES = 0x0020
    """ Permits bearer to manage public activities within a workspace. """

    MANAGE_PUBLIC_TASKS = 0x0040
    """ Permits bearer to manage public tasks within a workspace. """

    MANAGE_PRIVATE_ACTIVITIES = 0x0080
    """ Permits bearer to manage private activities of any User
        within a workspace (Users can always manage their own private
        activities without a need for a special Capability). """

    MANAGE_PRIVATE_TASKS = 0x0100
    """ Permits bearer to manage private tasks of any User
        within a workspace (Users can always manage their own private
        tasks without a need for a special Capability). """

    LOG_WORK = 0x0200
    """ Permits bearer to log Work performed against an Activity. """

    LOG_EVENTS = 0x0400
    """ Permits bearer to log Events. """

    GENERATE_REPORTS = 0x0800
    """ Permits bearer to henerate reports. """

    BACKUP_AND_RESTORE = 0x1000
    """ Permits bearer to perform backup and restore tasks. """

    ##########
    #   object
    def __str__(self) -> str:
        return DbResources.string("Capability." + self.name)
        
@final
class Capabilities(ClassWithConstants):
    """ A set of capabilities. """

    ##########
    #   Constants (individual capabilities)
    __administrator_impl = None
    @staticproperty
    def ADMINISTRATOR() -> "Capabilities":
        """ The set containing a single ADMINISTRATOR capability. """
        if Capabilities.__administrator_impl is None:
            Capabilities.__administrator_impl = Capabilities(Capability.ADMINISTRATOR.value)
        return Capabilities.__administrator_impl

    __manage_users_impl = None
    @staticproperty
    def MANAGE_USERS() -> "Capabilities":
        """ The set containing a single MANAGE_USERS capability. """
        if Capabilities.__manage_users_impl is None:
            Capabilities.__manage_users_impl = Capabilities(Capability.MANAGE_USERS.value)
        return Capabilities.__manage_users_impl

    __manage_stock_items_impl = None
    @staticproperty
    def MANAGE_STOCK_ITEMS() -> "Capabilities":
        """ The set containing a single MANAGE_STOCK_ITEMS capability. """
        if Capabilities.__manage_stock_items_impl is None:
            Capabilities.__manage_stock_items_impl = Capabilities(Capability.MANAGE_STOCK_ITEMS.value)
        return Capabilities.__manage_stock_items_impl

    __manage_beneficiaries_impl = None
    @staticproperty
    def MANAGE_BENEFICIARIES() -> "Capabilities":
        """ The set containing a single MANAGE_BENEFICIARIES capability. """
        if Capabilities.__manage_beneficiaries_impl is None:
            Capabilities.__manage_beneficiaries_impl = Capabilities(Capability.MANAGE_BENEFICIARIES.value)
        return Capabilities.__manage_beneficiaries_impl

    __manage_workloads_impl = None
    @staticproperty
    def MANAGE_WORKLOADS() -> "Capabilities":
        """ The set containing a single MANAGE_WORKLOADS capability. """
        if Capabilities.__manage_workloads_impl is None:
            Capabilities.__manage_workloads_impl = Capabilities(Capability.MANAGE_WORKLOADS.value)
        return Capabilities.__manage_workloads_impl

    __manage_public_activities_impl = None
    @staticproperty
    def MANAGE_PUBLIC_ACTIVITIES() -> "Capabilities":
        """ The set containing a single MANAGE_PUBLIC_ACTIVITIES capability. """
        if Capabilities.__manage_public_activities_impl is None:
            Capabilities.__manage_public_activities_impl = Capabilities(Capability.MANAGE_PUBLIC_ACTIVITIES.value)
        return Capabilities.__manage_public_activities_impl

    __manage_public_tasks_impl = None
    @staticproperty
    def MANAGE_PUBLIC_TASKS() -> "Capabilities":
        """ The set containing a single MANAGE_PUBLIC_TASKS capability. """
        if Capabilities.__manage_public_tasks_impl is None:
            Capabilities.__manage_public_tasks_impl = Capabilities(Capability.MANAGE_PUBLIC_TASKS.value)
        return Capabilities.__manage_public_tasks_impl

    __manage_private_activities_impl = None
    @staticproperty
    def MANAGE_PRIVATE_ACTIVITIES() -> "Capabilities":
        """ The set containing a single MANAGE_PRIVATE_ACTIVITIES capability. """
        if Capabilities.__manage_private_activities_impl is None:
            Capabilities.__manage_private_activities_impl = Capabilities(Capability.MANAGE_PRIVATE_ACTIVITIES.value)
        return Capabilities.__manage_private_activities_impl

    __manage_private_tasks_impl = None
    @staticproperty
    def MANAGE_PRIVATE_TASKS() -> "Capabilities":
        """ The set containing a single MANAGE_PRIVATE_TASKS capability. """
        if Capabilities.__manage_private_tasks_impl is None:
            Capabilities.__manage_private_tasks_impl = Capabilities(Capability.MANAGE_PRIVATE_TASKS.value)
        return Capabilities.__manage_private_tasks_impl

    __log_work_impl = None
    @staticproperty
    def LOG_WORK() -> "Capabilities":
        """ The set containing a single LOG_WORK capability. """
        if Capabilities.__log_work_impl is None:
            Capabilities.__log_work_impl = Capabilities(Capability.LOG_WORK.value)
        return Capabilities.__log_work_impl

    __log_events_impl = None
    @staticproperty
    def LOG_EVENTS() -> "Capabilities":
        """ The set containing a single LOG_EVENTS capability. """
        if Capabilities.__log_events_impl is None:
            Capabilities.__log_events_impl = Capabilities(Capability.LOG_EVENTS.value)
        return Capabilities.__log_events_impl

    __generate_reports_impl = None
    @staticproperty
    def GENERATE_REPORTS() -> "Capabilities":
        """ The set containing a single GENERATE_REPORTS capability. """
        if Capabilities.__generate_reports_impl is None:
            Capabilities.__generate_reports_impl = Capabilities(Capability.GENERATE_REPORTS.value)
        return Capabilities.__generate_reports_impl

    __backup_and_restore_impl = None
    @staticproperty
    def BACKUP_AND_RESTORE() -> "Capabilities":
        """ The set containing a single BACKUP_AND_RESTORE capability. """
        if Capabilities.__backup_and_restore_impl is None:
            Capabilities.__backup_and_restore_impl = Capabilities(Capability.BACKUP_AND_RESTORE.value)
        return Capabilities.__backup_and_restore_impl

    ##########
    #   Constants (capability sets)
    __none_impl = None
    @staticproperty
    def NONE() -> "Capabilities":
        """ The empty set containing none of the capabilities. """
        if Capabilities.__none_impl is None:
            Capabilities.__none_impl = Capabilities(0x0000)
        return Capabilities.__none_impl

    __all_impl = None
    @staticproperty
    def ALL() -> "Capabilities":
        """ The set of all permitted capabilities. """
        if Capabilities.__all_impl is None:
            Capabilities.__all_impl = Capabilities(0x1FFF)
        return Capabilities.__all_impl

    ##########
    #   Construction
    def __init__(self, bit_mask: int) -> None:
        assert isinstance(bit_mask, int)
        self.__bit_mask = (bit_mask & 0x1FFF)

    ##########
    #   object
    def __or__(self, op2) -> "Capabilities":
        if isinstance(op2, Capabilities):
            return Capabilities(self.__bit_mask | op2.__bit_mask)
        else:
            return Capabilities(self.__bit_mask  | op2.value)

    ##########
    #   Operations
    def contains_all(self, op2) -> bool:    #   TODO use args, like contains_any
        """
            Checks whether this capability set contains all of the
            specified capabilities or a single specified capability.

            @param op2:
                The Capabilities or a Capability to check for.
            @return:
                True if this capability set contains all of the
                specified capabilities or a single specified
                capability, else False.
        """
        assert isinstance(op2, Capabilities) or isinstance(op2, Capability)

        if isinstance(op2, Capabilities):
            #   Check for containing a capabilities set
            return (self.__bit_mask & op2.__bit_mask) == op2.__bit_mask
        else:
            #   Check for containing a single capability
            return (self.__bit_mask & op2.value) != 0

    def contains_any(self, *args) -> bool:
        """
            Checks whether this capability set contains any of the
            specified capabilities or a single specified capability.

            @param args:
                The list of Capabilities or a Capability to check for.
            @return:
                True if this capability set contains any of the
                specified capabilities or a single specified
                capability, else False.
        """
        for arg in args:
            assert isinstance(arg, Capabilities) or isinstance(arg, Capability)
            if isinstance(arg, Capabilities):
                #   Check for containing a capabilities set
                if (self.__bit_mask & arg.__bit_mask) != 0:
                    return True
            else:
                #   Check for containing a single capability
                if (self.__bit_mask & arg.value) != 0:
                    return True
        return False