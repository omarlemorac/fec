'''
Created on May 24, 2014

@author: marcelo
'''


#Windows
signed_docs_folder="C:\\ISOFTEC\\CELECTRONICOS\\DOC_FIRMADOS"
temp_folder="C:\\ISOFTEC\\CELECTRONICOS\\MASIVO_NO_AUTORIZADOS"
unsigned_docs_folder="C:\\ISOFTEC\\CELECTRONICOS\\DOC_GENERADOS"
authorized_docs_folder="C:\\ISOFTEC\\CELECTRONICOS\\DOC_AUTORIZADOS"
rejected_docs_folder="C:\\ISOFTEC\\CELECTRONICOS\\DOC_FIRMADOS\\rechazados"
deliver_url="https://cel.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantes?wsdl"
deliver_batch_url="https://cel.sri.gob.ec/comprobantes-electronicos-ws/RecepcionLoteMasivo?wsdl"
authorization_url="https://cel.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantes?wsdl"
time_out=10
mysql_config = {
  'user': 'fcec2013_factele',
  'password': 'fcec2014$#',
  'host': '192.254.250.165',
  'database': 'fcec2013_facturae',
  'raise_on_warnings': False,
}

