import os
import requests
import traceback
import json
from flask import Flask, request

#Token de parametrização com a API do Facebook Messenger
token = os.environ.get('FB_ACCESS_TOKEN')

app = Flask(__name__)

#Função de bem-vindo
def get_started():
    return {
        "get_started":{
        "payload":" Bem vindo a nossa página de checagem de notícias Fake News!!! Nos envie o título de alguma notícia que você acredita ser fake, que faremos todo o trabalho duro e verificaremos para você :)"
        }
    }

#Função que monta o json de retorno para a API do facebook messenger
def send_text(sender, text):
    return {
        "recipient": {
            "id": sender
        },
        "message": {
            "text": text
        }
    }

#Função que recebe um payload do tipo json, e faz o envio para a API do facebook (Messenger)
def send_message(payload):
    requests.post('https://graph.facebook.com/v5.0/me/messages/?access_token=' + token, json=payload)


#Função que faz uma requisição na API de verificação de checagem e retorna o valor o status da notícia 
def check_fakenews(sender, received_text):
    url_endpoint = 'http://3.233.169.170:3000/rpc/select_fakenews'

    headers = {
        'Content-Type': 'application/json',
        'Prefer': 'params=single-object'
    }

    data = {'titulo' : received_text} 

    r = requests.post(url = url_endpoint, json = data, headers=headers)
    json_data = json.loads(r.text)
    return json_data[0]['checagem']

#Definição das rotas
@app.route('/', methods=['GET', 'POST'])

def webhook():
    if request.method == 'POST':
        try:
            #Valores recebidos pela função POST (Enviada pelo usuário do chat no Messenger)
            data = json.loads(request.data.decode())

            sender = data['entry'][0]['messaging'][0]['sender']['id']
            
            print(data)

            # Action when user first enters the chat
            if 'postback' in data['entry'][0]['messaging'][0]:
 
                welcome = data['entry'][0]['messaging'][0]['postback']['payload']

                #Atribui ao payload de retorno o json
                payload = send_text(sender, welcome)
            
                #Envia o retorno para a API do Facebook
                send_message(payload)
            else:

                text = data['entry'][0]['messaging'][0]['message']['text']

                #Recebe o retorno da função e atribuiu o valor a variável
                message = check_fakenews(sender, text)

                #Atribui ao payload de retorno o json
                payload = send_text(sender, message)
            
                #Envia o retorno para a API do Facebook
                send_message(payload)

        except Exception as e:
            print(traceback.format_exc())
    elif request.method == 'GET': # Para a verificação inicial
        if request.args.get('hub.verify_token') == os.environ.get('FB_VERIFY_TOKEN'):
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Nothing"


if __name__ == '__main__':
    app.run(debug=True)
