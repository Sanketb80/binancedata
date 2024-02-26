# from django.core.management.base import BaseCommand
# import websocket
# import json
# import time
# import threading
# import schedule
# import json
# from concurrent.futures import ThreadPoolExecutor,wait
# from decimal import Decimal
# from datastructure.models import symbolmaster

# class BinanceWebSocketClient:
#     def _init_(self):
        
#         self.last_update_time = {}

#     def on_message(self, ws, message):
#         try:
#             data = json.loads(message)

#             for ticker_data in data:
#                 print(ticker_data)
#                 symbol = ticker_data.get('s', 'N/A')
#                 close_price = Decimal(ticker_data.get('c', 'N/A'))
#                 try:
                    
#                     users = symbolmaster.objects.get(symbol = symbol)
                    
#                     onehr = round(float(users.onehr),3)
#                     twohr = round(float(users.twohr),3)
#                     totalhr = round(float(users.totalhr),3)
                    
#                     onehrchange = float(close_price) - float(onehr)
#                     users.onehrprice = round(onehrchange,3)
#                     users.ltp = float(close_price)
#                     users.onehrchange = (onehrchange/float(onehr)) * 100
                    
#                     twohrchange = float(close_price) - float(twohr)
#                     users.twohrprice =  round(twohrchange,3)
#                     users.twohrchange = (twohrchange/float(twohr)) * 100
#                     totalhrchange = float(close_price) - float(totalhr)
#                     users.totalhrprice = round(totalhrchange,3)
#                     users.totalhrchange = (totalhrchange/float(totalhr)) * 100
#                     users.save()
#                     print(symbol,onehrchange,twohrchange,totalhrchange)
#                 except:
#                     pass
               
                
#                 # current_time = timezone.now()
#                 # last_update_time = self.last_update_time.get(symbol, None)

#                 # if last_update_time is None or (current_time - last_update_time).seconds >= 3600:
                    
#                 #     print(f"Symbol: {symbol}, close_price: {close_price}")
#                 #     self.last_update_time[symbol] = current_time
                    

#         except json.JSONDecodeError as e:
#             print(f"Error decoding JSON: {e}")
#         except Exception as e:
#             print(f"Error processing WebSocket message: {e}")

#     def on_close(self, ws, close_status_code, close_msg):
#         print("Connection closed")

#     def run_forever(self):
#         ws = websocket.WebSocketApp(
#             "wss://dstream.binance.com/ws/!ticker@arr",
#             on_message=self.on_message,
#             on_close=self.on_close
#         )

#         ws.run_forever()

# class Command(BaseCommand):
#     help = 'Runs the WebSocket client for ticker data'

#     # def add_arguments(self, parser):
#     #     pass

#     def handle(self, *args, **options):
#         # socket_url = 'wss://stream.binance.com:9443/ws/!ticker@arr'
#         binance_client = BinanceWebSocketClient()
#         binance_client.run_forever()

from django.core.management.base import BaseCommand
import websocket
import json
import time
import threading
import schedule
import json
from concurrent.futures import ThreadPoolExecutor,wait, FIRST_COMPLETED
from decimal import Decimal
from datastructure.models import symbolmaster
from django.db.models import Q
from django.db import transaction

class BinanceWebSocketClient:
    def __init__(self):
        
        self.last_update_time = {}

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            
            updates = []
            
            # with ThreadPoolExecutor(max_workers=200) as executor:
                
            #     futures = [executor.submit(updatedata, ticker_data) for ticker_data in data]
                
            #     time.sleep(2)

            #     # Collect results from completed futures
            #     updates = [future.result() for future in futures]
            #     print(updates)
            # with transaction.atomic():
            #     symbolmaster.objects.bulk_update(updates, ['onehrprice', 'ltp', 'onehrchange', 'twohrprice', 'twohrchange', 'totalhrprice', 'totalhrchange'])
            #     print('sanket')
            with ThreadPoolExecutor(max_workers=230) as executor:
                loop_logic = [executor.submit(updatedata,ticker_data) for ticker_data in data]
            # for ticker_data in data:
                
            #     symbol = ticker_data.get('s', 'N/A')
            #     close_price = Decimal(ticker_data.get('c', 'N/A'))
            #     print(symbol,close_price)
            #     # price_change = Decimal(ticker_data.get('p','N/A'))
            #     # price_change_percent = Decimal(ticker_data.get('p','N/A'))
                
            #     try:
                    
            #         users = symbolmaster.objects.get(symbol = symbol)
                    
            #         onehr = round(float(users.onehr),3)
            #         twohr = round(float(users.twohr),3)
            #         totalhr = round(float(users.totalhr),3)
                    
            #         onehrchange = float(close_price) - float(onehr)
            #         users.onehrprice = round(onehrchange,3)
            #         users.ltp = float(close_price)
            #         users.onehrchange = (onehrchange/float(onehr)) * 100
                    
            #         twohrchange = float(close_price) - float(twohr)
            #         users.twohrprice =  round(twohrchange,3)
            #         users.twohrchange = (twohrchange/float(twohr)) * 100
            #         totalhrchange = float(close_price) - float(totalhr)
            #         users.totalhrprice = round(totalhrchange,3)
            #         users.totalhrchange = (totalhrchange/float(totalhr)) * 100
            #         users.save()
            #         print(symbol,onehrchange,twohrchange,totalhrchange)
            #     except:
            #         pass
               
                
                # current_time = timezone.now()
                # last_update_time = self.last_update_time.get(symbol, None)

                # if last_update_time is None or (current_time - last_update_time).seconds >= 3600:
                    
                #     print(f"Symbol: {symbol}, close_price: {close_price}")
                #     self.last_update_time[symbol] = current_time
                    

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"Error processing WebSocket message: {e}")

    

    def on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")

    def run_forever(self):
        ws = websocket.WebSocketApp(
            "wss://dstream.binance.com/ws/!ticker@arr",
            on_message=self.on_message,
            on_close=self.on_close
        )

        ws.run_forever()

class Command(BaseCommand):
    help = 'Runs the WebSocket client for ticker data'

    # def add_arguments(self, parser):
    #     pass

    def handle(self, *args, **options):
        # socket_url = 'wss://stream.binance.com:9443/ws/!ticker@arr'
        binance_client = BinanceWebSocketClient()
        binance_client.run_forever()

from django.db.models import F
def updatedata(ticker_data):
    symbol = ticker_data.get('s', 'N/A')
    close_price = Decimal(ticker_data.get('c', 'N/A'))
    print(symbol)
    # price_change = Decimal(ticker_data.get('p','N/A'))
    # price_change_percent = Decimal(ticker_data.get('p','N/A'))
    
    
        
    users = symbolmaster.objects.get(Q(symbol = symbol) & Q(type = "COIN-M"))
    
    onehrchange = float(close_price) - float(users.onehr)
    twohrchange = float(close_price) - float(users.twohr)
    totalhrchange = float(close_price) - float(users.totalhr)
    
    # return symbolmaster(
    #     id=users.id,
    #     onehrprice=F('onehrprice') + onehrchange,
    #     ltp=float(close_price),
    #     onehrchange=F('onehrchange') + (onehrchange / float(users.onehr)) * 100,
    #     twohrprice=F('twohrprice') + twohrchange,
    #     twohrchange=F('twohrchange') + (twohrchange / float(users.twohr)) * 100,
    #     totalhrprice=F('totalhrprice') + totalhrchange,
    #     totalhrchange=F('totalhrchange') + (totalhrchange / float(users.totalhr)) * 100
    # )
    symbolmaster.objects.filter(Q(symbol=symbol) & Q(type="COIN-M")).update(
        onehrprice= onehrchange,
        ltp=float(close_price),
        onehrchange=(onehrchange / float(users.onehr)) * 100,
        twohrprice=twohrchange,
        twohrchange=(twohrchange / float(users.twohr)) * 100,
        totalhrprice=totalhrchange,
        totalhrchange=(totalhrchange / float(users.totalhr)) * 100
    )
    print(symbol,onehrchange,twohrchange )
    




    # onehr = float(users.onehr)
    # twohr = float(users.twohr)
    # totalhr = float(users.totalhr)
    
    # onehrchange = float(close_price) - float(onehr)
    # users.onehrprice = onehrchange
    # users.ltp = float(close_price)
    # users.onehrchange = (onehrchange/float(onehr)) * 100
    
    # twohrchange = float(close_price) - float(twohr)
    # users.twohrprice =  twohrchange
    # users.twohrchange = (twohrchange/float(twohr)) * 100
    # totalhrchange = float(close_price) - float(totalhr)
    # users.totalhrprice = totalhrchange
    # users.totalhrchange = (totalhrchange/float(totalhr)) * 100
    # users.save()
    # print(symbol,onehrchange,twohrchange,totalhrchange)
    # except:
    #     pass