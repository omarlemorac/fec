# -*- coding: utf-8 -*-

def write_invoice_codepret(args):
    from lexus_model import model as M
    statement = """
    EXEC SRI$SIMP_FACXML_FEV110 @WCIAS='{cias}',@WUOCI='{uoci}',
    @WTPDC='{wtpdc}',@WSERIE='{wserie}',@WNRODOC='{wnrodoc}',@user = 'sa',
    @pwd = 'Codepret2010',@servidor = 'SERAPL\CODEPRET',
    @BddNombre='ISOFTEC_CDP',
    @RutaXml = 'C:\ISOFTEC\CELECTRONICOS\DOC_GENERADOS',@UserLogin = 'WILMERO'
    """

    sql = statement.format(**args)
    m = M()
    return '\n'.join([r[0] for r in m.read(sql).fetchall()])

def write_invoice(company, args):
    if company == 'codepret':
        return write_invoice_codepret(args)
    else:
        return None

