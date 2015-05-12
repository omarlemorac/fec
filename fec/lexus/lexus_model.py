# -*- coding: utf-8 -*-
import pyodbc
from datetime import datetime as DT
import config as C
import suds
import pdb
import repo_model

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
        cr = self.cnxn.cursor()
        return cr.execute(sql)

    def to_number(self, string):
        """docstring for to_number"""
        try:
            return float(string)
        except ValueError:
            return string

    def write_sale(self, sql, params):
        """write sql in database"""
        idate = DT.strptime(params[12], "%d/%m/%Y")
#        params1 = [self.to_number(v) for v in params ]
        self.cr.execute(sql,params[0], params[1],params[2]
                ,params[3],params[4],params[5],
                params[6],params[7],params[8],
                params[9],params[10],
                params[11],idate,params[13],params[14],params[15],
                params[16],params[17],params[18])
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

    def read_validation_log(self):
        """read validation log table"""
        sql = """
        SELECT tsgflg_text
        FROM sco_ttsgma_fact_log
        """
        cr = self.cnxn.cursor()
        exists_log = False
        with open('/home/fec/validation.log', 'w') as log:
            for t in cr.execute(sql):
                exists_log = True
                log.write("{}\n".format(t[0]))
        if exists_log:
            import mail_manager
            mail_manager.send_validation_log()


    def validate_sales(self):
        """Run validate sales on Lexus Database"""
        sql="""
        EXEC  SGM_SFE01_VLDACTRL
        """
        cr = self.cnxn.cursor()
        try:
            cr.execute(sql)
            cr.commit()
        except Exception, ex:
            print ex
        cr.close()
    def proxy_authorization(self, ak, auth):
        if not auth:
            return
        for a in auth['autorizacion']:
            ad = suds.sudsobject.asdict(a)
            if 'numeroAutorizacion' in [k for k in ad.keys()]:
                self.write_authorization(ak, a['numeroAutorizacion'], a['fechaAutorizacion'])

    def process_outstanding_vouchers(self):
        """Process outstandig vouchers from REL table"""
        sql = "EXEC SGM_SFE09_ACTAUTO "
        cr = self.cnxn.cursor()
        try:
            cr.execute(sql)
            cr.commit()
        except Exception, ex:
            print ex
        cr.close()

    def update_lexus_authno(self):
        """Update Lexus authorization number"""
        rm = repo_model.Model()
        couchdb = rm.get_database(C.couchdb_config['doc_db'])
        for i in rm.read(C.couchdb_config['doc_db'], rm.WRITE_LEXUS_DB):
            self.write_authorization(i.value['claveacceso'],
                                     i.value['numeroAutorizacion'],
                                     i.value['fechaAutorizacion'])

            rm.write_lexus_update(C.couchdb_config['doc_db'],i.value['claveacceso'])
