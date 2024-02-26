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


def setsymbol3():
    url = "https://api.binance.com/api/v1/exchangeInfo"
    response = requests.get(url)
    userdata = response.json()['symbols']
    for user in userdata:
        if user['status'] == 'TRADING':
            post = symbolmaster(symbol = user['symbol'],type = "SPOT")
            post.save()
            print(user['symbol'])


def get1hrdata():
    userdata = symbolmaster.objects.filter(type = "USD-M")
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop_logic = [executor.submit(set1,user) for user in userdata]

def set1(user):
    try:
        url = "https://fapi.binance.com/fapi/v1/klines?symbol="+user.symbol+"&interval=1h"
        response = requests.get(url)
        response = response.json()
        data = pd.DataFrame(response)
        st = len(data) - 2
        user.onehr =data[4][st]
        user.save()
        print(data[4][st],user.symbol)
    except:
        pass

def get1hrdatac():
    userdata = symbolmaster.objects.filter(type = "COIN-M")
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop_logic = [executor.submit(set1c,user) for user in userdata]

def set1c(user):
    try:
        url = "https://dapi.binance.com/dapi/v1/klines?symbol="+user.symbol+"&interval=1h"
        response = requests.get(url)
        response = response.json()
        
        data = pd.DataFrame(response)
        st = len(data) - 2
        
        user.onehr =float(data[4][st])
        
        user.save()
        print(data[4][st],user.symbol)
    except:
        pass

def get1hrdatab():
    userdata = symbolmaster.objects.filter(type = "SPOT")
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop_logic = [executor.submit(set1b,user) for user in userdata]

def set1b(user):
    try:
        url = "https://api.binance.com/api/v1/klines?symbol="+user.symbol+"&interval=1h"
        response = requests.get(url)
        response = response.json()

        data = pd.DataFrame(response)
        st = len(data) - 2
        user.onehr =data[4][st]
        print(data[4][st],user.symbol)
        user.save()
        print(data[4][st],user.symbol)
    except:
        pass

def get4hrdata():
    userdata = symbolmaster.objects.filter(type = "USD-M")
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop_logic = [executor.submit(set,user) for user in userdata]

def set(user):
    try:
        url = "https://fapi.binance.com/fapi/v1/klines?symbol="+user.symbol+"&interval=4h"
        response = requests.get(url)
        response = response.json()

        data = pd.DataFrame(response)
        st = len(data) - 2
        user.twohr = data[4][st]
        user.save()
        print(data[4][st],user.symbol)
    except:
        pass

def get4hrdatac():
    userdata = symbolmaster.objects.filter(type = "COIN-M")
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop_logic = [executor.submit(setc,user) for user in userdata]

def setc(user):
    try:
        url = "https://dapi.binance.com/dapi/v1/klines?symbol="+user.symbol+"&interval=4h"
        response = requests.get(url)
        response = response.json()

        data = pd.DataFrame(response)
        st = len(data) - 2
        user.twohr = data[4][st]
        user.save()
        print(data[4][st],user.symbol)
    except:
        pass

def get4hrdatab():
    userdata = symbolmaster.objects.filter(type = "SPOT")
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop_logic = [executor.submit(setb,user) for user in userdata]

def setb(user):
    try:
        url = "https://api.binance.com/api/v1/klines?symbol="+user.symbol+"&interval=4h"
        response = requests.get(url)
        response = response.json()

        data = pd.DataFrame(response)
        st = len(data) - 2
        user.twohr = data[4][st]
        user.save()
        print(data[4][st],user.symbol)
    except:
        pass

def get24hrdata():
    userdata = symbolmaster.objects.filter(type = "USD-M")
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop_logic = [executor.submit(set3,user) for user in userdata]

def set3(user):
    try:

        url = "https://fapi.binance.com/fapi/v1/klines?symbol="+user.symbol+"&interval=1d"
        response = requests.get(url)
        response = response.json()
    
        data = pd.DataFrame(response)
        st = len(data) - 2
        user.totalhr =data[4][st]
        user.save()
        print(data[4][st],user.symbol)
    except:
        pass


def get24hrdatac():
    userdata = symbolmaster.objects.filter(type = "COIN-M")
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop_logic = [executor.submit(set3c,user) for user in userdata]

def set3c(user):
    try:
        url = "https://dapi.binance.com/dapi/v1/klines?symbol="+user.symbol+"&interval=1d"
        response = requests.get(url)
        response = response.json()
    
        data = pd.DataFrame(response)
        st = len(data) - 2
        user.totalhr =data[4][st]
        user.save()
        print(data[4][st],user.symbol)
    except:
        pass


def get24hrdatab():
    userdata = symbolmaster.objects.filter(type = "SPOT")
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop_logic = [executor.submit(set3b,user) for user in userdata]

def set3b(user):
    try:
        url = "https://api.binance.com/api/v1/klines?symbol="+user.symbol+"&interval=1d"
        response = requests.get(url)
        response = response.json()
        
        data = pd.DataFrame(response)
        st = len(data) - 2
        user.totalhr =data[4][st]
        print(data[4][st],user.symbol)
        user.save()
        
    except:
        pass


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
    step = percentage
    if float(step) == 0.5:
        percentage_array = [10,9.5,9,8.5,8,7.5,7,6.5,6,5.5,5,4.5,4,3.5,3,2.5,2,1.5,1,0.5,0,0,-0.5,-1,-1.5,-2,-2.5,-3,-3.5,-4,-4.5,-5,-5.5,-6,-6.5,-7,-7.5,-8,-8.5,-9,-9.5,-10]
    elif int(step) == 1:
        percentage_array = [10,9,8,7,6,5,4,3,2,1,0,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]
    elif int(step) == 2:
        percentage_array = [10,8,6,4,2,0,0,-2,-4,-6,-8,-10]
    elif int(step) == 3:
        percentage_array = [12,9,6,3,0,0,-3,-6,-9,-12]
    elif int(step) == 4:
        percentage_array = [12,8,4,0,0,-4,-8,-12]
    elif int(step) == 5:
        percentage_array = [15,10,5,0,0,-5,-10,-15]
    counts1 = []
    counts2 = []
    counts3 = []
    for i in range(0,len(percentage_array)):
        print(percentage_array[i])
        if i == 0:
            
            counts3.append('rgba(0, 128, 0, 0.6)')
            
            # elif percentage_array[i] == 0 and percentage_array[i-1] == 0:
            #     counts3.append('rgba(169, 169, 169, 0.6)')
            counts1.append(symbolmaster.objects.filter(onehrchange__gte=percentage_array[i]).count())
            counts2.append(">"+str(percentage_array[i])+"%")
        elif i == len(percentage_array):
            counts1.append(symbolmaster.objects.filter(onehrchange__gte=percentage_array[i], onehrchange__lt=percentage_array[i-1]).count())
            counts2.append(str(percentage_array[i-1])+"-"+str(percentage_array[i])+"%")
            counts1.append(symbolmaster.objects.filter(onehrchange__lte=percentage_array[i]).count())
            counts2.append("<"+str(percentage_array[i])+"%")
            counts3.append('rgba(255, 0, 0, 0.6)')
            counts3.append('rgba(255, 0, 0, 0.6)')
        elif percentage_array[i] == 0 and percentage_array[i-1] == 0:
            counts1.append(symbolmaster.objects.filter(onehrchange__gte=-0.00001, onehrchange__lt=0.00001).count())
            counts2.append(str(percentage_array[i])+"%")
            counts3.append('rgba(169, 169, 169, 0.6)' )
        else:
            if percentage_array[i] > 0:
                counts3.append('rgba(0, 128, 0, 0.6)')
            elif percentage_array[i] < 0:
                counts3.append('rgba(255, 0, 0, 0.6)')
            
            elif percentage_array[i] == 0 and percentage_array[i+1] == 0:
                counts3.append('rgba(0, 128, 0, 0.6)')
            if percentage_array[i] == 0 and percentage_array[i+1] == 0:
                counts1.append(symbolmaster.objects.filter(onehrchange__gte=0.00001, onehrchange__lt=percentage_array[i-1]).count())
            elif percentage_array[i-1] == 0 and percentage_array[i] != 0:
                counts1.append(symbolmaster.objects.filter(onehrchange__gte=percentage_array[i], onehrchange__lt=-0.00001).count())
            else:
                counts1.append(symbolmaster.objects.filter(onehrchange__gte=percentage_array[i], onehrchange__lt=percentage_array[i-1]).count())
            counts2.append(str(percentage_array[i-1])+"-"+str(percentage_array[i])+"%")
        # if percentage_array[i] > 0:
        #     counts3.append('rgba(0, 128, 0, 0.6)')
        # elif percentage_array[i] < 0:
        #     counts3.append('rgba(255, 0, 0, 0.6)')
        # else:
        #     counts3.append('rgba(169, 169, 169, 0.6)')
        # counts2.append(str(percentage_array[i-1])+"-"+str(percentage_array[i])+"%")
    print(counts3)
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

    return JsonResponse({'counts': counts1,"counts1":counts2,"counts3":counts3})




@csrf_exempt
def four_hr(request):
    
    
    data = json.loads(request.body.decode('utf-8'))
    percentage = data.get('percentage', None)
    step = percentage
    if float(step) == 0.5:
        percentage_array = [10,9.5,9,8.5,8,7.5,7,6.5,6,5.5,5,4.5,4,3.5,3,2.5,2,1.5,1,0.5,0,0,-0.5,-1,-1.5,-2,-2.5,-3,-3.5,-4,-4.5,-5,-5.5,-6,-6.5,-7,-7.5,-8,-8.5,-9,-9.5,-10]
    elif int(step) == 1:
        percentage_array = [10,9,8,7,6,5,4,3,2,1,0,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]
    elif int(step) == 2:
        percentage_array = [10,8,6,4,2,0,0,-2,-4,-6,-8,-10]
    elif int(step) == 3:
        percentage_array = [12,9,6,3,0,0,-3,-6,-9,-12]
    elif int(step) == 4:
        percentage_array = [12,8,4,0,0,-4,-8,-12]
    elif int(step) == 5:
        percentage_array = [15,10,5,0,0,-5,-10,-15]
    counts1 = []
    counts2 = []
    counts3 = []
    for i in range(0,len(percentage_array)):
        print(percentage_array[i])
        if i == 0:
            
            counts3.append('rgba(0, 128, 0, 0.6)')
            
            # elif percentage_array[i] == 0 and percentage_array[i-1] == 0:
            #     counts3.append('rgba(169, 169, 169, 0.6)')
            counts1.append(symbolmaster.objects.filter(twohrchange__gte=percentage_array[i]).count())
            counts2.append(">"+str(percentage_array[i])+"%")
        elif i == len(percentage_array):
            counts1.append(symbolmaster.objects.filter(twohrchange__gte=percentage_array[i], twohrchange__lt=percentage_array[i-1]).count())
            counts2.append(str(percentage_array[i-1])+"-"+str(percentage_array[i])+"%")
            counts1.append(symbolmaster.objects.filter(twohrchange__lte=percentage_array[i]).count())
            counts2.append("<"+str(percentage_array[i])+"%")
            counts3.append('rgba(255, 0, 0, 0.6)')
            counts3.append('rgba(255, 0, 0, 0.6)')
        elif percentage_array[i] == 0 and percentage_array[i-1] == 0:
            counts1.append(symbolmaster.objects.filter(twohrchange__gte=-0.00001, twohrchange__lt=0.00001).count())
            counts2.append(str(percentage_array[i])+"%")
            counts3.append('rgba(169, 169, 169, 0.6)' )
        else:
            if percentage_array[i] > 0:
                counts3.append('rgba(0, 128, 0, 0.6)')
            elif percentage_array[i] < 0:
                counts3.append('rgba(255, 0, 0, 0.6)')
            
            elif percentage_array[i] == 0 and percentage_array[i+1] == 0:
                counts3.append('rgba(0, 128, 0, 0.6)')
            if percentage_array[i] == 0 and percentage_array[i+1] == 0:
                counts1.append(symbolmaster.objects.filter(twohrchange__gte=0.00001, twohrchange__lt=percentage_array[i-1]).count())
            elif percentage_array[i-1] == 0 and percentage_array[i] != 0:
                counts1.append(symbolmaster.objects.filter(twohrchange__gte=percentage_array[i], twohrchange__lt=-0.00001).count())
            else:
                counts1.append(symbolmaster.objects.filter(twohrchange__gte=percentage_array[i], twohrchange__lt=percentage_array[i-1]).count())
            counts2.append(str(percentage_array[i-1])+"-"+str(percentage_array[i])+"%")
        # if percentage_array[i] > 0:
        #     counts3.append('rgba(0, 128, 0, 0.6)')
        # elif percentage_array[i] < 0:
        #     counts3.append('rgba(255, 0, 0, 0.6)')
        # else:
        #     counts3.append('rgba(169, 169, 169, 0.6)')
        # counts2.append(str(percentage_array[i-1])+"-"+str(percentage_array[i])+"%")
    
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

    return JsonResponse({'counts': counts1,"counts1":counts2,"counts3":counts3})



def generate_percentage_array(start, end, step):
    percentage_array = []

    # Generate the array from start to end with the specified step
    current_value = start
    while current_value >= end:
        percentage_array.append(current_value)
        current_value -= step

    return percentage_array

# def four_hr(request):
    
#     counts = [
#         symbolmaster.objects.filter(twohrchange__gte=10).count(),
#         symbolmaster.objects.filter(twohrchange__gte=7, twohrchange__lt=10).count(),
#         symbolmaster.objects.filter(twohrchange__gte=5, twohrchange__lt=7).count(),
#         symbolmaster.objects.filter(twohrchange__gte=3, twohrchange__lt=5).count(),
#         symbolmaster.objects.filter(twohrchange__gte=0, twohrchange__lt=3).count(),
#         symbolmaster.objects.filter(twohrchange__gte=-3, twohrchange__lt=0).count(),
#         symbolmaster.objects.filter(twohrchange__gte=-5, twohrchange__lt=-3).count(),
#         symbolmaster.objects.filter(twohrchange__gte=-7, twohrchange__lt=-5).count(),
#         symbolmaster.objects.filter(twohrchange__gte=-10, twohrchange__lt=-7).count(),
#         symbolmaster.objects.filter(twohrchange__lt=-10).count()

#     ]

#     return JsonResponse({'counts': counts})

@csrf_exempt
def one_day(request):
    
    
    data = json.loads(request.body.decode('utf-8'))
    percentage = data.get('percentage', None)
    step = percentage
    if float(step) == 0.5:
        percentage_array = [10,9.5,9,8.5,8,7.5,7,6.5,6,5.5,5,4.5,4,3.5,3,2.5,2,1.5,1,0.5,0,0,-0.5,-1,-1.5,-2,-2.5,-3,-3.5,-4,-4.5,-5,-5.5,-6,-6.5,-7,-7.5,-8,-8.5,-9,-9.5,-10]
    elif int(step) == 1:
        percentage_array = [10,9,8,7,6,5,4,3,2,1,0,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]
    elif int(step) == 2:
        percentage_array = [10,8,6,4,2,0,0,-2,-4,-6,-8,-10]
    elif int(step) == 3:
        percentage_array = [12,9,6,3,0,0,-3,-6,-9,-12]
    elif int(step) == 4:
        percentage_array = [12,8,4,0,0,-4,-8,-12]
    elif int(step) == 5:
        percentage_array = [15,10,5,0,0,-5,-10,-15]
    counts1 = []
    counts2 = []
    counts3 = []
    for i in range(0,len(percentage_array)):
        print(percentage_array[i])
        if i == 0:
            
            counts3.append('rgba(0, 128, 0, 0.6)')
            
            # elif percentage_array[i] == 0 and percentage_array[i-1] == 0:
            #     counts3.append('rgba(169, 169, 169, 0.6)')
            counts1.append(symbolmaster.objects.filter(totalhrchange__gte=percentage_array[i]).count())
            counts2.append(">"+str(percentage_array[i])+"%")
        elif i == len(percentage_array):
            counts1.append(symbolmaster.objects.filter(totalhrchange__gte=percentage_array[i], totalhrchange__lt=percentage_array[i-1]).count())
            counts2.append(str(percentage_array[i-1])+"-"+str(percentage_array[i])+"%")
            counts1.append(symbolmaster.objects.filter(totalhrchange__lte=percentage_array[i]).count())
            counts2.append("<"+str(percentage_array[i])+"%")
            counts3.append('rgba(255, 0, 0, 0.6)')
            counts3.append('rgba(255, 0, 0, 0.6)')
        elif percentage_array[i] == 0 and percentage_array[i-1] == 0:
            counts1.append(symbolmaster.objects.filter(totalhrchange__gte=-0.00001, totalhrchange__lt=0.00001).count())
            counts2.append(str(percentage_array[i])+"%")
            counts3.append('rgba(169, 169, 169, 0.6)' )
        else:
            if percentage_array[i] > 0:
                counts3.append('rgba(0, 128, 0, 0.6)')
            elif percentage_array[i] < 0:
                counts3.append('rgba(255, 0, 0, 0.6)')
            
            elif percentage_array[i] == 0 and percentage_array[i+1] == 0:
                counts3.append('rgba(0, 128, 0, 0.6)')
            if percentage_array[i] == 0 and percentage_array[i+1] == 0:
                counts1.append(symbolmaster.objects.filter(totalhrchange__gte=0.00001, totalhrchange__lt=percentage_array[i-1]).count())
            elif percentage_array[i-1] == 0 and percentage_array[i] != 0:
                counts1.append(symbolmaster.objects.filter(totalhrchange__gte=percentage_array[i], totalhrchange__lt=-0.00001).count())
            else:
                counts1.append(symbolmaster.objects.filter(totalhrchange__gte=percentage_array[i], totalhrchange__lt=percentage_array[i-1]).count())
            counts2.append(str(percentage_array[i-1])+"-"+str(percentage_array[i])+"%")
        # if percentage_array[i] > 0:
        #     counts3.append('rgba(0, 128, 0, 0.6)')
        # elif percentage_array[i] < 0:
        #     counts3.append('rgba(255, 0, 0, 0.6)')
        # else:
        #     counts3.append('rgba(169, 169, 169, 0.6)')
        # counts2.append(str(percentage_array[i-1])+"-"+str(percentage_array[i])+"%")
    
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

    return JsonResponse({'counts': counts1,"counts1":counts2,"counts3":counts3})



# def one_day(request):
    
#     counts = [
#         symbolmaster.objects.filter(totalhrchange__gte=10).count(),
#         symbolmaster.objects.filter(totalhrchange__gte=7, totalhrchange__lt=10).count(),
#         symbolmaster.objects.filter(totalhrchange__gte=5, totalhrchange__lt=7).count(),
#         symbolmaster.objects.filter(totalhrchange__gte=3, totalhrchange__lt=5).count(),
#         symbolmaster.objects.filter(totalhrchange__gte=0, totalhrchange__lt=3).count(),
#         symbolmaster.objects.filter(totalhrchange__gte=-0.00001, totalhrchange__lt=0.00001).count(),
#         symbolmaster.objects.filter(totalhrchange__gte=-3, totalhrchange__lt=0).count(),
#         symbolmaster.objects.filter(totalhrchange__gte=-5, totalhrchange__lt=-3).count(),
#         symbolmaster.objects.filter(totalhrchange__gte=-7, totalhrchange__lt=-5).count(),
#         symbolmaster.objects.filter(totalhrchange__gte=-10, totalhrchange__lt=-7).count(),
#         symbolmaster.objects.filter(totalhrchange__lt=-10).count()

#     ]

#     return JsonResponse({'counts': counts})
    


[11, 2, 3, 3, 5, 6, 12, 28, 29, 69, 600, 0, 646, 77, 10, 0, 4, 0, 0, 0, 0, 0] 
['>10%', '10-9%', '9-8%', '8-7%', '7-6%', '6-5%', '5-4%', '4-3%', '3-2%', '2-1%', '1-0%', '0%', '0--1%', '-1--2%', '-2--3%', '-3--4%', '-4--5%', '-5--6%', '-6--7%', '-7--8%', '-8--9%', '-9--10%'] 
['rgba(0, 128, 0, 0.6)0', 'rgba(0, 128, 0, 0.6)1', 'rgba(0, 128, 0, 0.6)2', 'rgba(0, 128, 0, 0.6)3', 'rgba(0, 128, 0, 0.6)4', 'rgba(0, 128, 0, 0.6)5', 'rgba(0, 128, 0, 0.6)6', 'rgba(0, 128, 0, 0.6)7', 'rgba(0, 128, 0, 0.6)8', 'rgba(0, 128, 0, 0.6)9', 'rgba(169, 169, 169, 0.6)10', 'rgba(169, 169, 169, 0.6)11', 'rgba(255, 0, 0, 0.6)12', 'rgba(255, 0, 0, 0.6)13', 'rgba(255, 0, 0, 0.6)14', 'rgba(255, 0, 0, 0.6)15', 'rgba(255, 0, 0, 0.6)16', 'rgba(255, 0, 0, 0.6)17', 'rgba(255, 0, 0, 0.6)18', 'rgba(255, 0, 0, 0.6)19', 'rgba(255, 0, 0, 0.6)20', 'rgba(255, 0, 0, 0.6)21']