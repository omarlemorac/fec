# -*- coding: utf-8 -*-
import couchdb
import config as C
import suds
import pdb
import time
class Model():

    '''Model for couchdb'''
    ALL_DOCUMENTS = """
    function(doc){
        emit(null, doc.claveacceso)
        }
    """
    AUTHORIZED = """
    function(doc){
        if(doc.estado == 'AUTORIZADO' && !mail_sended)
            emit(null, {'cias':doc.cias, 'uoci':doc.uoci,
            'wnrodoc':doc.wnrodoc, 'wserie':doc.wserie,'wtpdc':doc.wtpdc,
            'claveacceso':doc.claveacceso,
            'numeroAutorizacion':doc.numeroAutorizacion,
            'fechaAutorizacion':doc.fechaAutorizacion}
            );
        }
    """
    NOT_AUTHORIZED = """
    function(doc){
        if(doc.estado != 'AUTORIZADO')
            emit(null, {'cias':doc.cias, 'uoci':doc.uoci,
            'wnrodoc':doc.wnrodoc, 'wserie':doc.wserie,'wtpdc':doc.wtpdc,
            'claveacceso':doc.claveacceso}
            );
        }
    """
    NOT_AUTHORIZED_CMP = """
    function(doc){
        if(doc.estado != 'AUTORIZADO')
            emit(null, {'cias':doc.cias, 'uoci':doc.uoci,
            'wnrodoc':doc.wnrodoc, 'wserie':doc.wserie,'wtpdc':doc.wtpdc,
            'claveacceso':doc.claveacceso, 'comprobante':doc.comprobante}
            );
        }
    """
    BY_ACCESS_KEY = """
    function(doc){
        if(doc.claveacceso == '%s')
            emit(null, doc.claveacceso);
        }
    """
    GET_ID = """
    function(doc){
        if(doc.claveacceso == '%s')
            emit(null, doc.id);
        }
    """
    SEND_BY_MAIL = """
    function(doc){
        if(!doc.mail_sended)
            emit(null, doc.id);
        }
    """
    WRITE_WEB_DB = """
    function(doc){
        if(!doc.web_db_written)
            emit(null, doc.id);
        }
    """
    def _get_server(self):
        """docstring for _get_server"""
        return couchdb.Server(C.couchdb_config["host"])

    def _get_or_create(self, name):
        """Get database if not exist create"""
        server =  self._get_server()
        try:
            return server[name]
        except:
            return server.create(name)

    def get_database(self, dbname):
        return self._get_or_create(dbname)

    def save(self, dbname, rid, doc):
        """docstring for save"""
        db = self._get_or_create(dbname)
        db.save(doc)

    def read(self,dbname, fun):
        """docstring for re"""
        db = self._get_or_create(dbname)
        return db.query(fun)

    def write_authorized_voucher_db(self, dbname, ak, auth):
        """docstring for write_authorized_voucher_xml"""
        ids_lst = self.read(dbname, self.GET_ID % ak)
        db = self.get_database(dbname)
        for a in auth["autorizacion"]:
            for _id in ids_lst:
                doc = db[_id.id]
                ad = suds.sudsobject.asdict(a)
                for k, v in ad.items():
                    if v.__class__.__name__ == 'mensajes':
                        mensajes = suds.sudsobject.asdict(v)
                        mens_lst = []
                        for mk, mv in mensajes.items():
                            if mv.__class__.__name__ == 'list':
                                for ms in mv:
                                    oms = suds.sudsobject.asdict(ms)
                                    mens_lst.append(oms)
                        v = mens_lst
                    if v.__class__.__name__ == 'datetime':
                        v = v.strftime("%d/%m/%Y %H:%M:%S.%f")
                    doc[k] = v
                db.save(doc)

    def write_mail_sended(self, dbname, ak):
        """Writes True in mail sended"""
        ids_lst = self.read(dbname, self.GET_ID % ak)
        db = self.get_database(dbname)
        for _id in ids_lst:
            doc = db[_id.id]
            doc['mail_sended'] = True
            db.save(doc)

    def write_authorized_voucher(self, db, ak, sri_auth):
        """Writes the authorized voucher to file"""
        if not sri_auth:
            return
        for a in sri_auth["autorizacion"]:
            if not a:
                continue
            self.write_authorized_voucher_db(db, ak, sri_auth)
