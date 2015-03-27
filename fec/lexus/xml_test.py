# -*- coding: utf-8 -*-

import xml_writer

args =[
       {
        'cias':1100,
        'uoci':2000,
        'wtpdc':'FC',
        'wserie':'001010',
        'wnrodoc':574,
        },
       {
        'cias':1100,
        'uoci':2000,
        'wtpdc':'FC',
        'wserie':'001010',
        'wnrodoc':575,
        },
       {
        'cias':1100,
        'uoci':2000,
        'wtpdc':'FC',
        'wserie':'001010',
        'wnrodoc':576,
        },
       {
        'cias':1100,
        'uoci':2000,
        'wtpdc':'FC',
        'wserie':'001010',
        'wnrodoc':577,
        },
       {
        'cias':1100,
        'uoci':2000,
        'wtpdc':'FC',
        'wserie':'001010',
        'wnrodoc':578,
        },
       {
        'cias':1100,
        'uoci':2000,
        'wtpdc':'FC',
        'wserie':'001010',
        'wnrodoc':579,
        },
       {
        'cias':1100,
        'uoci':2000,
        'wtpdc':'FC',
        'wserie':'001010',
        'wnrodoc':580,
        },
       {
        'cias':1100,
        'uoci':2000,
        'wtpdc':'FC',
        'wserie':'001010',
        'wnrodoc':581,
        },

        ]
for x in args:
    print xml_writer.write_invoice_codepret(x)

