#!/usr/bin/env python3
# coding=utf-8

import sys
import requests
sys.path.append('/home/lucas/projects/gupshup_consulta')
import config_gupshup as config

def consultar_saldo():
    response = requests.get('https://api.gupshup.io/sm/api/v2/wallet/balance', headers={'apikey': config.GupshupSaldo.apikey})

    saldo = False
    if response:
        saldo = response.json()['balance'] # {'balance': 41.938, 'status': 'success'}

    return saldo

if __name__ == '__main__':
    print(consultar_saldo())
