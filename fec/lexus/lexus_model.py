# -*- coding: utf-8 -*-
import pyodbc
from datetime import datetime as DT
import suds

dsn = 'lexus_desarrollo'
user = 'sa'
password = 'sa'
database = 'ISOFTEC_CDP'

con_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, user, password, database)
cnxn = pyodbc.connect(con_string)


class model():
    def __init__(self):
        """Inital data"""
        self.cnxn = cnxn
        self.cr = cnxn.cursor()

    def read(self, sql):
        """Execute command in database"""
        print sql
        cr = self.cnxn.cursor()
        return cr.execute(sql)

    def write_sale(self, sql, params):
        """write sql in database"""
        idate = DT.strptime(params[12], "%d/%m/%Y")
        self.cr.execute(sql,params[0], params[1],params[2],params[3],params[4],params[5],
                params[6],params[7],params[8],params[9],params[10],
                params[11],idate,params[13],params[14],params[15],
                params[16],)
        cnxn.commit()

    def unlink_sale(self):
        """unlink sale object"""
        sql = "delete from SCO$TCBFC_SGMA"
        self.cr.execute(sql)
        cnxn.commit()

    def get_outstanding_vouchers(self):
        sql = """
        SELECT rcbfc_cias, rcbfc_uoci, rcbfc_tpdc,
        rcbfc_seriedc,rcbfc_nrodoc,rcbfc_clveaccs
        FROM sco$tcbfc_sgmarl
        WHERE  RCBFC_STATUS  = 'N'
        AND    LEN(LTRIM(RTRIM(RCBFC_AUTFACT))) < 20
        AND    LEN(LTRIM(RTRIM(RCBFC_FECAUT))) < 18
        """
        cr = self.cnxn.cursor()
        return cr.execute(sql)

    def get_outstanding_ak(self):
        sql = """
        SELECT rcbfc_cias, rcbfc_uoci, rcbfc_tpdc, rcbfc_seriedc,rcbfc_nrodoc
        FROM sco$tcbfc_sgmarl
        WHERE len( rcbfc_autfact ) < 10
        """
        cr = self.cnxn.cursor()
        return cr.execute(sql)
    def write_authorization(self, ak, au, ad):
        """
        @ak: Access Key
        @au: Authorization number
        @ad: Authorization date
        """
        sql="""
        UPDATE sco$tcbfc_sgmarl SET rcbfc_autfact = ?,
        rcbfc_fecaut = ?
        WHERE  rcbfc_clveaccs = ?
        """
        cr = self.cnxn.cursor()
        cr.execute(sql, (au, ad, ak))
        cr.commit()
        cr.close()

    def proxy_authorization(self, ak, auth):
        if not auth:
            return
        for a in auth['autorizacion']:
            ad = suds.sudsobject.asdict(a)
            if 'numeroAutorizacion' in [k for k in ad.keys()]:
                self.write_authorization(ak, a['numeroAutorizacion'], a['fechaAutorizacion'])


