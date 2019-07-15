# Código inspirado pelo vídeo "Build A Python App That Tracks Amazon Prices!" por dev ed
# Modificado para rastrear preços do site https://zoom.com.br, não testado com outros sites
# Recebe duas entradas: O link (que deve ser colado corretamente) e o valor que deseja alcançar (Parte adicional ao vídeo). O valor é atualizado a cada 10min

import requests
from bs4 import BeautifulSoup
import smtplib
from time import sleep
from validators import url

#Função que valida que o valor inserido é válido
def valida_preco(n):
    if not n.isdigit():
        try:
            valor = float(n)
        except ValueError:
            return False

    elif float(n) <= 0:
        return False
    else:
        return True

URL = input("Cole o link\n")

while not url(URL):                 #Verifica se o link é válido
    print('Email inválido')
    URL = input("Cole o link\n")

valor = input('Insira o preço alvo: ')

while not valida_preco(valor):
    print('\nO valor inserido é inválido!')
    valor = input('Insira o preço alvo: ')
valor = float(valor)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36 OPR/62.0.3331.18'
}

#função que checa se o valor foi atualizado
def check_price(URL):
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(attrs="product-name").get_text()
    price  = soup.find(attrs="price").get_text()
    converted_price = price.strip().split(',')[0][3:]
    converted_price = float(''.join(converted_price.split('.')))

    print(f"Preço atual: {price.strip()}")

    if converted_price < valor:
        send_mail()

#função que envia para o email
def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('andersonfelipecarvalho60@gmail.com', 'lwqudwkpxoquycrd')

    subject = 'O preco abaixou!'
    body = URL

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'andersonfelipecarvalho60@gmail.com',
        'andersonfelipe01@live.com',
        msg
    )
    print("Email enviado com sucesso!")

#checa o preço infinitamente
while True:
    check_price(URL)
    sleep(600)          #10 minutos para rodar o while novamente