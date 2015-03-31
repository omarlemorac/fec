# -*- coding: utf-8 -*-

import smtplib
from os.path import basename
from email.MIMEBase import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import Encoders
from repo_model import Model
import config as C
import os
from xreport import generate
from xml_parser import parse, parse_voucher
def send_mail(send_from, send_to, subject, text, files=None ):
    """Send email"""
    assert isinstance(send_to, list)
    print subject
    msg = MIMEMultipart(
        From=send_from,
        To=COMMASPACE.join(send_to),
        Date=formatdate(localtime=True),
        Subject=subject
    )
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    for f in files or []:
        if f[-3:] == 'pdf':
            attachFile = MIMEBase('application', 'PDF')
            attachFile.set_payload(open(f, "rb").read())
            Encoders.encode_base64(attachFile)
            attachFile.add_header('Content-Disposition', 'attachment',
                    filename='ride.pdf')
            msg.attach(attachFile)
        if f[-3:] == 'xml':
            attachFile = MIMEBase('application', 'XML')
            attachFile.set_payload(open(f, "rb").read())
            Encoders.encode_base64(attachFile)
            attachFile.add_header('Content-Disposition', 'attachment',
                    filename='comprobante.xml')
            msg.attach(attachFile)

    server = smtplib.SMTP('smtp.gmail.com:587')
    username = "java.diablo@gmail.com"
    password = "Megadeth666"
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail("Accioma",
    "grobalino@fullcarga.com.ec",msg.as_string()
            )
    server.quit()


def send_emails():
    m = Model()
    couchdb = m.get_database(C.couchdb_config['doc_db'])
    for i in m.read(C.couchdb_config['doc_db'], m.AUTHORIZED):
        xml = os.path.join(C.authorized_docs_folder, "{}_1.xml".format( i.value['claveacceso']) )
        rep_xml = parse(xml)
        dct = parse_voucher(rep_xml['comprobante'])
        pdf = os.path.join(C.authorized_docs_folder, "{}_1.pdf".format(
            i.value['claveacceso']))
        generate(dct, 0,pdf  )
        text = "Documento electronico No. {}".format(i.value['claveacceso'])
        subject = "Documento electronico'"
        send_from = "marcelo.mora@gmail.com"
        send_to = ["java.diablo@gmail.com"]
        files = [xml, pdf]

        send_mail(send_from, send_to, subject, text, files)


if __name__ == '__main__':
    send_emails()
