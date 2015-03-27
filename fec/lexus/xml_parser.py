# -*- coding: utf-8 -*-
from lxml import etree
from io import StringIO, BytesIO
def parse_voucher(xml):
    """Parse voucher xml"""
    myxml = xml.encode('utf-8')
    comprobante = etree.XML(myxml)
    res = {}
    for element in comprobante:
        res[element.tag] = {}

    for element in comprobante.find('.//infoTributaria'):
        res['infoTributaria'][element.tag] = element.text
    res['detalles'] = []
    for detalle in comprobante.findall('.//detalles/detalle'):
        el = {}
        for e in detalle:
            el[e.tag] = e.text
            if e.tag == 'impuestos':
                el[e.tag] = []
                for i in e:
                    impuestos = {}
                    for i1 in i:
                        impuestos[i1.tag] = i1.text
                el[e.tag].append(impuestos)
        res['detalles'].append(el)
    for element in comprobante.find('.//infoFactura'):
        res['infoFactura'][element.tag] = element.text
        if element.tag == 'totalConImpuestos':
            totalConImpuestos = []
            for i in element:
                tci = {}
                for i1 in i:
                    tci[i1.tag] = i1.text
                totalConImpuestos.append(tci)
            res['infoFactura']['totalConImpuestos'] = totalConImpuestos

    return res

def parse(filename):
    """
    Parse authorized xml file
    """
    res = {}
    tree = etree.parse(filename)
    for element in tree.getroot():
        res[element.tag] = element.text
    return res

if __name__ == '__main__':
    from xreport import generate
    xml = parse('/home/fec/authorized/2103201501099121024500120031030000043555486721312_A.xml')
    dct = parse_voucher(xml['comprobante'])
    generate(dct, 0,
            '/home/fec/authorized/test.pdf')
