#!/usr/bin/env python
# -*- coding: utf-8 -*-


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code39, code128, code93, eanbc, qr, usps
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
import time
import pdb
tipo_emision = {'1':u'PRUEBAS', '2':u'PRODUCCIÓN'}
def rcandrawString(can, x, y, cadena):
    can.drawRightString(x, y, cadena)

def drawString(can, x, y, cadena, length=12):
    if len(cadena)>length:
        l=cadena[:length].rfind(" ")
        if l < 0:
            l=cadena.find(" ")
        can.drawString(x, y + 5, cadena[:l])
        can.drawString(x, y - 5, cadena[l:])
    else:
        can.drawString(x, y, cadena)

def candrawString(can, x, y, cadena):
    if len(cadena)>15:
        l=cadena[:12].rfind(" ")
        if l < 0:
            l=cadena.find(" ")
        if l < 0:
            l=12
        can.drawString(x, y + 5, cadena[:l])
        can.drawString(x, y - 5, cadena[l:])
    else:
        can.drawString(x, y, cadena)


def generate(data, ix, fileout):

    infoTributaria = data["infoTributaria"]
    infoFactura = data["infoFactura"]
    #detalles=data["detalles"]["detalle"]
    detalles=data["detalles"]


    #Inicializa el canvas
    d=["FACTURA", "NOTA DE DÉBITO", "NOTA DE CRÉDITO", "GUÍA DE REMISIÓN"]
    can = canvas.Canvas(fileout, pagesize=letter)
    can.setLineWidth(.3)

    #Dibuja los primeros cuadros
    can.setFont('Helvetica', 12)
    can.roundRect(300, 450, 230, 280, 3, stroke=1, fill=0)
    can.roundRect(60, 450, 238, 160, 3, stroke=1, fill=0)
    can.rect(60, 390, 470, 58, stroke=1, fill=0)

    #el logo de la empresa, debes cambiar el contenido del archivo logo.png o reapuntar el archivo
    can.drawImage('logo.png', 60, 612, 238, 128)

    #El contenido del primer cuadro a la derecha
    can.drawString(305,700,'R.U.C.:    '+infoTributaria["ruc"])
    can.setFont('Helvetica', 14)
    can.drawString(305,680, d[ix])
    can.setFont('Helvetica', 10)
    can.drawString(305,660,u'No.       '+infoTributaria["estab"]+"-"+infoTributaria["ptoEmi"]+"-"+infoTributaria["secuencial"])
    can.setFont('Helvetica', 12)
    can.drawString(305,640,u'NÚMERO DE AUTORIZACIÓN')
    can.setFont('Helvetica', 10 )
    can.drawString(305,620,data['numeroAutorizacion'])
    can.drawString(305,600,u'FECHA Y HORA DE')
    can.drawString(305,590,u'AUTORIZACIÓN')

    can.setFont('Helvetica', 8)
    can.drawString(425,595, data['fechaAutorizacion'])
    can.setFont('Helvetica', 10)

    can.drawString(305,570,u'AMBIENTE:')
    can.drawString(420,570,tipo_emision[infoTributaria['tipoEmision']])
    can.drawString(305,550,u'EMISIÓN: NORMAL')
    can.setFont('Helvetica', 12)
    can.drawString(305,530,u'CLAVE DE ACCESO')
    can.setFont('Helvetica', 8)
    code=infoTributaria["claveAcceso"]

    barcode = code128.Code128(code)
    barcode.barWidth=0.6
    barcode.barHeight=30
    barcode.ratio=0.5
    barcode.drawOn(can, 300,490 )
    can.drawString(305,460,code)


    #Contenido del primer cuadro a la izquierda
    can.setFont('Helvetica', 10)
    can.drawString(65,600,'CODEPRET S.A.')
    can.setFont('Helvetica', 8)
    can.drawString(65,580,'FULLCARGA')
    can.drawString(65,550,u'Dirección')
    can.drawString(65,540,u'Matriz:')


    drawString(can, 110,545,infoTributaria["dirMatriz"])

    can.drawString(65,520,u'Dirección')
    can.drawString(65,510,u'Sucursal:')

    drawString(can,110,515,infoFactura["dirEstablecimiento"], 40)

    can.drawString(65,480,u'Contribuyente Especial Nro')
    can.drawString(180,480,infoFactura['contribuyenteEspecial'])

    can.drawString(65,460,u'OBLIGADO A LLEVAR CONTABILIDAD')
    can.drawString(220,460,infoFactura["obligadoContabilidad"])

    #contenido del cuadro intermedio
    can.drawString(65,430,u'Razón Social / Nombres y Apellidos: ')
    can.drawString(65,415,infoFactura["razonSocialComprador"])

    can.drawString(365,430,u'Identificación:   '+infoFactura["identificacionComprador"])
    can.drawString(65,400,u'Fecha Emisión:    ' +infoFactura["fechaEmision"])
    can.drawString(365,400,u'Guía Remisión:')

    n=len(detalles)
    s=388
    st=80
    lt=25

    #tabla de detalles. Crea "n" cantidad de filas, creando páginas si es necesario
    ii=0
    while 1:
        can.setFont('Helvetica', 8)
        if not n: break
        nn=min(int((s-st)/lt)+1, n)

        ss=s-((nn+1)*lt)

        n -= nn


        lens = [10,10,8,17,13,13,13,12]
        titles = ["Cod Principal", "Cod Auxiliar", "Cant","Descripción", "Detalle Adicional",
                  "Precio Unitario", "Descuento","Precio Total"]

        x=60
        lx = 0
        xs = list()
        for a in range(0, len(lens)):
            if (' ' in titles[a]):
                title = titles[a].split()
                can.drawString(x+5,s-20,title[1])
                can.drawString(x+5,s-10,title[0])
            else:
                can.drawString(x+5,s-15,titles[a])
            can.line(x,s,x,ss)
            xs.append(x+5)
            lx = x
            x+=int(lens[a]*4.7)


        for a in range(0, nn+1):
            y=ss+(a*lt)
            #canvas.line(60,ss+(a*lt),470,ss+((a)*lt))
            can.rect(60, y, 470, lt, stroke=1, fill=0)
            if a:
                candrawString(can, xs[0],y-15,detalles[ii]["codigoPrincipal"])
                if hasattr(detalles[ii], "codigoAuxiliar"):
                    candrawString(can, xs[1],y-15,detalles[ii]["codigoAuxiliar"])
                candrawString(can, xs[2],y-15,detalles[ii]["cantidad"])
                candrawString(can, xs[3],y-15,detalles[ii]["descripcion"])
                if hasattr(detalles[ii],"detallesAdicionales"):
                    candrawString(can, xs[4],y-15,detalles[ii]["detallesAdicionales"]["_detAdicional"]["valor"])
                rcandrawString(can, xs[6]-10,y-15,detalles[ii]["precioUnitario"])
                rcandrawString(can, xs[7]-10,y-15,detalles[ii]["descuento"])
                rcandrawString(can, x,y-15,detalles[ii]["precioTotalSinImpuesto"])

        if n:
            s = 700
            can.showPage()


   #si no hay espacio para el resumen final, avanzar otra página
    if ss < 220:
        can.showPage()
        ss = 700

    lt = 20


    #resumen final
    titles = ["SUBTOTAL 12%", "SUBTOTAL 0%", "SUBTOTAL No objeto de IVA", "SUBTOTAL Exento de IVA",
              "SUBTOTAL SIN IMPUESTOS", "TOTAL Descuento", "ICE", "IVA 12%", "IRBPNR",
              "PROPINA", "VALOR TOTAL"]

    ys=list()
    for a in range(0, 11):
        y=ss-((a+1)*lt)
        ys.append(y+lt)
        can.rect(320, y, 210, lt, stroke=1, fill=0)
        can.drawString(325,y+5,titles[a])

    can.line(lx,ss-((a+1)*lt),lx,ss)


    desc=0
    imp=0
    imps=dict({"2":[0,0], "3":[0,0], "5":[0,0]})
    ivas=dict({"0":[0,0], "2":[0,0], "6":[0,0], "7":[0,0]})
    for a  in detalles:
        desc+=float(a["descuento"])
        for b in a["impuestos"]:
            imp += float(b["valor"])
            imps[b["codigo"]][0] += float(b["baseImponible"])
            imps[b["codigo"]][1] += float(b["valor"])
            #if b["codigo"]=='2':
            ivas[b["codigoPorcentaje"]][0] += float(b["baseImponible"])
            ivas[b["codigoPorcentaje"]][1] += float(b["valor"])

    #print(ivas)

    rcandrawString(can, x, ys[0]-15, str(round(ivas["2"][0], 2)))
    rcandrawString(can, x, ys[1]-15, str(round(ivas["0"][0], 2)))
    rcandrawString(can, x, ys[2]-15, str(round(ivas["6"][0], 2)))
    rcandrawString(can, x, ys[3]-15, str(round(ivas["7"][0], 2)))
    rcandrawString(can, x, ys[4]-15, infoFactura["totalSinImpuestos"])
    rcandrawString(can, x, ys[5]-15, str(round(desc)))
    rcandrawString(can, x, ys[6]-15, str(round(imps["3"][1], 2)))
    rcandrawString(can, x, ys[7]-15, str(round(imps["2"][1], 2)))
    rcandrawString(can, x, ys[8]-15, str(round(imps["5"][1], 2)))
    rcandrawString(can, x, ys[9]-15, "0")
    rcandrawString(can, x, ys[10]-15, str(round(imp + float(infoFactura["totalSinImpuestos"]), 2)))
    sk = ss-(lt*8)-2
    can.rect(70, sk, 248, (lt*6)+40, stroke=1, fill=0)
    sk +=(lt*6)
    can.setFont('Helvetica', 12)
    can.drawString(105,sk+15 , u"Información Adicional")
    can.setFont('Helvetica', 11)
    can.drawString(75,sk , u"Dirección")
    can.drawString(75,sk - 33, u"Teléfono")
    can.drawString(75,sk - 61, u"Email")
    can.drawString(75,sk - 87, u"Observación")
    can.setFont('Helvetica', 8)
    can.drawString(75,sk - 12, data['infoAdicional']['Direccion'])
    can.drawString(75,sk - 42, data['infoAdicional']['Telefono'])
    can.drawString(75,sk - 70, data['infoAdicional']['Email'])
    can.drawString(75,sk - 97, data['infoAdicional']['Observacion'])

    """can.drawString(30,735,'OF ACME INDUSTRIES')
    can.drawString(500,750,"12/12/2010")
    can.line(480,747,580,747)

    can.drawString(275,725,'AMOUNT OWED:')
    can.drawString(500,725,"$1,000.00")
    can.line(378,723,580,723)

    can.drawString(30,703,'RECEIVED BY:')
    can.line(120,700,580,700)
    #can.drawString(120,703,"JOHN DOE")


     """

    can.save()
