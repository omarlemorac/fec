# -*- coding: utf-8 -*-

import csv

filenames = {
        'clientes' : '/home/fec/clientes.csv',
        'ventas' : '/home/fec/ventas.csv',
        }
def read_partner():
    with open(fn_clientes, 'rb') as partner_file:
        p_reader = csv.reader(partner_file, delimiter=',', quotechar='"')
        next(p_reader)
        for row in p_reader:
            yield row

def read_csv(value):
    """Reads the sale file and return contents """
    with open(filenames[value], 'rb') as csv_file:
        c_reader = csv.reader(csv_file, delimiter=';', quotechar='"')
        next(c_reader)
        for row in c_reader:
            yield row
"""
if __name__ == '__main__':
    read_partner('/home/fec/clientes.csv')
"""

