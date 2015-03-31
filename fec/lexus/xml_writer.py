# -*- coding: utf-8 -*-
import os
import subprocess
import pdb
import config as C
from lexus_model import model as M
import suds
from lxml import etree
from repo_model import Model as R

def write_invoice_codepret( args):
    from lexus_model import model as M
    statement = """
    EXEC SRI$SIMP_FACXML_FEV110 @WCIAS='{cias}',@WUOCI='{uoci}',
    @WTPDC='{wtpdc}',@WSERIE='{wserie}',@WNRODOC='{wnrodoc}',@user = 'sa',
    @pwd = 'Codepret2010',@servidor = 'SERAPL\CODEPRET',
    @BddNombre='ISOFTEC_CDP',
    @RutaXml = 'C:\ISOFTEC\CELECTRONICOS\DOC_GENERADOS',@UserLogin = 'WILMERO'
    """

    unsigned_folder = C.unsigned_docs_folder
    signed_folder = C.signed_docs_folder

    fname = "{claveacceso}.xml".format(**args)
    fu_path = os.path.join(unsigned_folder, fname)
    fs_path = os.path.join(signed_folder, fname)

    sql = statement.format(**args)
    m = M()

    with open(fu_path, 'w') as fu:
        fu.write( '\n'.join([r[0] for r in m.read(sql).fetchall()]))
    os.chdir('/var/lib/eris/')
    subprocess.call(["java", "-jar", "eris.jar", "sign", fname])

    tree = etree.parse(fs_path)
    email_recipient = tree.xpath("//infoAdicional/campoAdicional[@nombre='Email']")[0].text

    repo = R()
    couchdb = repo.get_database(C.couchdb_config['doc_db'])
    for i in repo.read(C.couchdb_config['doc_db'], R.GET_ID % args['claveacceso']):
        doc = couchdb[i.id]
        with open(fs_path, 'rb') as fs:
            doc['comprobante'] = fs.read()
        doc['email_recipient'] =  email_recipient
        couchdb.save(doc)

    return fu_path
def write_invoice(company, args):
    if company == 'codepret':
        return write_invoice_codepret(args)
    else:
        return None

def write_outstanding_vouchers():
    m = M()
    rs = m.get_outstanding_vouchers()
#    Send to cache
    args = []
    repo = R()
    for r in rs:
        query = repo.BY_ACCESS_KEY % (r[5])
        if r[5] in [a.value for a in repo.read(C.couchdb_config['doc_db'],
            query)]:
            continue
        repo.save(C.couchdb_config['doc_db'], r[5], {
        'cias':int(r[0]),
        'uoci':int(r[1]),
        'wtpdc':r[2],
        'wserie':r[3],
        'wnrodoc':int(r[4]),
        'claveacceso':r[5],
        'estado':'GENERADO',
        'mail_sended':False,
        'mail_recipient':"",
        })


    for a in repo.read(C.couchdb_config['doc_db'], repo.NOT_AUTHORIZED):
       write_invoice('codepret', a.value)

def write_authorized_voucher_xml(ak, auth):
    """docstring for write_authorized_voucher_xml"""
    n = 1
    for a in auth["autorizacion"]:
        root = etree.Element("autorizacion")
        ad = suds.sudsobject.asdict(a)
        for k, v in ad.items():
            if v.__class__.__name__ == 'mensajes':
                continue
            """
            if v.__class__.__name__ == 'mensajes':
                mensajes = suds.sudsobject.asdict(v)
                for mk, mv in mensajes.items():
                    if mv.__class__.__name__ == 'list':
                        for ms in mv:
                            oms = suds.sudsobject.asdict(ms)
                            print oms
            """
            if v.__class__.__name__ == 'datetime':
                v = v.strftime("%d/%m/%Y %H:%M:%S.%f")
            if k == 'comprobante':
                v = etree.CDATA(v)
            el = etree.SubElement(root, k)
            el.text = v
        etree.ElementTree(root).write(os.path.join(C.authorized_docs_folder,
            '{}_{}.xml'.format(ak, n)), pretty_print=True)

def write_authorized_voucher(ak, sri_auth):
    """Writes the authorized voucher to file"""
    if not sri_auth:
        return
    for a in sri_auth["autorizacion"]:
        if not a:
            continue
        ad = suds.sudsobject.asdict(a)
        if ad["estado"] == "AUTORIZADO":
            write_authorized_voucher_xml(ak, sri_auth)
        else:
            print "Write Error Log"
            #print ad["mensajes"]
            #print ad["ambiente"]

#        print ad["comprobante"]
