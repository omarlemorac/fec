# -*- coding: utf-8 -*-

import smtplib
from os.path import basename
from email.MIMEBase import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.MIMEImage import MIMEImage
from email import Encoders
from repo_model import Model
import config as C
import os
from xreport import generate
from xml_parser import parse, parse_voucher
from lexus_model import model as LM
import pdb
def send_mail(send_from, send_to, subject, text, files=None ):
    """Send email"""
    send_to = "marcelo.mora@hotmail.es"
    msg_root = MIMEMultipart('related')
    msg_root['From'] = send_from
    msg_root['To'] = send_to
    msg_root['Subject'] = subject

    msg_alt = MIMEMultipart('alternative')
    msg_root.attach(msg_alt)
    msg_alt.attach(MIMEText("Documento electronico", 'plain'))
    msg_alt.attach(MIMEText(text, 'html'))

    with open('logo_mail.png', 'rb') as fp:
        msg_image = MIMEImage(fp.read())


    msg_image.add_header('Content-ID','logo_mail.png' )
    msg_root.attach(msg_image)


    for f in files or []:
        if f[-3:] == 'pdf':
            attachFile = MIMEBase('application', 'PDF')
            attachFile.set_payload(open(f, "rb").read())
            Encoders.encode_base64(attachFile)
            attachFile.add_header('Content-Disposition', 'attachment',
                    filename='ride.pdf')
            msg_root.attach(attachFile)
        if f[-3:] == 'xml':
            attachFile = MIMEBase('application', 'XML')
            attachFile.set_payload(open(f, "rb").read())
            Encoders.encode_base64(attachFile)
            attachFile.add_header('Content-Disposition', 'attachment',
                    filename='comprobante.xml')
            msg_root.attach(attachFile)

    server = smtplib.SMTP_SSL('pro.turbo-smtp.com')
    username = "proveedores@fullcarga.com.ec"
    password = "0Sw9dSwR"
    server.login(username, password)
    server.sendmail(send_from, [send_to],msg_root.as_string())
    server.quit()


def send_emails():
    m = Model()
    couchdb = m.get_database(C.couchdb_config['doc_db'])

    for i in m.read(C.couchdb_config['doc_db'], m.OUTSTANDING_EMAIL):
        xml = os.path.join(C.authorized_docs_folder, "{}_1.xml".format( i.value['claveacceso']) )
        rep_xml = parse(xml)
        dct = parse_voucher(rep_xml['comprobante'])
        dct['numeroAutorizacion'] = i.value["numeroAutorizacion"]
        dct['fechaAutorizacion'] = i.value["fechaAutorizacion"]
        pdf = os.path.join(C.authorized_docs_folder, "{}_1.pdf".format(
            i.value['claveacceso']))
        generate(dct, 0,pdf  )
        text = ''
        with open('mail.html', 'r') as ma:
            text = ma.read()

        subject = u"Documentos electronicos enviados por Fullcarga Ecuador"
        send_from = "proveedores@fullcarga.com.ec"
        send_to = i.value['email_recipient']
        files = [xml, pdf]

        send_mail(send_from, send_to, subject, text, files)
#   Once the email is sended update db with mail_sended = True
        m.write_mail_sended(C.couchdb_config['doc_db'], i.value['claveacceso'])
def send_validation_log():
    """Send validation log to responsibles"""
    fp = open('/home/fec/validation.log', 'r')
    msg = fp.read()
    fp.close()
    text = msg
    subject = "Errores en facturacion por csv"
    send_from = "marcelo.mora@gmail.com"
    send_to = ["proveedores@fullcarga.com.ec",
               "jquiroga@fullcarga.com.ec",
               "ing.eduardosilva@gmail.com",
               "java.diablo@gmail.com"]
#    send_to = [ "java.diablo@gmail.com"]
    files = []

    send_mail(send_from, send_to, subject, text, files)

if __name__ == '__main__':
    send_emails()
