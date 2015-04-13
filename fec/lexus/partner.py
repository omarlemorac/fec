# -*- coding: utf-8 -*-
import conn
import pyodbc
import read_csv

cnxn = pyodbc.connect(conn.con_string)

def insert_partner_row(cr,row):

    print row
    sql = """
    INSERT INTO SCO$TCLIE_SGMA
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
    """
    cr.execute(sql, row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]
            ,row[8],row[9],row[10],row[11] )

def insert_partners():
    cursor = cnxn.cursor()
    sql = "delete from SCO$TCLIE_SGMA"
    cursor.execute(sql)
    for p in read_csv.read_partner():
        insert_partner_row(cursor, p)

    cnxn.commit()

if __name__ == '__main__':
    insert_partners()

