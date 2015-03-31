# -*- coding: utf-8 -*-
import partner
import ftp2
import sale
from lexus_model import model as M
import xml_writer
import sri_ws

def main_flow():
    """Define the main flow of application"""
    #ftp2.download() #Download FTP files
    #partner.insert_partners() #Insert partners
    #sale.write_sale() #Insert sales
    #xml_writer.write_outstanding_vouchers()
    sri_ws.send_docs()

if __name__ == '__main__':
    main_flow()
