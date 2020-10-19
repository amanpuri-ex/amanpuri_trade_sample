#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from client import Client

client = Client(
        os.environ['AMANPURI_API_KEY'],
        os.environ['AMANPURI_SECRET_KEY']
    )

# API Document
# https://api.amanpuri.io/api/docs/#info

print('get_margin_indices_active')
print(client.get_margin_indices_active().json())
print('get_margin_instrumentpython_by_symbol')
print(client.get_margin_instrument_by_symbol(order_id='btcusd').json())
print('get_margin_positions')
print(client.get_margin_positions().json())

print('create_limit_order')
print(client.get_margin_create_order(instrument_symbol='BTCUSD', side='buy', type='limit', quantity=1, leverage=1, price='1000', time_in_force='gtc').json())
print(client.get_margin_create_order(instrument_symbol='BTCUSD', side='sell', type='limit', quantity=1, leverage=1, price='20000', time_in_force='gtc').json())
print('create_market_order')
print(client.get_margin_create_order(instrument_symbol='BTCUSD', side='buy', type='market', quantity=1, leverage=1, time_in_force='gtc').json())
print('cancel_order')
#print(client.get_margin_cancel_order(id='179496999').json())
