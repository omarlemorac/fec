'''
Created on May 26, 2014

@author: marcelo
'''
from flask import Flask,request
app = Flask(__name__)

def do_sign(tagid, filename):
    from file_manager import sign
    sign(tagid, filename)

@app.route("/autorizacion", methods=['GET', 'POST'])
def authorize():
    from file_manager import send2sri
    try:
        send2sri(request.args.get("fn"))
    except Exception,e:
        return str(e)
    return "Autorizando %s" % request.args.get("fn") 

@app.route("/envio", methods=['GET', 'POST'])
def envio():
    if request.method == 'GET' or request.method == 'POST':
        tagid = request.args.get("ti")
        filename = request.args.get("fn")
        do_sign(tagid, filename)
        authorize(filename)
    return "Archivo %s firmado en el nodo %s" % (filename, tagid)
        
if __name__ == '__main__':
    app.run()