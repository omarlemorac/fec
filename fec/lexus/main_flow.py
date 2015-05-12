# -*- coding: utf-8 -*-
import partner
import ftp2
import sale
from lexus_model import model as M
import xml_writer
import sri_ws
import mail_manager
import pdb

def main_flow():
    """Define the main flow of application"""
    ftp2.download() #Download FTP files
#    try:
#        partner.insert_partners()
#    except Exception , e:
#        print e
#    sale.write_sale()
#    xml_writer.write_outstanding_vouchers()
#    sri_ws.send_docs()
    mail_manager.send_emails()
#    m = M()
#    m.update_lexus_authno()
#    m.process_outstanding_vouchers()

if __name__ == '__main__':
    main_flow()
