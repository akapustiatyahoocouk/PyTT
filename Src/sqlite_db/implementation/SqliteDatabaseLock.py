#   Python standard library
from typing import final
import os
import time
from threading import Thread

#   Dependencies on other PyTT components
from db.interface.api import *
from util.interface.api import *

##########
#   Public entities
@final
class SqliteDatabaseLock(ClassWithConstants):

    ##########
    #   Constants
    LOCK_REFRESH_INTERVAL_SEC = 5
    LOCK_TIMEOUT_SEC = 15

    ##########
    #   Construction
    def __init__(self, path: str):
        """
            Creates a database lock directory.

            @param path:
                The full path to the lock directory.
            @raise DatabaseError:
                If the database lock could not be created).
        """
        assert isinstance(path, str)

        self.__path = path
        try:
            #   Can we create a lock directory (clean case)?
            os.mkdir(path)
            #   Success! Start the refresh thread
        except Exception as ex:
            #   OOPS! Something is already there
            if not os.path.isdir(path):
                raise DatabaseObjectAlreadyExistsError("database lock", "path", path)
            #   When was it last modified ?
            mtime = os.path.getmtime(path)
            now = time.time()
            if now < mtime + SqliteDatabaseLock.LOCK_TIMEOUT_SEC:
                raise DatabaseIoError("Database " + path + " already in use")
            #   Take over the lock & start refresh thread
        self.__refresh_thread_stop_requested = False
        self.__refresh_thread = Thread(target=self.__run, args=[])
        self.__refresh_thread.daemon = True
        self.__refresh_thread.start()

    ##########
    #   Operations
    def close(self) -> None:
        self.__refresh_thread_stop_requested = True
        self.__refresh_thread = None
        try:
            os.rmdir(self.__path)
        except:
            pass    # TODO log

    ##########
    #   Threads
    def __run(self) -> None:
        while not self.__refresh_thread_stop_requested:
            now = time.time()
            try:
                os.utime(self.__path, (now, now))
            except:
                break
            time.sleep(SqliteDatabaseLock.LOCK_REFRESH_INTERVAL_SEC)
        pass
