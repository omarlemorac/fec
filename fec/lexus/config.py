'''
Created on May 24, 2014

@author: marcelo
'''


signed_docs_folder="/home/fec/signed/"
temp_folder="/home/fec/signed/"
unsigned_docs_folder="/home/fec/unsigned/"
authorized_docs_folder="/home/fec/authorized/"
rejected_docs_folder="/home/fec/rejected/"
deliver_url="https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantes?wsdl"
deliver_batch_url="https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionLoteMasivo?wsdl"
authorization_url="https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantes?wsdl"
time_out=10
mysql_config = {
  'user': 'fcec2013_factele',
  'password': 'fcec2014$#',
  'host': '192.254.250.165',
  'database': 'fcec2013_facturae',
  'raise_on_warnings': False,
}

couchdb_config = {
        'user':'fullcarga',
        'password':'fullcarga',
        'doc_db':'fc_db',
        'host':'http://fullcarga:fullcarga@127.0.0.1:5984'
        }
