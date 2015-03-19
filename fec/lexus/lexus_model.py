# -*- coding: utf-8 -*-
import pyodbc

dsn = 'lexus_desarrollo'
user = 'sa'
password = 'sa'
database = 'ISOFTEC_CDP'

con_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, user, password, database)
cnxn = pyodbc.connect(con_string)

class model():
    def __init__(self):
        """Inital data"""
        self.cnxn = cnxn
        self.cr = cnxn.cursor()

    def read(self, sql):
        """Execute command in database"""
        return self.cr.execute(sql)
