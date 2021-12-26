from binance.client import Client  #pip install python-binance
from binance.enums import *
from cre import api_key, api_secret
import time
import telegram_send


client = Client(api_key, api_secret)
stables = ["SUSDUSDT", "USTUSDT", "BUSDUSDT", "USDPUSDT", "TUSDUSDT", "USDCUSDT"]

def takeprice(stable):
    price = client.get_ticker(symbol=stable)
    return price['lastPrice']

def buy_stable(stable) :
    order = client.order_limit_buy(symbol=f'{stable}', quantity= 99, price= 0.992)
    telegram_send.send(messages = [f"{stable} alım emri gönderildi"])
    #return f"{stable} alım emri gönderildi"
    pass

while True :        
    for i in stables :
        price = takeprice(i)
        print(price)
        if float(price) < 1 :
            buy_stable(i)
            time.sleep(30)
