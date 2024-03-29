from django.core.management.base import BaseCommand
import websocket
import json
import time
import threading
import schedule
import json
from concurrent.futures import ThreadPoolExecutor,wait
from decimal import Decimal
from datastructure.models import symbolmaster

class BinanceWebSocketClient:
    def __init__(self):
        
        self.last_update_time = {}

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            with ThreadPoolExecutor(max_workers=230) as executor:
                loop_logic = [executor.submit(updatedata,ticker_data) for ticker_data in data]
            # for ticker_data in data:
                
            #     symbol = ticker_data.get('s', 'N/A')
            #     close_price = Decimal(ticker_data.get('c', 'N/A'))
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
            "wss://fstream.binance.com/ws/!ticker@arr",
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

        
from django.db.models import Q
def updatedata(ticker_data):
    symbol = ticker_data.get('s', 'N/A')
    close_price = Decimal(ticker_data.get('c', 'N/A'))
    try:
        
        users = symbolmaster.objects.get(Q(symbol = symbol) & Q(type = "USD-M"))
        
        onehr = float(users.onehr)
        twohr = float(users.twohr)
        totalhr = float(users.totalhr)
        
        onehrchange = float(close_price) - float(onehr)
        users.onehrprice = onehrchange
        users.ltp = float(close_price)
        users.onehrchange = (onehrchange/float(onehr)) * 100
        
        twohrchange = float(close_price) - float(twohr)
        users.twohrprice =  twohrchange
        users.twohrchange = (twohrchange/float(twohr)) * 100
        totalhrchange = float(close_price) - float(totalhr)
        users.totalhrprice = totalhrchange
        users.totalhrchange = (totalhrchange/float(totalhr)) * 100
        users.save()
        print(symbol,onehrchange,twohrchange,totalhrchange)
    except Exception as e:
        print(str(e))