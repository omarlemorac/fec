# -*- coding: utf-8 -*-

from ftplib import FTP

port = 21
ip = "ftp.fullcarga.com.ec"
password = "facele2014$$"
user = "lexus@fullcarga.com.ec"

def download():
    ftp = FTP(ip)
    ftp.login(user, password)
    a = ftp.cwd("FILES_SIGMA")
 #   clientes_fn = "PREFACTURA_ELECTRONICA_CLIENTES_2015-02-13_1423778875327.csv"
    clientes_fn = "PRUEBA_CLIENTES.csv"
    ventas_fn = "PREFACTURA_ELECTRONICA_VENTAS_2015-02-13_1423778875327.csv"
    with open("/home/fec/clientes.csv", "wb") as gFile:
        retr_cmd = 'RETR %s' % clientes_fn
        ftp.retrbinary(retr_cmd, gFile.write)
    with open("/home/fec/ventas.csv", "wb") as gFile:
        retr_cmd = 'RETR %s' % ventas_fn
        ftp.retrbinary(retr_cmd, gFile.write)
    ftp.quit()

if __name__ == '__main__':
    download()
