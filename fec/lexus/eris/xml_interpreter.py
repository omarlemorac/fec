'''
Created on May 2, 2014

@author: marcelo
'''
import base64

def signXml():
    #import jpype as JP
    import config as C
    from subprocess import call
    """
    #JPype no funciona con Java 7
    #JPype no puede acceder a atributos protected    
    JP.startJVM(C.java_start, "-Djava.class.path="+C.signer_home)
    DesEncrypt = JP.JPackage("com").accioma.eris.sign.xades.DesEncrypt
    passwd = DesEncrypt.decrypt(C.sign_password)
    
    Signer = JP.JPackage("com").accioma.eris.sign.xades.XAdESBESCoSignature
    signer = Signer( C.signed_docs_folder
                    ,"LOTE.XML" 
                    ,C.authorized_docs_folder
                    ,"LOTE.XML"
                    ,passwd
                    ,"lote"
                    ,"Documento lote"
                    ,"text/xml")
    print signer.toString()
    try:
        signer.testFunc()
        signer.execute()
    except Exception, e:
        print e
    print(str(dir(signer)))
    
    
    JP.java.lang.System.out.println("Hola Xml")
    JP.shutdownJVM()
    """
    
    call(["java", "-jar", C.signer_home, "sign", "lote", "LOTE.XML"])

def xml_2_byte(filename):
    encoded_data = base64.b64encode(open(filename, 'rb').read())
    strg = ''
    for i in xrange((len(encoded_data)/40)+1):
        strg += encoded_data[i*40:(i+1)*40]
    
    return strg

def autorize_doc(filename):
    import suds  # @UnresolvedImport
    from suds.client import Client  # @UnresolvedImport
    import logging
    
    logging.basicConfig(level = logging.INFO)
    logging.getLogger('suds.transport.http').setLevel(logging.DEBUG)
    
    
    headers = {'Content-Type': 'application/soap+xml; charset="UTF-8"'}
    client_rec = Client("https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantes?wsdl")
    response_rec = client_rec.service.validarComprobante(xml_2_byte(filename))
    with open("/home/marcelo/Documents/Eris/recepcion.txt", "w") as rf: 
        rf.write(str(response_rec))
    
    client_aut = Client("https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantes?wsdl", headers=headers)
    #print client_aut
    try:
        response_aut = client_aut.service.autorizacionComprobante("1905201401099237878600110010010000789120000005313")
        
        with open("/home/marcelo/Documents/Eris/autorizacion.txt", "w") as rf: 
            #rf.write(str(dir(response_aut)))
            #rf.write("\nAutorizaciones\n");
            #rf.write(str(dir(response_aut.autorizaciones)))
            #rf.write("\nAutorizacion\n");
            #rf.write(str(response_aut.autorizaciones.autorizacion))
            #rf.write("\nLista Autorizacion\n")

            for a in response_aut.autorizaciones.autorizacion:
                rf.write(str(dir(a)))
                rf.write("\nAmbiente: %s" % str(a.ambiente) )
                rf.write("\nfechaAutorizacion %s" % str(a.fechaAutorizacion) )
                rf.write("\nEstado %s" % str(a.estado))
                if hasattr(a, "numeroAutorizacion"):
                    rf.write("\nNumeroAutorizacion %s" % str(a.numeroAutorizacion))
                rf.write("\nComprobante\n")
                rf.write("\n%s" % str(a.comprobante))

                rf.write("\nMensajes\n")
                for mens in a.mensajes:
                    for ms in mens:
                        if not type(ms) is str:
                            for m in ms:
                                rf.write("\nIdentificador: %s\n" % m.identificador)
                                rf.write("Mensaje: %s\n" % m.mensaje)
                                rf.write("Tipo: %s\n" % m.tipo)
                        
    except suds.WebFault as detail:
        print detail 

    

def test_byte(ba):
    with open("/home/marcelo/Documents/Eris/test_xml.xml", "w") as rf:
        rf.write(str(ba))
    
    
if __name__ == '__main__':
    filename = "/home/marcelo/Documents/Eris/DOC_FIRMADOS/POS-1905201401099237878600110010010000789120000005313.XML"
    #filename = "/home/marcelo/Documents/Eris/sign_test/factura_xades.xml"
    
    #test_byte(xml_2_byte(filename))
    #autorize_doc(filename)
    signXml()