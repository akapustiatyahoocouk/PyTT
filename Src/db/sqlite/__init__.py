import db.api as dbapi
import db.sqlite.SqliteDatabaseType as sqlitedb

print('initialising db.sqlite package')

dbapi.DatabaseTypeRegistry.register_database_type(sqlitedb.SqliteDatabaseType.instance())
