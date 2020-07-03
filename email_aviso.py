#!/usr/bin/env python3
#coding=utf-8
"""
Esse script realiza a consulta de saldo disponível
no gupshup para informar através de email. Eu uso
ele em um servidor linux com 2 cron jobs. 1 usa o
argumento "saldo_check" para verificar a cada 15
minutos o saldo disponível, e enviar um email com
mensagem personalizada caso esteja abaixo da média.
O outro usa o argumento "saldo_atual" para enviar
um email toda segunda feira às 9h a informação.
                             } (
Author: Lucas Rocha Abraão  (   ) )
Date: 02/07/2020             ) { (
License: GNU GPLv3        ___|___)_
                       .-'---------|
                      ( C|/\/\/\/\/|
                       '-./\/\/\/\/|
                         '_________'
                          '-------'
"""

import sys
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser
from gupshup_api_saldo import consultar_saldo
import config

email_conf = config.Email
my_email = email_conf.cgr[0]
password = email_conf.cgr[1]
email_destino = email_conf.lucas[0]

saldo = consultar_saldo()

if saldo: # consutar_saldo retorna o saldo, ou False
    if sys.argv[1] == "saldo_check":
        if saldo > 10:
            sys.exit()
        message = MIMEMultipart("alternative")
        message["Subject"] = "Saldo BAIXO no Gupshup"
        message["From"] = my_email
        message["To"] = email_destino

        # Criar as versões texto e html da mensagem
        text = f"""\
        Foi detectado saldo baixo no Gupshup.
        Saldo atual: {saldo}.
        """
        html = f"""\
        <html>
        <body>
            <p>Olá,<br>
            Foi detectado <i>saldo baixo</i> no Gupshup.<br>
            Saldo atual: <b><mark>{saldo}</mark></b>
            </p>
        </body>
        </html>
        """

        # Tornar esses em objetos plain/html MIMEText
        part1 = MIMEText(text, "plain", "utf-8")
        part2 = MIMEText(html, "html")

        # Adiciona as partes HTML/plain-text à mensagem MIMEMultipart
        # obs: O client de email vai tentar renderizar a última primeiro,
        # logo é importante colocar o html pro último. Se por um acaso
        # o client não tiver suporte para html (raro hoje em dia), ele
        # vai tentar ler a outra parte, que é texto normal. A vantágem
        # de html é poder colocar itálico, negrito, etc.
        message.attach(part1)
        message.attach(part2)

    elif sys.argv[1] == "saldo_atual":
        message = MIMEMultipart("alternative")
        message["Subject"] = "Saldo ATUAL no Gupshup"
        message["From"] = my_email
        message["To"] = email_destino

        # Criar as versões texto e html da mensagem
        text = f"""\
        Atualmente o saldo no gupshup é de {saldo} mensagens.
        """
        html = f"""\
        <html>
        <body>
            <p>Olá,<br>
            Atualmente o saldo no gupshup é de <b><mark>{saldo}</mark></b> mensagens.
            </p>
        </body>
        </html>
        """

        part1 = MIMEText(text, "plain", "utf-8")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        
    # Cria um contexto SSL seguro
    contexto = ssl.create_default_context()
    porta = 465  # pro SSL
    with smtplib.SMTP_SSL("smtp.gmail.com", porta, context=contexto) as server:
        server.login(my_email, password)
        server.sendmail(my_email, email_destino, message.as_string())

else:
    print("Não houve retorno na consulta do saldo do gupshup")