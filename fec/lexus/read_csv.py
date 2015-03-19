# -*- coding: utf-8 -*-

import csv
fn_clientes = '/home/fec/clientes.csv'
def read_partner():
    with open(fn_clientes, 'rb') as partner_file:
        p_reader = csv.reader(partner_file, delimiter=',', quotechar='"')
        next(p_reader)
        for row in p_reader:
            yield row

"""
if __name__ == '__main__':
    read_partner('/home/fec/clientes.csv')
"""

