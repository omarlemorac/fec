# -*- coding: utf-8 -*-

from ftplib import FTP
import sys

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

def download_eris():
    ftp = FTP(ip)
    ftp.login(user, password)
    a = ftp.cwd("FILES_SIGMA")
    ftp.voidcmd("TYPE I")
    retr_cmd = 'RETR eris.tar.gz'
    datasock, estsize = ftp.ntransfercmd(retr_cmd)
    transbytes = 0
    fd =open("/home/fec/eris.tar.gz", "wb")
    while 1:
        buf = datasock.recv(2048)
        if not len(buf):
            break
        fd.write(buf)
        transbytes += len(buf)
        sys.stdout.write("received %d" % transbytes)

        if estsize:
            sys.stdout.write("of %d bytes (%.1f%%)\r" % \
                    (estsize, 100.0 * float(transbytes) / float(estsize)))
        else:
            sys.stdout.write("bytes\r")

        sys.stdout.flush()
    sys.stdout.write("\n")
    fd.close()
    datasock.close()
    ftp.voidresp()
    ftp.quit()


if __name__ == '__main__':
    download_eris()
