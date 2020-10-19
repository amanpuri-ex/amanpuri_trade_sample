import requests
from helpers import *
import hmac
import hashlib
import binascii
from urllib.parse import urlparse


class Client(object):

    def __init__(self, api_key='', secret=''):
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': '',
        }

        self.api_key = api_key
        self.secret = secret

    def get_signature(self, method, url, params):
        array_params = []
        for attr in params:
            array_params.append("{key}={value}".format(key=attr, value=params[attr]))
        path = url.replace(BASE_URL, '')
        message = '{method} {path}?{params}'.format(method=method, path=path, params='&'.join(array_params))

        return hmac.new(bytes(self.secret, 'latin-1'), bytes(message, 'latin-1'), hashlib.sha256).hexdigest()

    def private_request(self, url, method, data):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'APIKEY': self.api_key,
        }
        print(headers)
        signature = self.get_signature(method, url, data)
        data['signature'] = signature
        print(data)
        if method == 'GET':
            return requests.get(url, params=data, headers=headers)
        if method == 'POST' or method == 'PUT':
            return requests.post(url, json=data, headers=headers)

    # SPOT EXCHANGE TRADING API
    def get_price_scope(self, **kwargs):
        ''' [Public] Price Scope
        :param coin : required
        :type coin : str
        :description coin : The coin name, ex: eth.
        :param currency : required
        :type currency : str
        :description currency : The currency name, ex: btc.
        :returns: Price Scope
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "c4c5e35f610222a9cd29d500356e4b790cf21642",
                "data": {
                    "current_price": "0.0468648224",
                    "changed_percent": "0",
                    "max_price": "0.0468648224",
                    "min_price": "0.0468648224",
                    "volume": 0,
                    "previous_price": "0.0468648224",
                    "currency": "btc",
                    "coin": "eth"
                }
            }
        '''

        return requests.get(get_price_scope_url(), params=kwargs, headers=self.headers)

    def get_order_books(self, **kwargs):
        ''' [Public] Get Order books
            :param currency : required
            :type currency : string
            :description currency : currency name
            :param coin : required
            :type coin : string
            :description coin : coin name
            :param tickerSize : required
            :type tickerSize : decimal
            :description tickerSize : ticker size
            :returns: Order books
            :response
                {
                    "success": true,
                    "message": null,
                    "dataVersion": "c4c5e35f610222a9cd29d500356e4b790cf21642",
                    "data": {
                        "buy": [],
                        "sell": [],
                        "updatedAt": {
                            "date": "2019-10-14 07:10:33.145224",
                            "timezone_type": 3,
                            "timezone": "UTC"
                        },
                        "meta": {
                            "buy": {
                                "min": 0,
                                "max": 9223372036854775807
                            },
                            "sell": {
                                "min": 0,
                                "max": 9223372036854775807
                            }
                        },
                        "currency": null,
                        "coin": null,
                        "tickerSize": null
                    }
                }
        '''

        return requests.get(get_order_books_url(), params=kwargs, headers=self.headers)

    def get_market_recent_trades(self, **kwargs):
        ''' [Public] Get Market Recent Trades
        :param currency : optional
        :type currency : str
        :description currency : currency name
        :param coin : optional
        :type coin : str
        :description coin : coin name
        :param count : optional
        :type count : str
        :description count : count transactions
        :returns: Market Recent Trades
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "c4c5e35f610222a9cd29d500356e4b790cf21642",
                "data": []
            }
        '''

        return requests.get(get_market_recent_trades_url(), params=kwargs, headers=self.headers)

    def get_auth_token(self, **kwargs):
        ''' get auth token
        :param client_id : required
        :type client_id : string
        :description client_id : client id
        :param client_secret : required
        :type client_secret : string
        :description client_secret : private key
        :param grant_type : required
        :type grant_type : string
        :description grant_type : grant type login
        :param scope : optional
        :type scope : string
        :description scope : optional authorization login
        :param username : required
        :type username : string
        :description username : username
        :param password : required
        :type password : string
        :description password : password
        :param otp : optional
        :type otp : string
        :description otp : This is required if enable google otp
        :returns: Gen Auth Token
        :response
            {
                "token_type": "Bearer",
                "expires_in": 1800,
                "access_token": "xxx",
                "refresh_token": "xxx"
            }
        '''

        return requests.post(get_auth_token_url(), json=kwargs)

    def get_order_transaction_latest(self, **kwargs):
        ''' [Public] Order Transaction Latest
        :param currency : optional
        :type currency : str
        :description currency : The currency name.
        :param coin : optional
        :type coin : str
        :description coin : The coin name.
        :returns: Order Transaction Latest
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "xxx",
                "data": null
            }
        '''
        return requests.get(get_order_transaction_latest_url(), params=kwargs, headers=self.headers)

    def get_cancel_all_order(self, **kwargs):
        ''' [Private] Cancel All Order
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "xxxx",
                "data": null
            }
        '''

        return self.private_request(get_cancel_all_order_url(), 'PUT', kwargs)

    def get_cancel_by_type(self, **kwargs):
        ''' [Private] Cancel By Type
        :param type : optional
        :type type : str
        :description type : The type(limit or market)
        :returns: Cancel By Type
        :response
        {
            "success": true,
            "message": null,
            "dataVersion": "xxx",
            "data": null
        }
        '''

        return self.private_request(get_cancel_by_type_url(), 'PUT', kwargs)

    def get_cancel_a_order(self, order_id, **kwargs):
        ''' get cancel a order
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "xxxx",
                "data": null
            }
        '''

        return self.private_request(get_cancel_a_order_url(order_id), 'PUT', kwargs)

    def get_user_order_history(self, **kwargs):
        ''' get user order history
        :param page : optional
        :type page : str
        :description page : current page
        :param limit : optional
        :type limit : str
        :description limit : number items of per page
        :returns: user order history
        :response
        {
            "success": true,
            "message": null,
            "dataVersion": "xxx",
            "data": [
                {
                    "created_at": 1567043630932,
                    "price": "0.0468640000",
                    "quantity": "3.9940000000",
                    "transaction_type": "sell"
                },
                {
                    "created_at": 1567043630932,
                    "price": "0.0468640000",
                    "quantity": "3.9940000000",
                    "transaction_type": "sell"
                }
            ]
        }
        '''

        return self.private_request(get_user_order_history_url(), 'GET', kwargs)

    def get_user_opening_orders(self, **kwargs):
        ''' get user opening orders
        :param coin : optional
        :type coin : str
        :description coin : string optional coin name.
        
        :param currency : optional
        :type currency : str
        :description currency : string optional currency name.
        
        :param page : optional
        :type page : str
        :description page : int optional.
        
        :param limit : optional
        :type limit : str
        :description limit : int optional
        :returns: user opening orders
        :response
        {
            "success": true,
            "message": "Jessica Jones",
            "dataVersion": "6e7a7795297cdc4222ecb77463a7e83638d3f33f",
            "data": {
                "current_page": 1,
                "data": [
                    {
                        "id": 708,
                        "original_id": null,
                        "user_id": 2,
                        "email": "bot2@gmail.com",
                        "trade_type": "sell",
                        "currency": "usd",
                        "coin": "ltc",
                        "type": "limit",
                        "ioc": null,
                        "quantity": "100.0000000000",
                        "price": "2.0000000000",
                        "executed_quantity": "0.0000000000",
                        "executed_price": "0.0000000000",
                        "base_price": null,
                        "stop_condition": null,
                        "fee": "0.0000000000",
                        "status": "pending",
                        "created_at": 1567150919521,
                        "updated_at": 1567150919521,
                        "total": "200.00000000000000000000"
                    }
                ],
                "first_page_url": "http:\/\/localhost:8001\/api\/v1\/orders\/pending?page=1",
                "from": null,
                "last_page": 1,
                "last_page_url": "http:\/\/localhost:8001\/api\/v1\/orders\/pending?page=1",
                "next_page_url": null,
                "path": "http:\/\/localhost:8001\/api\/v1\/orders\/pending",
                "per_page": "10",
                "prev_page_url": null,
                "to": null,
                "total": 2
            }
        }
        '''

        return self.private_request(get_user_opening_orders_url(), 'GET', kwargs)

    def get_all_user_opening_orders(self, **kwargs):
        ''' get all user opening orders
        :param coin : optional
        :type coin : str
        :description coin : string optional coin name.
        :param currency : optional
        :type currency : str
        :description currency : string optional currency name.
        :returns: user opening orders
        :response
        {
            "success": true,
            "message": "Jessica Jones",
            "dataVersion": "6e7a7795297cdc4222ecb77463a7e83638d3f33f",
            "data": [
                {
                    "id": 708,
                    "original_id": null,
                    "user_id": 2,
                    "email": "bot2@gmail.com",
                    "trade_type": "sell",
                    "currency": "usd",
                    "coin": "ltc",
                    "type": "limit",
                    "ioc": null,
                    "quantity": "100.0000000000",
                    "price": "2.0000000000",
                    "executed_quantity": "0.0000000000",
                    "executed_price": "0.0000000000",
                    "base_price": null,
                    "stop_condition": null,
                    "fee": "0.0000000000",
                    "status": "pending",
                    "created_at": 1567150919521,
                    "updated_at": 1567150919521,
                    "total": "200.00000000000000000000"
                }
            ]
        }
        '''

        return self.private_request(get_all_user_opening_orders_url(), 'GET', kwargs)

    def create_order(self, **kwargs):
        ''' create order
        :param coin : required
        :type coin : string
        :description coin : coin name.
        :param currency : required
        :type currency : string
        :description currency : currency name.
        :param price : required
        :type price : decimal
        :description price : price
        :param quantity : required
        :type quantity : integer
        :description quantity : quantity.
        :param trade_type : required
        :type trade_type : string
        :description trade_type : trade type(buy, sell).
        :returns: order
        :response
        {
            "success": true,
            "message": null,
            "dataVersion": "6e7a7795297cdc4222ecb77463a7e83638d3f33f",
            "data": {
                "id": 1,
                "original_id": null,
                "user_id": 1,
                "email": "bot1@gmail.com",
                "trade_type": "buy",
                "currency": "btc",
                "coin": "eth",
                "type": "limit",
                "ioc": null,
                "quantity": "1222.0000000000",
                "price": "0.0468640000",
                "executed_quantity": "46.9910000000",
                "executed_price": "0.0468640000",
                "base_price": null,
                "stop_condition": null,
                "fee": "0.0704865000",
                "status": "pending",
                "created_at": 1566440661180,
                "updated_at": 1566440661180
            }
        }
        '''

        return self.private_request(get_create_order_url(), 'POST', kwargs)

    def get_user_trading_history(self, **kwargs):
        ''' get user trading history
        :param page : optional
        :type page : str
        :description page : current page
        :param limit : optional
        :type limit : str
        :description limit : number items of per page
        :returns: user trading history
        :response
        {
            "success": true,
            "message": null,
            "dataVersion": "6e7a7795297cdc4222ecb77463a7e83638d3f33f",
            "data": {
                "current_page": 1,
                "data": [
                    {
                        "trade_type": "sell",
                        "fee": "0.0400000000",
                        "created_at": 1567154633635,
                        "currency": "btc",
                        "coin": "eos",
                        "price": "5.0000000000",
                        "quantity": "4.0000000000",
                        "amount": "20.0000000000"
                    },
                    {
                        "trade_type": "sell",
                        "fee": "0.0400000000",
                        "created_at": 1567154633635,
                        "currency": "btc",
                        "coin": "eos",
                        "price": "5.0000000000",
                        "quantity": "4.0000000000",
                        "amount": "20.0000000000"
                    }
                ],
                "first_page_url": "http:\/\/localhost:8001\/api\/v1\/orders\/trading-histories?page=1",
                "from": null,
                "last_page": 1,
                "last_page_url": "http:\/\/localhost:8001\/api\/v1\/orders\/trading-histories?page=1",
                "next_page_url": null,
                "path": "http:\/\/localhost:8001\/api\/v1\/orders\/trading-histories",
                "per_page": "10",
                "prev_page_url": null,
                "to": null,
                "total": 2
            }
        }
        '''

        return self.private_request(get_user_trading_history_url(), 'GET', kwargs)

    def get_my_trade_history(self, **kwargs):
        ''' get my trade history
        :param symbol : required
        :type symbol : str
        :description symbol : The coin name - currency name, ex: xrp-btc.
        
        :param startDate : required
        :type startDate : str
        :description startDate : The start date, ex: 2018-09-10 00:00:00.
        
        :param endDate : optional
        :type endDate : str
        :description endDate : optional The end date, ex: 2020-09-20 00:00:00 .
        
        :param page : optional
        :type page : str
        :description page : optional The page, ex: 1 .
        
        :param limit : optional
        :type limit : str
        :description limit : optional The limit per page(default is 10), ex: 10 
        
        :returns: my trade history
        :response
        {
            "success": true,
            "message": null,
            "dataVersion": "c4c5e35f610222a9cd29d500356e4b790cf21642",
            "data": {
                "status": true,
                "total": 0,
                "last_page": 1,
                "per_page": "10",
                "current_page": 1,
                "next_page_url": null,
                "prev_page_url": null,
                "from": 1,
                "to": 0,
                "data": []
            }
        }
        '''

        return self.private_request(get_my_trade_history_url(), 'GET', kwargs)

    def get_margin_positions(self, **kwargs):
        
        return self.private_request(get_margin_positions(), 'GET', kwargs)

    def get_margin_balance(self, **kwargs):
        
        return self.private_request(get_margin_balance(), 'GET', kwargs)
        
    def get_trades_by_order_id(self, order_id, **kwargs):
        ''' get trades by order id
        
        :returns: trades
        :response
        {
            "success": true,
            "message": null,
            "dataVersion": "c4c5e35f610222a9cd29d500356e4b790cf21642",
            "data": {
                "status": true,
                "total": 0,
                "last_page": 1,
                "per_page": 15,
                "current_page": 1,
                "next_page_url": null,
                "prev_page_url": null,
                "from": 1,
                "to": 0,
                "data": []
            }
        }
        '''

        return self.private_request(get_trades_by_order_id_url(order_id), 'GET', kwargs)

    # MARGIN EXCHANGE TRADING API
    def get_margin_instruments(self, **kwargs):
        ''' [Public] Get all instruments
        :returns: trades
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": [
                    {
                        "id": 4,
                        "symbol": "ETHUSD",
                        "root_symbol": "ETH",
                        "state": "Open",
                        "type": 2,
                        "expiry": null,
                        "base_underlying": "ETH",
                        "quote_currency": "USD",
                        "underlying_symbol": "ETH",
                        "settle_currency": "BTC",
                        "init_margin": "0.0200000000",
                        "maint_margin": "0.0100000000",
                        "deleverageable": 1,
                        "maker_fee": "-0.0002500000",
                        "taker_fee": "0.0007500000",
                        "settlement_fee": "0.0000000000",
                        "has_liquidity": 1,
                        "reference_index": "ETH",
                        "settlement_index": null,
                        "funding_base_index": "ETHBON8H",
                        "funding_quote_index": "USDBON8H",
                        "funding_premium_index": "ETHUSDPI8H",
                        "funding_interval": 8,
                        "tick_size": "0.0500000000",
                        "max_price": "1000000.0000000000",
                        "max_order_qty": 10000000,
                        "multiplier": "0.0000010000",
                        "option_strike_price": "0.0000000000",
                        "option_ko_price": "0.0000000000",
                        "risk_limit": "50.00000000",
                        "risk_step": "50.00000000",
                        "created_at": "2019-07-11 07:14:23",
                        "updated_at": "2019-07-11 07:14:23",
                        "extra": {
                            "id": 4,
                            "symbol": "ETHUSD",
                            "impact_bid_price": "0.0000000000",
                            "impact_mid_price": "0.0000000000",
                            "impact_ask_price": "0.0000000000",
                            "fair_basis_rate": "-0.007500000000000",
                            "fair_basis": "-0.521977526973839",
                            "fair_price": "133.246956241026161",
                            "mark_price": "133.246956241026161",
                            "funding_timestamp": "2019-12-23 08:00:00",
                            "funding_rate": "-0.0075000000",
                            "indicative_funding_rate": "0.0000000000",
                            "last_price": "0.3000000000",
                            "last_price_24h": "100.0000000000",
                            "ask_price": null,
                            "bid_price": null,
                            "mid_price": null,
                            "trade_reported_at": "2019-12-12",
                            "max_value_24h": "223.0000000000",
                            "min_value_24h": "0.3000000000",
                            "total_turnover_24h": "0.0410033500",
                            "total_volume_24h": "2057.0000000000",
                            "total_volume": "2631275.00",
                            "created_at": null,
                            "updated_at": "2019-12-23 03:50:15"
                        },
                        "open_value": "0.294841940241950",
                        "open_interest": "5209"
                    }
                ]
            }
        '''

        return requests.get(get_margin_instruments_url(), params=kwargs, headers=self.headers)

    def get_margin_active_instruments(self, **kwargs):
        ''' [Public] Get all active instruments
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": [
                    {
                        "id": 4,
                        "symbol": "ETHUSD",
                        "root_symbol": "ETH",
                        "state": "Open",
                        "type": 2,
                        "expiry": null,
                        "base_underlying": "ETH",
                        "quote_currency": "USD",
                        "underlying_symbol": "ETH",
                        "settle_currency": "BTC",
                        "init_margin": "0.0200000000",
                        "maint_margin": "0.0100000000",
                        "deleverageable": 1,
                        "maker_fee": "-0.0002500000",
                        "taker_fee": "0.0007500000",
                        "settlement_fee": "0.0000000000",
                        "has_liquidity": 1,
                        "reference_index": "ETH",
                        "settlement_index": null,
                        "funding_base_index": "ETHBON8H",
                        "funding_quote_index": "USDBON8H",
                        "funding_premium_index": "ETHUSDPI8H",
                        "funding_interval": 8,
                        "tick_size": "0.0500000000",
                        "max_price": "1000000.0000000000",
                        "max_order_qty": 10000000,
                        "multiplier": "0.0000010000",
                        "option_strike_price": "0.0000000000",
                        "option_ko_price": "0.0000000000",
                        "risk_limit": "50.00000000",
                        "risk_step": "50.00000000",
                        "created_at": "2019-07-11 07:14:23",
                        "updated_at": "2019-07-11 07:14:23",
                        "extra": {
                            "id": 4,
                            "symbol": "ETHUSD",
                            "impact_bid_price": "0.0000000000",
                            "impact_mid_price": "0.0000000000",
                            "impact_ask_price": "0.0000000000",
                            "fair_basis_rate": "-0.007500000000000",
                            "fair_basis": "-0.521977526973839",
                            "fair_price": "133.246956241026161",
                            "mark_price": "133.246956241026161",
                            "funding_timestamp": "2019-12-23 08:00:00",
                            "funding_rate": "-0.0075000000",
                            "indicative_funding_rate": "0.0000000000",
                            "last_price": "0.3000000000",
                            "last_price_24h": "100.0000000000",
                            "ask_price": null,
                            "bid_price": null,
                            "mid_price": null,
                            "trade_reported_at": "2019-12-12",
                            "max_value_24h": "223.0000000000",
                            "min_value_24h": "0.3000000000",
                            "total_turnover_24h": "0.0410033500",
                            "total_volume_24h": "2057.0000000000",
                            "total_volume": "2631275.00",
                            "created_at": null,
                            "updated_at": "2019-12-23 03:50:15"
                        },
                        "open_value": "0.294841940241950",
                        "open_interest": "5209"
                    }
                ]
            }
        '''
        return requests.get(get_margin_active_instruments_url(), params=kwargs, headers=self.headers)

    def get_margin_indices_by_symbol(self, order_id, **kwargs):
        ''' [Public] Get indices by symbol
        :param symbol : optional
        :type symbol : str
        :description symbol : string required symbol name.
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": []
            }
        '''
        return requests.get(get_margin_indices_url(order_id), params=kwargs, headers=self.headers)

    def get_margin_indices_active(self, **kwargs):
        ''' [Public] Get lastest indices of all symbol
        :response
        {
            "success": true,
            "message": null,
            "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
            "data": [
                        {
                            "id": 1,
                            "symbol": "BTC",
                            "root_symbol": "BTC",
                            "status": "active",
                            "type": "ami",
                            "precision": "8",
                            "value": "7573.4800000000",
                            "constance_value": "0.0000000000",
                            "previous_value": "7598.7680000000",
                            "previous_24h_value": "6734.7300000000",
                            "is_index_price": 1,
                            "reference_symbol": "BTC",
                            "created_at": "2019-09-04 02:07:17",
                            "updated_at": "2019-12-23 03:50:15"
                        }
                    ]
                }
        '''
        return requests.get(get_margin_indices_active_url(), params=kwargs, headers=self.headers)

    def get_margin_risk_limit_list(self, **kwargs):
        ''' [Public] Get risk limit list of an instrument
        :param symbol : required
        :type symbol : str
        :description symbol : string required symbol name.
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": [
                    {
                        "riskLimit": "200",
                        "initMargin": "0.01",
                        "maintMargin": "0.005"
                    }
                ]
            }
        '''
        return requests.get(get_margin_risk_limit_list_url(), params=kwargs, headers=self.headers)

    def get_margin_instrument_by_symbol(self, order_id, **kwargs):
        ''' [Public] Get an instrument by symbol
        :param symbol : required
        :type symbol : str
        :description symbol : string required symbol name.
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": null
            }
        '''
        return requests.get(get_margin_instrument_url(order_id), params=kwargs, headers=self.headers)

    def get_margin_settlement_history(self, **kwargs):
        ''' [Public] Get all settlement history
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": {
                    "current_page": 1,
                    "data": [],
                    "first_page_url": "http:\/\/localhost\/api\/v1\/margin\/settlement?page=1",
                    "from": null,
                    "last_page": 1,
                    "last_page_url": "http:\/\/localhost\/api\/v1\/margin\/settlement?page=1",
                    "next_page_url": null,
                    "path": "http:\/\/localhost\/api\/v1\/margin\/settlement",
                    "per_page": 10,
                    "prev_page_url": null,
                    "to": null,
                    "total": 0
                }
            }
        '''
        return requests.get(get_margin_settlement_history_url(), params=kwargs, headers=self.headers)

    def get_margin_insurance_history(self, **kwargs):
        ''' [Public] Get all insurance history
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": {
                    "current_page": 1,
                    "data": [],
                    "first_page_url": "http:\/\/localhost\/api\/v1\/margin\/insurance?page=1",
                    "from": null,
                    "last_page": 1,
                    "last_page_url": "http:\/\/localhost\/api\/v1\/margin\/insurance?page=1",
                    "next_page_url": null,
                    "path": "http:\/\/localhost\/api\/v1\/margin\/insurance",
                    "per_page": 10,
                    "prev_page_url": null,
                    "to": null,
                    "total": 0
                }
            }
        '''
        return requests.get(get_margin_insurance_history_url(), params=kwargs, headers=self.headers)

    def get_margin_composite_index(self, **kwargs):
        ''' [Public] Get all composite index
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": {
                    "current_page": 1,
                    "data": [
                        {
                            "id": 9007225,
                            "symbol": "OKEX_ETH",
                            "index_symbol": "ETH",
                            "reference": "OKEX",
                            "weight": null,
                            "value": "133.6719220000",
                            "created_at": "2019-12-23 03:50:15",
                            "updated_at": "2019-12-23 03:50:15"
                        }
                    ]
                }
            }
        '''
        return requests.get(get_margin_composite_index_url(), params=kwargs, headers=self.headers)

    def get_margin_active_orders(self, **kwargs):
        ''' [Private] Get all active orders
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": null
            }
        '''

        return self.private_request(get_margin_active_orders_url(), 'GET', kwargs)

    def get_margin_stop_orders(self, **kwargs):
        ''' [Private] Get all stop orders
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": null
            }
        '''

        return self.private_request(get_margin_stop_orders_url(), 'GET', kwargs)

    def get_margin_fill_orders(self, **kwargs):
        ''' [Private] Get all fill orders
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": null
            }
        '''

        return self.private_request(get_margin_fill_orders_url(), 'GET', kwargs)

    def get_margin_create_order(self, **kwargs):
        ''' [Private] Create Order
        :param instrument_symbol : required
        :type instrument_symbol : string
        :description instrument_symbol : instrument_symbol name.
        :param side : required
        :type side : string
        :description side : trade type(buy, sell).
        :param type : required
        :type type : string
        :description type : type(limit, market).
        :param stop_type : required
        :type stop_type : string
        :description stop_type : stop type(stop_limit, stop_market, take_profit_limit, take_profit_market, trailing_stop, oco, ifd).
        :param quantity : required
        :type quantity : integer
        :description quantity : quantity.
        :param leverage : required
        :type leverage : decimal
        :description leverage : leverage.
        :param price : required
        :type price : decimal
        :description price : price.
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": null
            }
        '''

        return self.private_request(get_margin_create_order_url(), 'POST', kwargs)

    def get_margin_cancel_order(self, **kwargs):
        ''' [Private] Cancel A Order
        :param id : required
        :type id : string
        :description id : id number.
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "6e7a7795297cdc4222ecb77463a7e83638d3f33f",
                "data": null
            }
        '''

        return self.private_request(get_margin_cancel_order_url(), 'POST', kwargs)

    def get_margin_trades(self, **kwargs):
        ''' [Private] Get all your trades in Margin Exchange.
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "6e7a7795297cdc4222ecb77463a7e83638d3f33f",
                "data": null
            }
        '''

        return self.private_request(get_margin_trades_url(), 'GET', kwargs)

    def get_margin_order_book(self, **kwargs):
        ''' [Public] Get all order book follow by symbol
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": {
                    "buy": [
                        {
                            "quantity": "10",
                            "count": "1",
                            "price": "50.0000000000"
                        },
                        {
                            "quantity": "2",
                            "count": "1",
                            "price": "20.0000000000"
                        },
                        {
                            "quantity": "30",
                            "count": "3",
                            "price": "2.0000000000"
                        },
                        {
                            "quantity": "10",
                            "count": "1",
                            "price": "0.5000000000"
                        }
                    ],
                    "sell": [],
                    "meta": {
                        "updated_at": null,
                        "is_full_orderbook": true
                    },
                    "at": [
                        {
                            "price": "BTCUSD"
                        },
                        {
                            "price": "TRXZ19"
                        },
                        {
                            "price": "XRPZ19"
                        },
                        {
                            "price": "BTCZ19"
                        },
                        {
                            "price": "BTCH20"
                        },
                        {
                            "price": "ETHUSD"
                        },
                        {
                            "price": "ADAZ19"
                        },
                        {
                            "price": "BCHZ19"
                        },
                        {
                            "price": "EOSZ19"
                        },
                        {
                            "price": "LTCZ19"
                        }
                    ]
                }
            }
        '''
        return requests.get(get_margin_order_book_url(), params=kwargs, headers=self.headers)

    def get_margin_recent(self, **kwargs):
        ''' [Public] Get all the most recent successful orders.By default, this request return 50 record.
        :response
            {
                "success": true,
                "message": null,
                "dataVersion": "800351d51f6059392f58bc9da30b8e1cf714d2ef",
                "data": []
            }
        '''
        return requests.get(get_margin_recent_url(), params=kwargs, headers=self.headers)
