
import datetime
import hashlib
import base64
import requests
import json
from decouple import config

"""
Classe para integração com sistema MisterChef

http://tdn.totvs.com/display/public/TChef/API+Pedidos+Online#APIPedidosOnline-Autentica%C3%A7%C3%A3oeToken

"""

HOST = 'http://chefweb.bematech.com.br/IntegracaoPedidosOnline/'
HHOST = 'http://hchefweb.bematech.com.br/IntegracaoPedidosOnline/'

class GenerateToken:

    def __init__(self, codigo_integracao, chave_cliente, codigo_estabelecimento):
        self.codigo_estabelecimento = codigo_estabelecimento
        self.codigo_integracao = codigo_integracao
        self.chave_cliente = chave_cliente

    def gerarToken(self):
        data = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        token = str(self.codigo_integracao) +"|"+ str(self.chave_cliente) +"|"+ data
        print(token)
        token_md5 = hashlib.md5(token.encode('utf-8')).hexdigest()
        token_md5 = data+":"+token_md5
        print(token_md5)
        token_base64 = base64.b64encode(token_md5.encode('UTF-8')).decode('ascii')
        return 'Basic ' + token_base64


    def sendTest(self, token):

        url = HOST + "CadastroService.svc/ObterCardapio"
        datas = "{\n   \"parametros\": {\n      \"CodigoEstabelecimento\": \""+self.codigo_estabelecimento +"\",\n      \"CodigoIntegracao\": 1\n   }\n}"

        headers = {
            'authorization': token,
            'content-type': "application/json",
            'cache-control': "no-cache",
        }

        rsp = requests.post(url, data=datas, headers=headers)
        print(rsp.json())


if __name__ == '__main__':

    gerador = GenerateToken(codigo_integracao=1,chave_cliente=config('KEY'), codigo_estabelecimento=config('ESTABELECIMENTO'))
    token = gerador.gerarToken()
    print(token)

    gerador.sendTest(token)


