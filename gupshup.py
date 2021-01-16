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
version: 1.2           .-'---------|
                      ( C|/\/\/\/\/|
                       '-./\/\/\/\/|
                         '_________'
                          '-------'
"""
# TODO
# > enviar email quando detectar que houve uma recarga
# > proper logging
#

import os
import sys
import typer
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser
from ruamel.yaml import YAML

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_PATH)
from gupshup_api_saldo import consultar_saldo
import config_gupshup as config
import textos_gupshup as textos


def main(modo: str, destino: str = ""):
    """
    Argumento obrigatório: Modo [saldo_check | saldo_atual]\n
        saldo_check -> consulta o saldo atual e envia um email informando o saldo caso esteja baixo (<10).\n
        saldo_atual -> consulta o saldo atual e envia por email.\n    
    Argumento Opcional: destino [email]
    """

    email_remetente = config.Email.cgr[0]
    password = config.Email.cgr[1]
    email_destino = destino if destino else config.Email.adriana[0]

    yaml = YAML(typ='safe')
    config_file = f'{BASE_PATH}/config_verificar_envio.yaml'
    with open(config_file, 'r') as cfg:
        yaml_cfg = yaml.load(cfg)
    email_enviado = yaml_cfg['email']['email_saldo_baixo_enviado']

    saldo = consultar_saldo()
    respostas = textos.Resposta(saldo)
    if saldo: # consutar_saldo retorna o saldo, ou False
        #if sys.argv[1] == "saldo_check":
        if modo == "saldo_check":
            if saldo > 10:
                print(f"saldo suficiente: {saldo:2f}")
                # quando o saldo fica baixo, é enviado um email avisando.
                # a variável "email_enviado" é usada pra controlar esse
                # envio, para não ficar enviando constantemente email até
                # que seja colocado crédito e o saldo voltar ao normal.
                if email_enviado == 's': # email avisando o saldo baixo foi enviado
                    # resetar o email_enviado pra n[ão], e talvez enviar um email avisando o novo saldo
                    print("Email já foi enviado informando o saldo baixo, e já foi recarregado o saldo! Zerando a informação de envio de email.")
                    with open(config_file, 'w') as arquivo:
                        enviado = ['email']['email_saldo_baixo_enviado'] = 'n'
                        yaml.dump(enviado, arquivo)
                        # enviar o email aqui avisando o novo saldo
                # se email_enviado não for 's'[im], é só sair e ignorar.
                sys.exit()
            print(f"saldo baixo: {saldo:2f}")
            # de cara é necessário conferir se o email já foi enviado,
            # para não ficar enviando constantemente. além disso, tem que
            # verificar em ambas condições (aqui e acima) para dar tempo
            # do responsável colocar crédito e isso não afetar o
            # funcionamento do script.
            if email_enviado == 's':
                # se já foi enviado, pode sair...
                # caso contrário, só continuar o script pra criar a
                # a mensagem e enviar o email.
                print("Email já foi enviado informando o saldo baixo!")
                sys.exit()
            message = MIMEMultipart("alternative")
            message["Subject"] = "Saldo BAIXO no Gupshup"
            message["From"] = email_remetente
            message["To"] = email_destino

            # Criar as versões texto e html da mensagem
            text = respostas.saldo_baixo
            html = respostas.saldo_baixo_html

            # Tornar esses em objetos plain/html MIMEText
            part1 = MIMEText(text, "plain", "utf-8")
            part2 = MIMEText(html, "html")

            # Adiciona as partes HTML/plain-text à mensagem MIMEMultipart
            # obs: O client de email vai tentar renderizar a última primeiro,
            # logo é importante colocar o html por último. Se por um acaso
            # o client não tiver suporte para html (raro hoje em dia), ele
            # vai tentar ler a outra parte, que é texto normal. A vantágem
            # de html é poder colocar itálico, negrito, etc.
            message.attach(part1)
            message.attach(part2)
            with open(config_file, 'w') as arquivo:
                conf['email']['email_saldo_baixo_enviado'] = 's'
                conf.write(arquivo)

        elif sys.argv[1] == "saldo_atual":
            message = MIMEMultipart("alternative")
            message["Subject"] = "Saldo ATUAL no Gupshup"
            message["From"] = email_remetente
            message["To"] = email_destino

            # Criar as versões texto e html da mensagem
            text = respostas.saldo_atual
            html = respostas.saldo_atual_html

            part1 = MIMEText(text, "plain", "utf-8")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)

        else:
            print("Não entendi. Favor tentar novamente com um dos parâmetros obrigatórios: saldo_atual ou saldo_check")
            sys.exit()

        # Cria um contexto SSL
        contexto = ssl._create_unverified_context()
        porta = 465  # pro SSL
        with smtplib.SMTP_SSL(host="smtp.quick.com.br", port=porta, context=contexto) as server:
            server.login(email_remetente, password)
            server.sendmail(email_remetente, email_destino, message.as_string())
            print(f"Email enviado de {email_remetente} para {email_destino}")

    else:
        print("Não houve retorno na consulta do saldo do gupshup. Entre em contato com o Lucas (lucasrabraao@gmail.com) para verificar.")

if __name__ == "__main__":
    typer.run(main)
