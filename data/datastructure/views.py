from django.shortcuts import render
import requests
# Create your views here.
from datastructure.models import symbolmaster
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from django.http import JsonResponse
from django.db.models import Q


def amol(n_pairs, percentage_move):
    # Initialize variables
    p = percentage_move / 100
    n_trials = 10  # Assuming 10 intervals based on your example

    # Calculate probabilities for each interval
    probabilities_up = []
    probabilities_down = []
    for i in range(n_trials):
        probability_up = n_pairs * p
        probability_down = n_pairs * (1 - p)
        probabilities_up.append(probability_up)
        probabilities_down.append(probability_down)

        # Update for the next interval
        n_pairs = probability_down  # The remaining pairs

    return probabilities_up, probabilities_down

def setsymbol():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = requests.get(url)
    userdata = response.json()['symbols']
    for user in userdata:
        post = symbolmaster(symbol = user['symbol'],type = "USD-M")
        post.save()
        print(user['symbol'])

def setsymbol2():
    url = "https://dapi.binance.com/dapi/v1/exchangeInfo"
    response = requests.get(url)
    userdata = response.json()['symbols']
    for user in userdata:
        post = symbolmaster(symbol = user['symbol'],type = "COIN-M")
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
    user.onehr =data[4][st]
    user.save()
    print(data[4][st],user.symbol)

def get1hrdatac():
    userdata = symbolmaster.objects.all()
    with ThreadPoolExecutor(max_workers=130) as executor:
        loop_logic = [executor.submit(set1c,user) for user in userdata]

def set1c(user):
    url = "https://dapi.binance.com/dapi/v1/klines?symbol="+user.symbol+"&interval=1h"
    response = requests.get(url)
    response = response.json()
    data = pd.DataFrame(response)
    st = len(data) - 1
    user.onehr =data[4][st]
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

def get4hrdatac():
    userdata = symbolmaster.objects.all()
    with ThreadPoolExecutor(max_workers=130) as executor:
        loop_logic = [executor.submit(setc,user) for user in userdata]

def setc(user):
    
    url = "https://dapi.binance.com/dapi/v1/klines?symbol="+user.symbol+"&interval=4h"
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
    user.totalhr =data[4][st]
    user.save()
    print(data[4][st],user.symbol)

def get24hrdatac():
    userdata = symbolmaster.objects.all()
    with ThreadPoolExecutor(max_workers=130) as executor:
        loop_logic = [executor.submit(set3c,user) for user in userdata]

def set3c(user):
    
    url = "https://dapi.binance.com/dapi/v1/klines?symbol="+user.symbol+"&interval=1d"
    response = requests.get(url)
    response = response.json()
    data = pd.DataFrame(response)
    st = len(data) - 1
    user.totalhr =data[4][st]
    user.save()
    print(data[4][st],user.symbol)


#get 24hr data
def get_data1(request):
    
    symbol_data = symbolmaster.objects.all()  

    data = [{
        'symbol': crypto.symbol,
        'totalhr': crypto.totalhr,
        'ltp': crypto.ltp,
        'totalhrprice': crypto.totalhrprice,
        'totalhrchange': crypto.totalhrchange,
        
    } for crypto in symbol_data]

    return JsonResponse(data,safe = False)

def get_data(request):
     
    symbol_data = symbolmaster.objects.all()

    return render(request, 'templates/bar.html', {'symbol_data': symbol_data})


#get 4 hr data

def get_data2(request):
    symbol_data_twohr = symbolmaster.objects.all() 
    
    data = [{
        'symbol': crypto.symbol,
        'twohr': crypto.twohr,
        'ltp': crypto.ltp,
        'twohrprice': crypto.twohrprice,
        'twohrchange': crypto.twohrchange,
       
    } for crypto in symbol_data_twohr]

    return JsonResponse(data,safe = False)

def get_data_twohr(request):
    
    symbol_data_twohr = symbolmaster.objects.all()

    return render(request, 'templates/data_4hr.html', {'symbol_data_twohr': symbol_data_twohr})

#get 1 hour data

def get_data3(request):
    symbol_data_onehr = symbolmaster.objects.all() 
    
    data = [{
        'symbol': crypto.symbol,
        'onehr': str(crypto.onehr),
        'ltp': str(crypto.ltp),
        'onehrprice': str(crypto.onehrprice),
        'onehrchange': str(crypto.onehrchange),
       
    } for crypto in symbol_data_onehr]
    
    return JsonResponse(data,safe = False)

def get_data_1hr(request):
    
    symbol_data_onehr = symbolmaster.objects.all()

    return render(request, 'templates/demo.html', {'symbol_data_onehr': symbol_data_onehr})


# def one_hr(request):
#     # user1 = symbolmaster.objects.filter(Q(onehrchange__lte=2) & Q(onehrchange__gte=0)).count()
#     # user1 = symbolmaster.objects.filter(
#     #     Q(onehrchange__gt=10) |
#     #     Q(onehrchange__gte=7, onehrchange__lte=10) |
#     #     Q(onehrchange__gte=5, onehrchange__lt=7) |
#     #     Q(onehrchange__gte=3, onehrchange__lt=5) |
#     #     Q(onehrchange__gte=0, onehrchange__lt=3)
#     # ).count()
#     # count_gt_10 = symbolmaster.objects.filter(onehrchange__gt=10).count()
#     # count_7_to_10 = symbolmaster.objects.filter(onehrchange__gte=7, onehrchange__lte=10).count()
#     # count_5_to_7 = symbolmaster.objects.filter(onehrchange__gte=5, onehrchange__lt=7).count()
#     # count_3_to_5 = symbolmaster.objects.filter(onehrchange__gte=3, onehrchange__lt=5).count()
#     # count_0_to_3 = symbolmaster.objects.filter(onehrchange__gte=0, onehrchange__lt=3).count()

#     # return render(request, 'templates/demo.html', {
#     #     'count_gt_10': count_gt_10,
#     #     'count_7_to_10': count_7_to_10,
#     #     'count_5_to_7': count_5_to_7,
#     #     'count_3_to_5': count_3_to_5,
#     #     'count_0_to_3': count_0_to_3,
#     # })
#     counts = [
#         symbolmaster.objects.filter(onehrchange__gte=10).count(),
#         symbolmaster.objects.filter(onehrchange__gte=7, onehrchange__lt=10).count(),
#         symbolmaster.objects.filter(onehrchange__gte=5, onehrchange__lt=7).count(),
#         symbolmaster.objects.filter(onehrchange__gte=3, onehrchange__lt=5).count(),
#         symbolmaster.objects.filter(onehrchange__gte=0, onehrchange__lt=3).count(),
#         symbolmaster.objects.filter(onehrchange__gte=-3, onehrchange__lt=0).count(),
#         symbolmaster.objects.filter(onehrchange__gte=-5, onehrchange__lt=-3).count(),
#         symbolmaster.objects.filter(onehrchange__gte=-7, onehrchange__lt=-5).count(),
#         symbolmaster.objects.filter(onehrchange__gte=-10, onehrchange__lt=-7).count(),
#         symbolmaster.objects.filter(onehrchange__lt=-10).count()

#     ]

#     return JsonResponse({'counts': counts})
import json
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def one_hr(request):
    # user1 = symbolmaster.objects.filter(Q(onehrchange__lte=2) & Q(onehrchange__gte=0)).count()
    # user1 = symbolmaster.objects.filter(
    #     Q(onehrchange__gt=10) |
    #     Q(onehrchange__gte=7, onehrchange__lte=10) |
    #     Q(onehrchange__gte=5, onehrchange__lt=7) |
    #     Q(onehrchange__gte=3, onehrchange__lt=5) |
    #     Q(onehrchange__gte=0, onehrchange__lt=3)
    # ).count()
    # count_gt_10 = symbolmaster.objects.filter(onehrchange__gt=10).count()
    # count_7_to_10 = symbolmaster.objects.filter(onehrchange__gte=7, onehrchange__lte=10).count()
    # count_5_to_7 = symbolmaster.objects.filter(onehrchange__gte=5, onehrchange__lt=7).count()
    # count_3_to_5 = symbolmaster.objects.filter(onehrchange__gte=3, onehrchange__lt=5).count()
    # count_0_to_3 = symbolmaster.objects.filter(onehrchange__gte=0, onehrchange__lt=3).count()

    # return render(request, 'templates/demo.html', {
    #     'count_gt_10': count_gt_10,
    #     'count_7_to_10': count_7_to_10,
    #     'count_5_to_7': count_5_to_7,
    #     'count_3_to_5': count_3_to_5,
    #     'count_0_to_3': count_0_to_3,
    # })
    
    data = json.loads(request.body.decode('utf-8'))
    percentage = data.get('percentage', None)
    step = int(percentage)
    percentage_array =  generate_percentage_array(10, -10, step)
    counts1 = []
    counts2 = []
   
    for i in range(1,len(percentage_array)):
        counts1.append(symbolmaster.objects.filter(onehrchange__gte=percentage_array[i], onehrchange__lt=percentage_array[i-1]).count())
        counts2.append(str(percentage_array[i-1])+"-"+str(percentage_array[i])+"%")
    print(counts1,counts2)
    # counts = [
    #     symbolmaster.objects.filter(onehrchange__gte=10).count(),
    #     symbolmaster.objects.filter(onehrchange__gte=7, onehrchange__lt=10).count(),
    #     symbolmaster.objects.filter(onehrchange__gte=5, onehrchange__lt=7).count(),
    #     symbolmaster.objects.filter(onehrchange__gte=3, onehrchange__lt=5).count(),
    #     symbolmaster.objects.filter(onehrchange__gte=0, onehrchange__lt=3).count(),
    #     symbolmaster.objects.filter(onehrchange__gte=-3, onehrchange__lt=0).count(),
    #     symbolmaster.objects.filter(onehrchange__gte=-5, onehrchange__lt=-3).count(),
    #     symbolmaster.objects.filter(onehrchange__gte=-7, onehrchange__lt=-5).count(),
    #     symbolmaster.objects.filter(onehrchange__gte=-10, onehrchange__lt=-7).count(),
    #     symbolmaster.objects.filter(onehrchange__lt=-10).count()

    # ]

    return JsonResponse({'counts': counts1,"counts1":counts2})

def generate_percentage_array(start, end, step):
    percentage_array = []

    # Generate the array from start to end with the specified step
    current_value = start
    while current_value >= end:
        percentage_array.append(current_value)
        current_value -= step

    return percentage_array

def four_hr(request):
    
    counts = [
        symbolmaster.objects.filter(twohrchange__gte=10).count(),
        symbolmaster.objects.filter(twohrchange__gte=7, twohrchange__lt=10).count(),
        symbolmaster.objects.filter(twohrchange__gte=5, twohrchange__lt=7).count(),
        symbolmaster.objects.filter(twohrchange__gte=3, twohrchange__lt=5).count(),
        symbolmaster.objects.filter(twohrchange__gte=0, twohrchange__lt=3).count(),
        symbolmaster.objects.filter(twohrchange__gte=-3, twohrchange__lt=0).count(),
        symbolmaster.objects.filter(twohrchange__gte=-5, twohrchange__lt=-3).count(),
        symbolmaster.objects.filter(twohrchange__gte=-7, twohrchange__lt=-5).count(),
        symbolmaster.objects.filter(twohrchange__gte=-10, twohrchange__lt=-7).count(),
        symbolmaster.objects.filter(twohrchange__lt=-10).count()

    ]

    return JsonResponse({'counts': counts})

def one_day(request):
    
    counts = [
        symbolmaster.objects.filter(totalhrchange__gte=10).count(),
        symbolmaster.objects.filter(totalhrchange__gte=7, totalhrchange__lt=10).count(),
        symbolmaster.objects.filter(totalhrchange__gte=5, totalhrchange__lt=7).count(),
        symbolmaster.objects.filter(totalhrchange__gte=3, totalhrchange__lt=5).count(),
        symbolmaster.objects.filter(totalhrchange__gte=0, totalhrchange__lt=3).count(),
        symbolmaster.objects.filter(totalhrchange__gte=-3, totalhrchange__lt=0).count(),
        symbolmaster.objects.filter(totalhrchange__gte=-5, totalhrchange__lt=-3).count(),
        symbolmaster.objects.filter(totalhrchange__gte=-7, totalhrchange__lt=-5).count(),
        symbolmaster.objects.filter(totalhrchange__gte=-10, totalhrchange__lt=-7).count(),
        symbolmaster.objects.filter(totalhrchange__lt=-10).count()

    ]

    return JsonResponse({'counts': counts})
    


