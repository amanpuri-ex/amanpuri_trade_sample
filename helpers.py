BASE_URL = 'https://api.amanpuri.io/'
API_URL = '{base}api/'.format(base=BASE_URL)
PUBLIC_API_VERSION = 'v1'
PRIVATE_API_VERSION = 'v1'


def get_price_scope_url():
    return API_URL + PUBLIC_API_VERSION + '/price-scope'


def get_order_books_url():
    return API_URL + PUBLIC_API_VERSION + '/orders/order-book'


def get_market_recent_trades_url():
    return API_URL + PUBLIC_API_VERSION + '/orders/transactions/recent'


def get_auth_token_url():
    return API_URL + PUBLIC_API_VERSION + '/oauth/token'


def get_order_transaction_latest_url():
    return API_URL + PUBLIC_API_VERSION + '/order-transaction-latest'


def get_cancel_all_order_url():
    return API_URL + PRIVATE_API_VERSION + '/orders/cancel-all'


def get_cancel_by_type_url():
    return API_URL + PRIVATE_API_VERSION + '/orders/cancel-by-type'


def get_cancel_a_order_url(order_id):
    return API_URL + PRIVATE_API_VERSION + '/orders/{}/cancel'.format(order_id)


def get_user_order_history_url():
    return API_URL + PRIVATE_API_VERSION + '/orders/transactions'


def get_user_opening_orders_url():
    return API_URL + PRIVATE_API_VERSION + '/orders/pending'


def get_all_user_opening_orders_url():
    return API_URL + PRIVATE_API_VERSION + '/orders/pending-all'


def get_create_order_url():
    return API_URL + PRIVATE_API_VERSION + '/orders'


def get_user_trading_history_url():
    return API_URL + PRIVATE_API_VERSION + '/orders/trading-histories'


def get_my_trade_history_url():
    return API_URL + PRIVATE_API_VERSION + '/my-order-transactions'


def get_trades_by_order_id_url(order_id):
    return API_URL + PRIVATE_API_VERSION + '/get-trades-by-order-id/{}'.format(order_id)


def get_margin_instruments_url():
    return API_URL + PUBLIC_API_VERSION + '/margin/instrument/all'


def get_margin_active_instruments_url():
    return API_URL + PUBLIC_API_VERSION + '/margin/instrument/active'


def get_margin_indices_url(order_id):
    return API_URL + PUBLIC_API_VERSION + '/margin/instrument/indices/{}'.format(order_id)


def get_margin_indices_active_url():
    return API_URL + PUBLIC_API_VERSION + '/margin/instrument/indices-active'


def get_margin_risk_limit_list_url():
    return API_URL + PUBLIC_API_VERSION + '/margin/instrument/risk-limit-list'


def get_margin_instrument_url(order_id):
    return API_URL + PUBLIC_API_VERSION + '/margin/instrument/{}'.format(order_id)


def get_margin_settlement_history_url():
    return API_URL + PUBLIC_API_VERSION + '/margin/settlement'


def get_margin_insurance_history_url():
    return API_URL + PUBLIC_API_VERSION + '/margin/insurance'


def get_margin_composite_index_url():
    return API_URL + PUBLIC_API_VERSION + '/margin/composite-index'


def get_margin_active_orders_url():
    return API_URL + PRIVATE_API_VERSION + '/margin/order/get-active'


def get_margin_stop_orders_url():
    return API_URL + PRIVATE_API_VERSION + '/margin/order/stops'


def get_margin_positions():
    return API_URL + PRIVATE_API_VERSION + '/margin/positions'


def get_margin_balance():
    return API_URL + PRIVATE_API_VERSION + '/margin/balance'


def get_margin_fill_orders_url():
    return API_URL + PRIVATE_API_VERSION + '/margin/order/fills'


def get_margin_create_order_url():
    return API_URL + PRIVATE_API_VERSION + '/margin/order/create'


def get_margin_cancel_order_url():
    return API_URL + PRIVATE_API_VERSION + '/margin/order/cancel-active-order'


def get_margin_trades_url():
    return API_URL + PRIVATE_API_VERSION + '/margin/trade'


def get_margin_order_book_url():
    return API_URL + PUBLIC_API_VERSION + '/margin/orderbook'


def get_margin_recent_url():
    return API_URL + PUBLIC_API_VERSION + '/margin/trade/recent'
