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

def xml_2_byte(filename):
    import base64
    encoded_data = base64.b64encode(open(filename, 'rb').read())
    strg = ''
    for i in xrange((len(encoded_data)/40)+1):
        strg += encoded_data[i*40:(i+1)*40]

    return strg
def send_doc(docstyle, filename):
    logging.basicConfig(level=logging.INFO)

    fn = os.path.join(C.signed_docs_folder, filename)
    if not os.path.isfile(fn):
        raise FileNotFoundError(C.signed_docs_folder, filename)
    logging.info("Enviando: %s: %s" % (docstyle,filename))
    try:
        if docstyle == "comprobante":
            client_rec = Client(C.deliver_url)
            response_rec = client_rec.service.validarComprobante(xml_2_byte(fn))
        elif docstyle == "lote":
            client_rec = Client(C.deliver_batch_url)
            response_rec = client_rec.service.validarLoteMasivo(xml_2_byte(fn))
    except Exception,e:
        logging.exception(e)
        return False
    if hasattr(response_rec, "estado"):
        #Lee el archivo XML para sacar la informacion
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

def test_send():
    m = M()
    fns = [os.path.join(C.signed_docs_folder,\
            "{}.{}.{}.{}.{}.xml".format(int(r[0]),int(r[1]),r[2],r[3],int(r[4]))) \
            for r in m.get_outstanding_vouchers()]
    for fn in fns:
        if os.path.isfile(fn):
            send_doc("comprobante", fn)

if __name__ == '__main__':
    test_send()
