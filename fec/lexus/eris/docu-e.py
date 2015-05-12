#-*- coding: utf-8 -*-
'''
Created on 27/05/2014

@author: Administrador
'''
import traceback
import logging as L
import config as C
from os import path as P
import argparse
from lxml import etree
from datetime import datetime as DT
import pdb
import os
import time
L.basicConfig(
         filename=P.join(C.authorized_docs_folder,"eris.log")
        ,level = L.ERROR)
parser = argparse.ArgumentParser(description=u"SRI eDocuments")
parser.add_argument('-p', '--path', required=True, help="Absolute path to signed files")
args = parser.parse_args()

#L.basicConfig(filename=P.join(C.authorized_docs_folder,"eris.log") , level = L.INFO)
logger = L.getLogger('docue_main')
logger.setLevel(L.DEBUG)
formatter = L.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = L.FileHandler("docue.log")
fh.setFormatter(formatter)
logger.addHandler(fh)
process_path = ""

def xml_2_byte(filename):
    import base64
    encoded_data = base64.b64encode(open(filename, 'rb').read())
    strg = ''
    for i in xrange((len(encoded_data)/40)+1):
        strg += encoded_data[i*40:(i+1)*40]

    return strg

def get_estado(filename):
    """
    Returns accesskey from document
    """
    from lxml import etree
    with open(filename, 'r') as xml:
        tree = etree.parse(xml, parser=None, base_url=None)
        root = tree.getroot()
        return root.xpath("//infoTributaria/claveAcceso/text()")[0]

def get_claveacceso(filename):
    """
    Returns accesskey from document
    """
    from lxml import etree
    with open(filename, 'r') as xml:
        tree = etree.parse(xml, parser=None, base_url=None)
        root = tree.getroot()
        return root.xpath("//infoTributaria/claveAcceso/text()")[0]

def save_rec_file(response, fn):
    """
    Saves received file registered in database
    @param response: Response object
    @param fn: Original xml filename
    """
    from lxml import etree
    #Creo el tag principal:
    autorizacion_el = etree.Element('autorizacion')
    doc_id = get_claveacceso(fn)
    auth_no = ''
    with open(fn) as rf:
        doc = rf.read()
    auth_date = DT.now()
    state = response.estado

    estado_el = etree.SubElement(autorizacion_el, 'estado')
    estado_el.text = state
    numeroAutorizacion_el = etree.SubElement(autorizacion_el, 'numeroAutorizacion')
    numeroAutorizacion_el.text = auth_no
    fechaAutorizacion_el = etree.SubElement(autorizacion_el, 'fechaAutorizacion')
    fechaAutorizacion_el.attrib['class'] = 'fechaAutorizacion'
    fechaAutorizacion_el.text = auth_date.strftime('%d/%m/%Y %H:%M:%S')
    comprobante_el = etree.SubElement(autorizacion_el, 'comprobante')
    comprobante_el.text = etree.CDATA(doc)


    #Obtengo los mensajes
    if hasattr(response, "estado"):
        if response['estado'] == 'RECIBIDA':
            logger.info("%s: RECIBIDA" % doc_id)
            return True

        #Guarda cualquier mensaje que se pudiera haber generado
        if hasattr(response, "comprobantes"):
            for comprobantes in response.comprobantes:
                for comprobante in comprobantes:
                    if type( comprobante ).__name__ == 'list':
                        for comprobante_element in comprobante:
                            mensajes_el = etree.SubElement(autorizacion_el, 'mensajes')
                            if hasattr(comprobante_element, 'mensajes'):
                                for mensaje_tuple in comprobante_element.mensajes:
                                    mensaje_el = etree.SubElement(mensajes_el, 'mensaje')
                                    for mensaje_element in mensaje_tuple:
                                        mensaje2_el = etree.SubElement(mensaje_el, 'mensaje')
                                        if type(mensaje_element).__name__ == 'list':
                                            for mensaje in mensaje_element:
                                                identificador_el = etree.SubElement(mensaje2_el, 'identificador')
                                                identificador_el.text = unicode(mensaje.identificador)
                                                mensaje3_el = etree.SubElement(mensaje2_el, 'mensaje')
                                                mensaje3_el.text = unicode(mensaje.mensaje)
                                                tipo_el = etree.SubElement(mensaje2_el, 'tipo')
                                                tipo_el.text = str(mensaje.tipo)
                                                infoAdicional_el =\
                                                etree.SubElement(mensaje2_el,\
                                                        'infoAdicional')
                                                infoAdicional_el.text =\
                                                unicode(mensaje.informacionAdicional)

    #print etree.tostring(autorizacion_el, pretty_print=True)
    with open(P.join(C.temp_folder, "%s" % P.basename(fn)), 'w') as xmlfile:
        logger.info( 'Guardando: %s' % P.join(C.temp_folder, "%s" % fn))
        xmlfile.write(etree.tostring(autorizacion_el, pretty_print=True))

def save_auth_file(response, fn):
    if not hasattr(response, "autorizaciones"):
        raise ErisError("102", "La clave de acceso %s no tiene autorizaciones" % claveacceso)
    from lxml import etree
    for au in response.autorizaciones:
        counter = 0
        for aut in  au[1]:
            auth_no = ''
            if hasattr(aut, "numeroAutorizacion"):
                auth_no = aut.numeroAutorizacion

            autorizacion_el = etree.Element('autorizacion')
            estado_el = etree.SubElement(autorizacion_el, 'estado')
            estado_el.text = aut.estado
            numeroAutorizacion_el = etree.SubElement(autorizacion_el, 'numeroAutorizacion')
            numeroAutorizacion_el.text = auth_no
            fechaAutorizacion_el = etree.SubElement(autorizacion_el, 'fechaAutorizacion')
            fechaAutorizacion_el.attrib['class'] = 'fechaAutorizacion'
            fechaAutorizacion_el.text = aut.fechaAutorizacion.strftime('%d/%m/%Y %H:%M:%S')
            comprobante_el = etree.SubElement(autorizacion_el, 'comprobante')
            comprobante_el.text = etree.CDATA(aut.comprobante)


            mensajes_el = etree.SubElement(autorizacion_el, 'mensajes')
            for mensaje_tuple in aut.mensajes:
                mensaje_el = etree.SubElement(mensajes_el, 'mensaje')
                for mensaje_element in mensaje_tuple:
                    mensaje2_el = etree.SubElement(mensaje_el, 'mensaje')
                    if type(mensaje_element).__name__ == 'list':
                        for mensaje in mensaje_element:
                            identificador_el = etree.SubElement(mensaje2_el, 'identificador')
                            identificador_el.text = unicode(mensaje.identificador)
                            mensaje3_el = etree.SubElement(mensaje2_el, 'mensaje')
                            mensaje3_el.text = unicode(mensaje.mensaje)
                            tipo_el = etree.SubElement(mensaje2_el, 'tipo')
                            tipo_el.text = str(mensaje.tipo)
                            infoAdicional_el =\
                            etree.SubElement(mensaje2_el,'infoAdicional')
                            try:
                                infoAdicional_el.text =unicode(mensaje.informacionAdicional)
                            except:
                                pass
            xfn = P.basename(fn)
            if not auth_no:
                counter += 1
                xfn = "%s%03d.XML" % ( P.basename(fn)[:-4], counter )
            with open(P.join(C.authorized_docs_folder, "%s" % xfn), 'w') as xmlfile:
                logger.info( 'Guardando: %s' % P.join(C.authorized_docs_folder, "%s" % xfn))
                xmlfile.write(etree.tostring(autorizacion_el, pretty_print=True))

def send_doc(filename):
    from suds.client import Client
    client_rec = Client(C.deliver_url)
    response_rec = client_rec.service.validarComprobante(xml_2_byte(filename))
    save_rec_file(response_rec, filename)
    h = {'Content-Type': 'application/soap+xml; charset="UTF-8"'}
    client_aut = Client(C.authorization_url, headers=h)
    response_aut = client_aut.service.autorizacionComprobante(get_claveacceso(filename))
    os.remove(filename)
    save_auth_file(response_aut, filename)

def list_files():
    """
    List all files in path
    """
    import os
    return [os.path.join(process_path, f) for f in os.listdir(process_path) if
            os.path.isfile(os.path.join(process_path, f)) and f[-4:].lower() ==
            '.xml']


def process_files():
    for f in list_files():
        logger.info("Procesando archivo %s a las %s" % (f, DT.now().strftime('%H:%M:%S')))
        print "Procesando archivo %s a las %s" % (f, DT.now().strftime('%H:%M:%S'))
        try:
            while True:
		try:
                    send_doc(f)
		    break
	    	except Exception, e:
		    if type(e).__name__ != "SSLError":
			logger.error("Error al enviar: %s", e)
		        break
		    logger.error("Error timeout: %s", e)
	            print "Web Service del SRI no responde. Por favor espere...."
	            time.sleep(C.time_out)

        except Exception, e:
            logger.exception(traceback.print_exc())


def run():
    opts = parser.parse_known_args()
    logger.info("Path: %s " % args.path)
    logger.info("Start processing ")
    global process_path
    process_path = args.path
    process_files()

    print "===================================================="
    print "        PROCESO TERMINADO                           "
    print "===================================================="



if __name__ == '__main__':
    run()
