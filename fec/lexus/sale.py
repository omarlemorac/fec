# -*- coding: utf-8 -*-
from lexus_model import model
from read_csv import read_csv
import xml_writer
import pdb

def write_sale():
    """
    Write sale object from csv
    """
    sale_reader = read_csv('ventas')
    sale_writer = model()
    sale_writer.unlink_sale()

    for s in sale_reader:
        sql = """
        INSERT INTO SCO$TCBFC_SGMA
            (FCSG_TPDC, FCSG_SERIEFC, FCSG_NROFAC, FCSG_MTIN, FCSG_CODUNI,
             FCSG_CTDDOC, FCSG_PRCUNI, FCSG_MTOREN, FCSG_MTODTO1, FCSG_PSPDCTO,
             FCSG_MTOOBJR, FCSG_MTOIMP, FCSG_FECFACT, FCSG_NRORUC, FCSG_CODCLIE,
             FCSG_PSPNRO,FCSG_COPA, FCSG_UOCI, FCSG_CTRL)
        VALUES
            (?,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?,? ,? ,?,?,? );

        """
        sale_writer.write_sale(sql, s)
    sale_writer.validate_sales()
    sale_writer.read_validation_log()
def authorize_sale():
    """Authorize sale over SRI webservice"""
    sql = """
    select CBFC_CIAS, CBFC_UOCI, CBFC_TPDC, CBFC_SERIEDC, CBFC_NRODOC
    from SCO$TCBFC
    where CBFC_USECRE = 'SIGMA'
    and CBFC_AUTFACT = 'NO ENVIADO'
    """
    lm = model()
    for l in lm.read(sql):
        args = {
            'cias':int(l[0]),
            'uoci':int(l[1]),
            'wtpdc':l[2],
            'wserie':l[3],
            'wnrodoc':int(l[4]),
            }
        print l, args
        print xml_writer.write_invoice_codepret(args)

if __name__ == '__main__':
    #write_sale()
    authorize_sale()



