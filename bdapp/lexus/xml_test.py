# -*- coding: utf-8 -*-

import xml_writer

args = {
        'cias':1100,
        'uoci':2000,
        'wtpdc':'FC',
        'wserie':'001010',
        'wnrodoc':574,
        }
print xml_writer.write_invoice_codepret(args)

