#-*- coding: utf-8 -*-
'''
Created on May 26, 2014

@author: marcelo
'''
import pdb
import config as C
import os.path as P
import mysql.connector as CN
import time
import os
import logging
import traceback
logging.basicConfig(
         filename=P.join(C.authorized_docs_folder,"eris.log")
        ,level = logging.DEBUG)
class FileNotFoundError(Exception):
    def __init__(self, path, filename):
        self.filename = filename
        self.path = path
    def __str__(self):
        return "El archivo %s en %s no ha sido encontrado" % (self.filename, self.path)

class ErisError(Exception):
    def __init__(self, errornumber, message):
        self.errornumber = errornumber
        self.message = message

    def __str__(self):
        return "Error %s. %s" %(self.errornumber, self.message)

class document():
    def __init__(self, comprobante):
        self.comprobante = comprobante

doc_type_id = ""

doc_data = {'ambiente':'', 'tipoEmision':'', 'tipoIdentificacionComprador':'', 'razonSocialComprador':'',
            'identificacionComprador':'','email':'','fechaEmision':'', 'estado':'', 'claveAcceso':'',
            'tipoDocumento':'', 'codDoc':'', 'estab':'', 'ptoEmi':'', 'secuencial':''
            }
ret_data = {
        'ambiente':'',
        'tipoEmision':'',
        'tipoIdentificacionSujetoRetenido':'',
        'razonSocialSujetoRetenido':'',
        'identificacionSujetoRetenido':'',
        'email':'','fechaEmision':'',
        'claveAcceso':'',
        'codDoc':'',
        'estab':'',
        'ptoEmi':'',
        'secuencial':''
            }


def get_userid_from_vatno(vatno):
    import mysql.connector as CN
    query = "SELECT eris_user_id FROM eris_user WHERE eris_vatno = '%s'" % vatno

    cnx = CN.connect(**C.mysql_config)
    cursor = cnx.cursor()
    cursor.execute(query)
    for user_id in cursor:
        return user_id[0]
    raise Exception("No se encuentra registrado el cliente %s" % vatno)


def add_user():
    import mysql.connector as CN
    user_data = {
        'identificacion' : '',
        'tipoIdentificacion' : '',
        'razonSocial' : '',
        'email' : '',
    }
    if doc_type_id in ( 'factura', 'notaCredito' ):
        user_data['identificacion'] = doc_data['identificacionComprador']
        user_data['tipoIdentificacion'] = doc_data['tipoIdentificacionComprador']
        user_data['razonSocial'] = doc_data['razonSocialComprador']
        user_data['email'] = doc_data['email']
    elif doc_type_id == 'comprobanteRetencion':
        user_data['identificacion']=\
        ret_data['identificacionSujetoRetenido']
        user_data['tipoIdentificacion'] =\
        ret_data['tipoIdentificacionSujetoRetenido']
        user_data['razonSocial'] = ret_data['razonSocialSujetoRetenido']
        user_data['email'] = ret_data['email']
    else:
        raise ErisError(300, 'Tipo de documento %s no soportado' % doc_type_id)
    try:
        cnx = CN.connect(**C.mysql_config)
        query = "SELECT count(*) FROM eris_user WHERE eris_vatno = '%s'" % user_data['identificacion']
        cursor = cnx.cursor()
        cursor.execute(query)
        if int(cursor.fetchone()[0]) == 0:
            query = ("""INSERT INTO `eris_user`(`eris_vatno`, `eris_vatno_type`
                                             , `eris_companyname`, `eris_tradename`, `eris_username`
                                             , `eris_password`, `eris_email`)
                                       VALUES (%(identificacion)s,%(tipoIdentificacion)s
                                              ,%(razonSocial)s,%(razonSocial)s,
                                               %(identificacion)s
                                              ,%(identificacion)s,%(email)s)""")
            cur_adduser = cnx.cursor()
            cur_adduser.execute(query,user_data)
            cnx.commit()
            cur_adduser.close()
        cursor.close()
        cnx.close()
    except Exception as err:
        logging.error("Error al agregar usuario %s" % err)

def get_doc_id_by_accesskey(cnx, ak):
    """
    Determina si la clave de acceso esta guardada en la tabla
    @param ak: Clave de acceso
    """

    query = "SELECT eris_document_id FROM eris_document WHERE eris_accesskey = '%s'" % ak

    cursor = cnx.cursor()
    cursor.execute(query)
    for user_id in cursor:
        return user_id[0]
    raise Exception("No se encuentra registrado el documento %s" % ak)



def save_doc(cnx, filename):
    """
    Inserta en la tabla el documento validado
    """
    fn = os.path.split(filename)[-1]
    query_insert = """
        INSERT INTO `eris_document`( `eris_user_id`, `eris_accesskey`,
                                     `eris_documentxml`, `eris_docyear`,
                                     `eris_docymonth`, `eris_docday`, `eris_environment`,
                                     `eris_receptionstate`,`eris_document_estab`,
                                     `eris_document_ptoemi`,`eris_document_secuencial`,
                                     `eris_coddoc_id`, `eris_doc_filename`)
                            VALUES ( %(user_id)s,%(access_key)s,
                                     %(xml)s,%(year)s,
                                     %(month)s,%(day)s,%(environment)s,
                                     %(reception_state)s,%(estab)s,
                                     %(pto_emi)s, %(secuencial)s,
                                     %(coddoc)s,%(filename)s
                                   )
    """

    query_update = """
        UPDATE `eris_document` SET `eris_documentxml` = %(xml)s,
                                   `eris_docyear` = %(year)s,
                                   `eris_docymonth` = %(month)s,
                                   `eris_docday` = %(day)s,
                                   `eris_receptionstate` = %(reception_state)s,
                                   `eris_environment` = %(environment)s,
                                   `eris_document_estab` = %(estab)s,
                                   `eris_document_ptoemi` = %(pto_emi)s,
                                   `eris_document_secuencial` = %(secuencial)s,
                                   `eris_coddoc_id` = %(coddoc)s,
                                   `eris_user_id` = %(user_id)s,
                                   `eris_doc_filename` = %(filename)s
                            WHERE  `eris_document_id` = %(document_id)s
    """
    if doc_type_id in ( 'factura', 'notaCredito' ):
        identificacion =doc_data['identificacionComprador']
    elif doc_type_id == 'comprobanteRetencion':
        identificacion = ret_data['identificacionSujetoRetenido']
    else:
        raise ErisError(300, 'Tipo de documento %s no soportado' % doc_type_id)
    insert_data = {'user_id' : get_userid_from_vatno(identificacion),
                   'access_key' : doc_data['claveAcceso'],
                   'xml' : open(filename).read(),
                   'year' : doc_data['fechaEmision'][6:10],
                   'month' : doc_data['fechaEmision'][3:5],
                   'day' : doc_data['fechaEmision'][0:2],
                   'environment' : doc_data['ambiente'],
                   'reception_state' : doc_data['estado'],
                   'estab' : doc_data['estab'],
                   'pto_emi' : doc_data['ptoEmi'],
                   'secuencial' : doc_data['secuencial'],
                   'coddoc' : doc_data['codDoc'],
                   'filename' : fn,

                   }

    cursor = cnx.cursor()
    document_id = ""
    try:
        document_id = get_doc_id_by_accesskey(cnx, doc_data['claveAcceso'])
        #Si existe solamente actualiza
        insert_data.setdefault("document_id", document_id)
        cursor.execute(query_update,insert_data)
    except Exception, e:
        #Si no existe agrega y actualiza
        cursor.execute(query_insert,insert_data)
        document_id = get_doc_id_by_accesskey(cnx, doc_data['claveAcceso'])
        insert_data.setdefault("document_id", document_id)
        cursor.execute(query_update,insert_data)

    cursor.close()
    return document_id



def xml_2_byte(filename):
    import base64
    encoded_data = base64.b64encode(open(filename, 'rb').read())
    strg = ''
    for i in xrange((len(encoded_data)/40)+1):
        strg += encoded_data[i*40:(i+1)*40]

    return strg

def get_claveacceso(filename):
    from lxml import etree
    with open(filename, 'r') as xml:
        tree = etree.parse(xml, parser=None, base_url=None)
        root = tree.getroot()
        return root.xpath("//infoTributaria/claveAcceso/text()")[0]
def get_headerdata(filename):
    from lxml import etree
    global doc_type_id
    with open(filename, 'r') as xml:
        tree = etree.parse(xml, parser=None, base_url=None)
        root = tree.getroot()
        doc_data['tipoDocumento'] = root.tag
        doc_type_id = root.tag
        for element in root.iter("*"):
            if element.text is not None and not element.text.strip():
                element.text = None
            else:
                #print "%s:%s" % (element.tag, element.text)
                if element.tag == 'campoAdicional':
                    if element.attrib["nombre"] == "Email":
                        doc_data["email"] = element.text
                        ret_data["email"] = element.text
                else:
                    for key in doc_data.iterkeys():
                        if key == element.tag:
                            doc_data[key] = element.text
                    for key in ret_data.iterkeys():
                        if key == element.tag:
                            ret_data[key] = element.text
def send_doc(docstyle, filename):
    from suds.client import Client
    logging.basicConfig(level=logging.INFO)

    fn = P.join(C.signed_docs_folder, filename)
    if not P.isfile(fn):
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
        get_headerdata(fn)
        doc_data["estado"] = str(response_rec.estado)

        #Guarda el documento
        try:
            cnx = CN.connect(**C.mysql_config)
            add_user()
            document_id = save_doc(cnx, fn)
            logging.info("Guardando Documento No. %s" % document_id)
            #Guarda cualquier mensaje que se pudiera haber generado
            #print response_rec
            if hasattr(response_rec, "comprobantes"):
                #print response_rec.comprobantes
                for comprobantes in response_rec.comprobantes:
                    for comprobante in comprobantes:
                        if type( comprobante ).__name__ == 'list':
                            for comprobante_element in comprobante:
                                if hasattr(comprobante_element, 'mensajes'):
                                    for mensaje_tuple in comprobante_element.mensajes:
                                        for mensaje_element in mensaje_tuple:
                                            if type(mensaje_element).__name__ == 'list':
                                                for mensaje in mensaje_element:
                                                    insert_message(cnx, document_id, unicode(mensaje.identificador), "%s. %s" % (unicode(mensaje.informacionAdicional), unicode(mensaje.mensaje)), str(mensaje.tipo))

            """
            print "Tiene mensajes %s" % str(hasattr(response_rec, "mensajes"))
            #Inserta los mensajes referentes al documento de la ultima consulta
            for mens in response_rec.mensajes:
                print mens
                for ms in mens:
                    if not type(ms) is str:
                        for m in ms:
                            insert_message(cnx, str(document_id), str(m.identificador), str(m.mensaje), str(m.tipo))

            if hasattr(response_rec, "mensajes"):
                print response_rec["mensajes"]
                for message in response_rec["mensajes"]:
                    print "message %s" % message
                    #insert_message(cnx, document_id, msg_number, msg_text, msg_type)
                    for m in message["mensaje"]:
                        print m
            """
            #Elimina el archivo de los firmados
            cnx.commit()
            os.remove(fn)
        except Exception, e:
            try:
                cnx.rollback()
            except:
                pass
            """
            if e.errno == 1062:
                os.remove(fn)
            """
            logging.exception(e)
        finally:
            try:
                cnx.close()
            except:
                pass

def get_documentid_by_acceskey(cnx, accesskey):
    """
    Obtiene el id del documento con la clave de acceso se encuentre
    en la base de datos con el status de enviado
    """
    query = """
            SELECT eris_document_id FROM eris_document WHERE eris_accesskey = '%s'
            """ % accesskey
    cursor = cnx.cursor()
    cursor.execute(query)
    for document_id in cursor:
        return document_id[0]

    raise ErisError("101", "Documento no encontrado")

def update_authorizationnumber(cnx, document_id, authnumber, authdate, state):
    """
    Actualiza el numero de autorizacion y el estado del documento
    """
    query = """
            UPDATE eris_document SET eris_receptionstate = %(state)s, eris_authorizationnumber = %(authn)s,
                                     eris_authorizationdate = %(adate)s
            WHERE eris_document_id = %(did)s
            """
    update_data = {'state':state, 'authn':authnumber, 'adate':authdate, 'did':document_id}
    cursor = cnx.cursor()
    cursor.execute(query, update_data)


def delete_messages(cnx, document_id):
    """
    Elimina todos los mensajes relativos a un documento
    """
    query = """
            DELETE FROM eris_message WHERE eris_document_id = %(document_id)s
            """
    delete_data = {'document_id':document_id}
    cursor = cnx.cursor()
    cursor.execute(query, delete_data)

def insert_message(cnx, document_id, msg_number, msg_text, msg_type):
    """
    Inserta un mensaje relativo a un documento
    """
    query = """
            INSERT INTO `eris_message`(`eris_document_id`, `eris_message_number`, `eris_message_text`, `eris_message_type`)
                               VALUES (%(document_id)s,%(msg_number)s,%(msg_text)s, %(msg_type)s)
            """
    insert_data = {'document_id':document_id, 'msg_number':msg_number, "msg_text":msg_text, 'msg_type':msg_type}
    cursor = cnx.cursor()
    cursor.execute(query, insert_data)



def save_auth_file(accesskey):
    """
    Saves authorized file registered in database
    @param accesskey: Access Key

    """
    from lxml import etree
    #Creo el tag principal: autorizacion
    autorizacion_el = etree.Element('autorizacion')
    #print accesskey
    #Leo la base de datos para sacar los datos
    cnx = CN.connect(**C.mysql_config)
    query = """
            SELECT * FROM eris.eris_document
            WHERE eris_accesskey = %(accesskey)s
            AND eris_receptionstate = 'AUTORIZADO';
            """
    query_data = {'accesskey':accesskey}
    cursor = cnx.cursor()
    cursor.execute(query, query_data)
    comprobante = cursor.fetchone()
    doc_id = comprobante[0]
    auth_no = comprobante[3]
    doc = comprobante[4]
    auth_date = comprobante[10]
    state = comprobante[11]
    fn = comprobante[16]


    estado_el = etree.SubElement(autorizacion_el, 'estado')
    estado_el.text = state
    numeroAutorizacion_el = etree.SubElement(autorizacion_el, 'numeroAutorizacion')
    numeroAutorizacion_el.text = auth_no
    fechaAutorizacion_el = etree.SubElement(autorizacion_el, 'fechaAutorizacion')
    fechaAutorizacion_el.attrib['class'] = 'fechaAutorizacion'
    fechaAutorizacion_el.text = auth_date.strftime('%d/%m/%Y %H:%M:%S')
    comprobante_el = etree.SubElement(autorizacion_el, 'comprobante')
    comprobante_el.text = etree.CDATA(doc)

    cursor.close()

    #Obtengo los mensajes
    query = """
            SELECT eris_message_number, eris_message_text, eris_message_type
            FROM eris_message
            WHERE eris_document_id = %(document_id)s
            """
    query_data = {'document_id':doc_id}
    cursor = cnx.cursor()
    cursor.execute(query, query_data)
    mensajes_el = etree.SubElement(autorizacion_el, 'mensajes')
    for m in cursor:
        mensaje_el = etree.SubElement(mensajes_el, 'mensaje')
        mensaje2_el = etree.SubElement(mensaje_el, 'mensaje')
        identificador_el = etree.SubElement(mensaje2_el, 'identificador')
        identificador_el.text = m[0]
        mensaje3_el = etree.SubElement(mensaje2_el, 'mensaje')
        mensaje3_el.text = m[1]
        tipo_el = etree.SubElement(mensaje2_el, 'tipo')
        tipo_el.text = m[2]

    if not fn:
        fn = accesskey

    with open(P.join(C.authorized_docs_folder, "%s.xml" % fn), 'w') as xmlfile:
        xmlfile.write(etree.tostring(autorizacion_el, pretty_print=True))
    #print etree.tostring(autorizacion_el, pretty_print=True)
def load_auth_file(docstyle,filename):
    """
    Load authorized file to database
    """
    import time
    logging.basicConfig(level=logging.INFO)
    fn = P.join(C.authorized_docs_folder, filename)
    if not P.isfile(fn):
        #print fn
        raise FileNotFoundError(C.authorized_docs_folder, filename)
    logging.info("Guardando: %s: %s" % (docstyle,filename))
    #Reads file so I can get variables
    from lxml import etree
    tree = etree.parse(fn)
    eel= tree.xpath("/autorizacion/estado")
    e = eel[0].text #estado
    nael = tree.xpath("/autorizacion/numeroAutorizacion")
    na = nael[0].text #numero autorizacion
    cel = tree.xpath("/autorizacion/comprobante")
    c = cel[0].text #comprobante
    fael = tree.xpath("/autorizacion/fechaAutorizacion")
    fa_str = fael[0].text #fecha autorizacion
    try:
        fa = time.strptime(fa_str, "%d/%m/%Y %H:%M:%S.%f")
    except:
        fa = time.strptime(fa_str, "%d/%m/%Y %H:%M:%S")
    m1el = tree.xpath("/autorizacion/mensajes")
    #Temporaly saves the xml doc to hd so I can reutilize save_doc
    with open(P.join(C.signed_docs_folder, filename), 'w') as doc_firmado:
        doc_firmado.write(c.encode('utf-8'))
    try:
        cnx = CN.connect(**C.mysql_config)
    except Exception, e:
        raise e
    try:
        get_headerdata(P.join(C.signed_docs_folder, filename))
        add_user()
        document_id = save_doc(cnx, P.join(C.signed_docs_folder, filename))
        update_authorizationnumber(  cnx, document_id
                                   , na
                                   , fa
                                   , e)
        #Elimina los mensajes referentes al documento
        delete_messages(cnx, document_id)
        #Saves all mesages in db
        for m2 in m1el:
            for m3 in m2:
                for m4 in m3:
                    insert_message(cnx\
                            , document_id\
                            , m4[0].text\
                            , m4[1].text\
                            , m4[2].text)

        cnx.commit()
    except Exception, e:
        cnx.rollback()
        raise e
    finally:
        cnx.close()
    #Update fileds

    #Don't forget to remove temporaly xml
def authorize_doc(claveacceso, docstyle):
    from suds.client import Client
    import logging

    logging.basicConfig(
             filename=P.join(C.authorized_docs_folder,"eris.log")
            ,level = logging.INFO)
    logging.getLogger('suds.transport.http').setLevel(logging.INFO)
    logging.info("Autorizando: %s" % (claveacceso))

    try:
        cnx = CN.connect(**C.mysql_config)
        document_id = get_documentid_by_acceskey(cnx, claveacceso)
        #Realiza la autorizacion por el webservice
        headers = {'Content-Type': 'application/soap+xml; charset="UTF-8"'}
        client_aut = Client(C.authorization_url, headers=headers)
        if docstyle == "comprobante":
            response_aut = client_aut.service.autorizacionComprobante(claveacceso)
        elif docstyle == "lote":
            response_aut = client_aut.service.autorizacionComprobanteLoteMasivo(claveacceso)

        if not hasattr(response_aut, "autorizaciones"):
            raise ErisError("102", "La clave de acceso %s no tiene autorizaciones" % claveacceso)

        #Elimina los mensajes referentes al documento
        delete_messages(cnx, document_id)

        for a in response_aut.autorizaciones.autorizacion:
            if hasattr(a, "numeroAutorizacion"):
                update_authorizationnumber(  cnx, document_id
                                           , str(a.numeroAutorizacion)
                                           , a.fechaAutorizacion
                                           , str(a.estado))
            #Inserta los mensajes referentes al documento de la ultima consulta
            for mens in a.mensajes:
                for ms in mens:
                    if not type(ms) is str:
                        for m in ms:
                            insert_message(cnx, str(document_id), str(m.identificador), str(m.mensaje), str(m.tipo))


        cnx.commit()
        #Guarda el archivo xml en la carpeta de autorizaciones
        save_auth_file(claveacceso)
    except Exception, e:
        logging.exception(e)
        cnx.rollback()


def sign(tagid, filename):
    """
    Java signer call
    """

    fn = P.join(C.unsigned_docs_folder, filename)
    if not P.isfile(fn):
        raise FileNotFoundError(C.unsigned_docs_folder, filename)

    from subprocess import call
    call(["java", "-jar", C.signer_home, "sign", tagid, filename])


def send2sri(claveacceso, docstyle, filename, do_sign):
    try:
        if do_sign:
            sign(docstyle, filename)
        send_doc(docstyle, filename)
        authorize_doc(claveacceso, docstyle)
    except Exception, e:
        logging.exception(e)
    #claveacceso = get_claveacceso(fn)

def batch_send(dirname, do_sign):
    """
    Send files in batch mode usig folder
    """
    #Check if folder exists
    if os.path.exists(dirname) and os.path.isdir(dirname):
        for f in os.listdir(dirname):
            if (f[-4:]).lower() == ".xml":
                try:
                    claveAcceso = get_claveacceso(os.path.join(dirname, f))
                except Exception, e:
                    raise ErisError('201',
                            '''No se pudo obtner la clave del acceso
                            del arhivo %s. %s''' % (dirname, traceback.format_exc()
                                ))
                send2sri(get_claveacceso(os.path.join(dirname, f)),
                         'comprobante',
                         os.path.join(dirname, f),
                         do_sign
                        )

def email_link(accesskey):
    """
    Send email to customer
    @param accesskey: Access Key

    """
    pass
