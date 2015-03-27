#-*- coding: utf-8 -*-
'''
Created on 27/05/2014

@author: Administrador
'''
import pdb
from file_manager import send2sri, authorize_doc, send_doc,\
        batch_send, save_auth_file, load_auth_file
import logging as L
import config as C
from os import path as P
import argparse

action_help = """
Define the action to be performed.\n
Options: [send | auth | validation | xml | load]\n
send: Validate and authorization\n
auth: Authorization of document sended\n
validation: Validation of document sending only\n
xml: Retrieves xml from database\n
load: Load authorized doc to database\n
"""

parser = argparse.ArgumentParser(description=u"Eris: Electronic Invoicing SRI")
parser.add_argument('-a', '--action', help=action_help, required=True)
parser.add_argument('-k', '--accesskey', help="Access Key")
parser.add_argument('-f', '--filename', help="Name of file to process")
parser.add_argument('-m', '--mode', help="[comprobante | lote]", required=True)
parser.add_argument('-s', '--sign', action='store_true', help="Sign documents")
args = parser.parse_args()

#L.basicConfig(filename=P.join(C.authorized_docs_folder,"eris.log") , level = L.INFO)
logger = L.getLogger('eris_main')
logger.setLevel(L.DEBUG)
formatter = L.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = L.FileHandler(P.join(C.authorized_docs_folder,"eris.log"))
fh.setFormatter(formatter)
logger.addHandler(fh)
def runeris():
    opts = parser.parse_known_args()
    logger.info("Action: %s " % args.action)
    logger.info("Filename: %s " % args.filename)
    logger.info("AccessKey: %s " % args.accesskey)
    logger.info("Mode: %s " % args.mode)
    logger.info("Sign: %s " % args.sign)
    logger.info("Start processing ")
    if args.action == "send":
        if args.mode == "comprobante":
            send2sri(args.accesskey, args.mode, args.filename, args.sign)
        elif args.mode == "lote":
            batch_send(args.filename, args.sign)
    elif args.action == "autorizacion":
        authorize_doc(args.accesskey, args.mode)
    elif args.action == "validacion":
        try:
            send_doc(args.mode, args.filename)
        except Exception, e:
            logger.log(L.ERROR, e)
            exit()
    elif args.action == "xml":
        save_auth_file(args.accesskey)
    elif args.action == "load":
        try:
            load_auth_file(args.mode, args.filename)
        except Exception, e:
            logger.log(L.ERROR, e)
            exit()



if __name__ == '__main__':
    runeris()
    #from file_manager import save_auth_file
    #save_auth_file(args.accesskey)
