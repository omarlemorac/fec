# -*- coding: utf-8 -*-

import csv

def read_partner(fn):
    with open(fn, 'rb') as partner_file:
        p_reader = csv.reader(partner_file, delimiter=';', quotechar='"')
        for row in p_reader:
            yield row


if __name__ == '__main__':
    read_partner('/home/fec/clientes.csv')


