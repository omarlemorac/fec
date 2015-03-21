import pyodbc

dsn = 'lexus_desarrollo'
user = 'sa'
password = 'sa'
database = 'ISOFTEC_CDP'

con_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, user, password, database)
