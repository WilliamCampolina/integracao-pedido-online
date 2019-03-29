
import datetime
import hashlib
import base64
import requests

"""
Classe para integração com sistema MisterChef

http://tdn.totvs.com/display/public/TChef/API+Pedidos+Online#APIPedidosOnline-Autentica%C3%A7%C3%A3oeToken

"""

HOST = 'http://hchefweb.bematech.com.br/IntegracaoPedidosOnline/'
HHOST = 'http://hchefweb.bematech.com.br/IntegracaoPedidosOnline/'

class GenerateToken:

    def __init__(self, codigo_integracao, chave_cliente):
        self.codigo_integracao = codigo_integracao
        self.chave_cliente = chave_cliente

    def gerarToken(self):
        data = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        token = str(self.codigo_integracao) + str(self.chave_cliente) + data
        token_md5 = hashlib.md5(token.encode('utf-8')).hexdigest()
        token_base64 = base64.urlsafe_b64encode(token_md5.encode('UTF-8')).decode('ascii')
        return 'Basic ' + token_base64


    def send_test(self, token):

        url = HOST + "CadastroService.svc/ObterCardapio"
        datas = {
                   "parametros": {
                      "CodigoEstabelecimento": "96700001",
                      "CodigoIntegracao": 1,
                      "DataAtualizacao": "null"
                   }
                }

        headers = {'Content-type': 'application/json',
                   'Authorization': token
                   }

        rsp = requests.post(url, json=datas, headers=headers)
        dump(rsp)


def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))

if __name__ == '__main__':

    gerador = GenerateToken(codigo_integracao=1,chave_cliente=12345678)
    token = gerador.gerarToken()
    print(token)
    #gerador.send_test(token[0])

