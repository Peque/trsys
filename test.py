
import time
import json
import pickle
import requests


class Trade(object):
    """
    TODO
    """
    def __init__(self, time, amount, price, side, id):
        assert all(isinstance(x, float) for x in [time, last, bid, ask])

        self.time = time
        self.amount = amount
        self.price = price
        self.side = side
        self.id = id

    def __repr__(self):
        return '({0.last}) {0.bid} - {0.ask} @ {0.time}'.format(self)


class Ticker(object):
    """
    TODO
    """
    def __init__(self, time, last, bid, ask):
        assert all(isinstance(x, float) for x in [time, last, bid, ask])

        self.time = time
        self.last = last
        self.bid = bid
        self.ask = ask

    def __repr__(self):
        return '({0.last}) {0.bid} - {0.ask} @ {0.time}'.format(self)


class Symbol(object):
    """
    TODO
    """
    def __init__(self, symbol, commodity, currency, lot, step,
                 provide_liquidity_rate, take_liquidity_rate):
        assert all(isinstance(x, str) for x in [symbol,commodity, currency])
        assert all(isinstance(x, float) for x in [lot, step,
                                                  provide_liquidity_rate,
                                                  take_liquidity_rate])

        self.symbol = symbol
        self.commodity = commodity
        self.currency = currency
        self.lot = lot
        self.step = step
        self.provide_liquidity_rate = provide_liquidity_rate
        self.take_liquidity_rate = take_liquidity_rate

    def __repr__(self):
        return '{0.symbol} ({0.commodity}/{0.currency})'.format(self)


class Symbols(dict):
    """
    TODO
    """
    def __init__(self, symbol_list = None):
        if not symbol_list:
            symbol_list = []
        assert all(isinstance(x, Symbol) for x in symbol_list)
        for symbol in symbol_list:
            self[symbol.symbol] = symbol

    def add(self, symbol):
        assert isinstance(symbol, Symbol)
        self[symbol.symbol] = symbol

    def __repr__(self):
        return str(list(self.values()))


class HitBTCClient(object):
    def __init__(self, demo = True):

        if demo:
            self.endpoint = 'http://demo-api.hitbtc.com'
        else:
            self.endpoint = 'http://api.hitbtc.com'

    def get_symbols(self):
        resource = '/api/1/public/symbols'
        response = requests.get(self.endpoint + resource)

        # Check the response status code
        if response.status_code != 200:
            # TODO: create log system
            print(r)
            return None

        symbols = Symbols()
        for aux in response.json()['symbols']:
            symbol = Symbol(aux['symbol'],
                            aux['commodity'],
                            aux['currency'],
                            float(aux['lot']),
                            float(aux['step']),
                            float(aux['provideLiquidityRate']),
                            float(aux['takeLiquidityRate']))
            symbols.add(symbol)

        return symbols

    def get_ticker(self, symbol):
        """
        TODO
        """
        assert isinstance(symbol, str)

        resource = '/api/1/public/{}/ticker'.format(symbol)
        response = requests.get(self.endpoint + resource)

        # Check the response status code
        if response.status_code != 200:
            # TODO: create log system
            print(r)
            return None

        aux = response.json()
        ticker = Ticker(float(aux['timestamp']),
                        float(aux['last']),
                        float(aux['bid']),
                        float(aux['ask']))

        return ticker

    def get_recent_trades(self, symbol, max_results):
        """
        TODO
        """
        assert isinstance(symbol, str)
        assert isinstance(max_results, int)

        resource = '/api/1/public/{}/trades/recent'.format(symbol)
        params = {'max_results': max_results,
                  'format_item': 'object',
                  'side': 'true'}
        response = requests.get(self.endpoint + resource, params = params)

        # Check the response status code
        if response.status_code != 200:
            # TODO: create log system
            print(r)
            return None

        aux = response.json()


def load_api_key(demo = True):
    """
    TODO
    """
    with open('.keys', 'rb') as f:
        keys = pickle.load(f)
    if demo:
        return keys['demo']['api']
    return keys['real']['api']

def load_secret_key(demo = True):
    """
    TODO
    """
    with open('.keys', 'rb') as f:
        keys = pickle.load(f)
    if demo:
        return keys['demo']['secret']
    return keys['real']['secret']



if __name__ == '__main__':

    client = HitBTCClient()

    symbol = client.get_symbols()['XMRBTC']
    ticker = client.get_ticker(symbol.symbol)
    print(ticker)
    print(load_api_key())
    print(load_secret_key())

