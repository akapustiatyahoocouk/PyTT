import db.api as dbapi
import db.sqlite_impl.SqliteDatabaseType as sqlitedb

print("initialising db.sqlite_impl package")

dbapi.DatabaseTypeRegistry.register_database_type(sqlitedb.SqliteDatabaseType.instance())

