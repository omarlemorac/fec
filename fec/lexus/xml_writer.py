# -*- coding: utf-8 -*-
import os
import subprocess
import pdb
import config as C
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

    fname = "{cias}.{uoci}.{wtpdc}.{wserie}.{wnrodoc}.xml".format(**args)
    fu_path = os.path.join(unsigned_folder, fname)
    fs_path = os.path.join(signed_folder, fname)

    sql = statement.format(**args)
    m = M()

    with open(fu_path, 'w') as fu:
        fu.write( '\n'.join([r[0].replace("<ambiente>2</ambiente>","<ambiente>1</ambiente>" ) for r in m.read(sql).fetchall()]))
    os.chdir('/var/lib/eris/')
    subprocess.call(["java", "-jar", "eris.jar", "sign", fname])
    #subprocess.call(["java", "-jar", "eris.jar","sign",fname, "comprobante"])


    return fu_path

def write_invoice(company, args):
    if company == 'codepret':
        return write_invoice_codepret(args)
    else:
        return None

def write_outstanding_vouchers():
    m = M()
    rs = m.get_outstanding_vouchers()
    args =[
        {
        'cias':int(r[0]),
        'uoci':int(r[1]),
        'wtpdc':r[2],
        'wserie':r[3],
        'wnrodoc':int(r[4]),
        } for r in rs]
    for a in args:
       write_invoice('codepret', a)
