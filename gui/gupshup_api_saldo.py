#!/usr/bin/env python3
# coding=utf-8

import os
import sys
import requests

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
import config_gupshup as cfg

def consultar_saldo():
    response = requests.get('https://api.gupshup.io/sm/api/v2/wallet/balance', headers={'apikey': cfg.GupshupSaldo.apikey})

    saldo = False
    if response:
        saldo = response.json()['balance'] # {'balance': 41.938, 'status': 'success'}

    return saldo

if __name__ == '__main__':
    print(consultar_saldo())
