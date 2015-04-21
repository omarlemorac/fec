#-*- coding: utf-8 -*-
'''
Created on May 26, 2014

@author: accioma
'''
import suds, pdb
import logging
import config as C
import os
from suds.client import Client
from suds import sudsobject
from lexus_model import model as M
from repo_model import Model
import xml_writer
import pdb

logging.basicConfig(
         filename="/home/fec/eris.log"
        ,level = logging.ERROR)

class ErisError(Exception):
    def __init__(self, errornumber, message):
        self.errornumber = errornumber
        self.message = message

    def __str__(self):
        return "Error %s. %s" %(self.errornumber, self.message)

def xml_2_byte(xml):
    import base64
    encoded_data = base64.b64encode(xml)
    strg = ''
    for i in xrange((len(encoded_data)/40)+1):
        strg += encoded_data[i*40:(i+1)*40]

    return strg
def send_doc(docstyle, xml):
    logging.basicConfig(level=logging.INFO)
    try:
        if docstyle == "comprobante":
            client_rec = Client(C.deliver_url)
            response_rec = client_rec.service.validarComprobante(xml_2_byte(xml))
        elif docstyle == "lote":
            client_rec = Client(C.deliver_batch_url)
            response_rec = client_rec.service.validarLoteMasivo(xml_2_byte(xml))
    except Exception,e:
        logging.exception(e)
        return False
    if hasattr(response_rec, "estado"):
        #Lee el archivo XML para sacar la informacion
        # response_rec.comprobantes
        return response_rec.estado
    return "ERROR"
        #res = sudsobject.asdict(response_rec)
        #print res['estado']
        #for k,v in res.items():
        #    print k
        #    if k == 'comprobantes':
        #        c = sudsobject.asdict(v)
        #        print c
        #print str(response_rec.estado)

def authorize_doc(claveacceso, docstyle):
    from suds.client import Client
    import logging
    logging.getLogger('suds.transport.http').setLevel(logging.INFO)
    logging.info("Autorizando: %s" % (claveacceso))

    try:
        headers = {'Content-Type': 'application/soap+xml; charset="UTF-8"'}
        client_aut = Client(C.authorization_url, headers=headers)
        if docstyle == "comprobante":
            response_aut = client_aut.service.autorizacionComprobante(claveacceso)
        elif docstyle == "lote":
            response_aut = client_aut.service.autorizacionComprobanteLoteMasivo(claveacceso)

        res = sudsobject.asdict(response_aut)
        ak = ""

        if "claveAccesoConsultada" in res.keys():
            ak = res["claveAccesoConsultada"]
        if "autorizaciones" in res.keys():
            aut = sudsobject.asdict(res["autorizaciones"])
            if not aut:
                raise ErisError("102", "La clave de acceso %s no tiene autorizaciones" % claveacceso)
            return (ak, aut)

        for authk, authv in res.items():
            logging.info("k{}, v {}".format(authk, authv))
    except Exception, e:
        logging.exception(e)
    return (ak, None)
def send_docs():
    m = M()
    mod = Model()
    db = mod.get_database(C.couchdb_config['doc_db'])

    for d in mod.read(C.couchdb_config['doc_db'],mod.NOT_AUTHORIZED_CMP):
        send_doc('comprobante', d.value['comprobante'])
        try:
            logging.info("Authorizing {}".format(d.value['claveacceso']))
            auth = authorize_doc(d.value['claveacceso'], 'comprobante')
            mod.write_authorized_voucher(*(C.couchdb_config['doc_db'], ) + auth )
        except KeyError as ke:
            print [a for a in d.value.keys()]
        except Exception as ex:
            print ex
        xml_writer.write_authorized_voucher(*auth)
if __name__ == '__main__':
    test_send()
