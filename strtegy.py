class Strategy():
    # option setting needed
    def __setitem__(self, key, value):
        self.options[key] = value

    # option setting needed
    def __getitem__(self, key):
        return self.options.get(key, '')

    def __init__(self):
        # strategy property
        self.subscribedBooks = {
            'Binance': {
                'pairs': ['BTC-USDT'],
            },
        }
        self.period = 60 * 20
        self.options = {}

        # user defined class attribute
        self.history=[]
        self.sell = False
        self.sell_price = 0

    def on_order_state_change(self,  order):
        Log("on order state change message: " + str(order) + " order price: " + str(order["price"]))
        self.sell_price = order["price"]


    # called every self.period
    def trade(self, information):
        exchange = list(information['candles'])[0]
        pair = list(information['candles'][exchange])[0]
        target_currency = pair.split('-')[0]  #ETH
        base_currency = pair.split('-')[1]  #USDT
        base_currency_amount = self['assets'][exchange][base_currency] 
        target_currency_amount = self['assets'][exchange][target_currency] 
        # add latest price into trace
        close_price = information['candles'][exchange][pair][0]['close']
        self.history.append(close_price)
        if(len(self.history) > 30 and close_price < min(self.history[-30:-2]) and not self.sell ):
            self.sell = True
            return [
                {
                    'exchange': exchange,
                    'amount': 1,
                    'price': -1,
                    'type': 'MARKET',
                    'pair': pair,
                }
            ]
        elif(len(self.history) > 30 and (close_price - self.sell_price) / self.sell_price >= 0.05  ):
            self.sell = False
            return [
                {
                    'exchange': exchange,
                    'amount': -1,
                    'price': -1,
                    'type': 'MARKET',
                    'pair': pair,
                }
            ]


        return []

