from django.shortcuts import render
import requests
# Create your views here.
from datastructure.models import symbolmaster
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def setsymbol():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = requests.get(url)
    userdata = response.json()['symbols']
    for user in userdata:
        post = symbolmaster(symbol = user['symbol'],type = "USD-M")
        post.save()
        print(user['symbol'])

def get1hrdata():
    userdata = symbolmaster.objects.all()
    with ThreadPoolExecutor(max_workers=130) as executor:
        loop_logic = [executor.submit(set1,user) for user in userdata]

def set1(user):
    url = "https://fapi.binance.com/fapi/v1/klines?symbol="+user.symbol+"&interval=1h"
    response = requests.get(url)
    response = response.json()
    data = pd.DataFrame(response)
    st = len(data) - 1
    user.onehr = data[4][st]
    user.save()
    print(data[4][st],user.symbol)

def get4hrdata():
    userdata = symbolmaster.objects.all()
    with ThreadPoolExecutor(max_workers=130) as executor:
        loop_logic = [executor.submit(set,user) for user in userdata]

def set(user):
    
    url = "https://fapi.binance.com/fapi/v1/klines?symbol="+user.symbol+"&interval=4h"
    response = requests.get(url)
    response = response.json()
    data = pd.DataFrame(response)
    st = len(data) - 1
    user.twohr = data[4][st]
    user.save()
    print(data[4][st],user.symbol)

def get24hrdata():
    userdata = symbolmaster.objects.all()
    with ThreadPoolExecutor(max_workers=130) as executor:
        loop_logic = [executor.submit(set3,user) for user in userdata]

def set3(user):
    
    url = "https://fapi.binance.com/fapi/v1/klines?symbol="+user.symbol+"&interval=1d"
    response = requests.get(url)
    response = response.json()
    data = pd.DataFrame(response)
    st = len(data) - 1
    user.totalhr = data[4][st]
    user.save()
    print(data[4][st],user.symbol)