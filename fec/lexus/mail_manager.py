# -*- coding: utf-8 -*-

import smtplib
from os.path import basename
from email.MIMEBase import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import Encoders

def send_mail(send_from, send_to, subject, text, files=None ):
    """Send email"""
    assert isinstance(send_to, list)
    msg = MIMEMultipart(
        From=send_from,
        To=COMMASPACE.join(send_to),
        Date=formatdate(localtime=True),
        Subject=subject
    )
    msg.attach(MIMEText(text))

    for f in files or []:
        attachFile = MIMEBase('application', 'PDF')
        attachFile.set_payload(open(f, "rb").read())
        Encoders.encode_base64(attachFile)
        attachFile.add_header('Content-Disposition', 'attachment',
                filename='ride.pdf')
        msg.attach(attachFile)

    server = smtplib.SMTP('smtp.gmail.com:587')
    username = "java.diablo@gmail.com"
    password = "Megadeth666"
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail("Accioma",
    "marcelo.mora@hotmail.es",msg.as_string()
            )
    server.quit()

if __name__ == '__main__':
    text = "Hola email"
    subject = "Hola email"
    send_from = "marcelo.mora@gmail.com"
    send_to = ["java.diablo@gmail.com"]
    files =\
    ['/home/fec/authorized/test.pdf']
    send_mail(send_from, send_to, subject, text, files)

