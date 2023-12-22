
from iqoptionapi.stable_api import IQ_Option
import time
error_password="""{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
iqoption = IQ_Option(USERNAME,PASS)
check,reason=iqoption.connect()
from time import strftime, localtime


def take_trade(currency,Money,expiry_time,expirations_mode):
  ACTIVES=currency
  green = 0
  red = 0
  ACTION = ''
  prev_candles = iqoption.get_candles(currency,expiry_time,5,time.time())
  last_candle = prev_candles[-1]
  penultimate_candle = prev_candles[-2]
  last_candle_size = last_candle['close']-last_candle['open']
  penultimate_candle_size = penultimate_candle['close']-penultimate_candle['open']
  print('Prev_candle',float(last_candle['close'])-float(last_candle['open']))
  for c in prev_candles[:-1]:
    if c['open']<c['close']:
      green+=1
      print(strftime('%Y-%m-%d %H:%M:%S', localtime(c['from'])),c['open'],c['close'],'GREEN')
    elif c['open']>c['close']:
      print(strftime('%Y-%m-%d %H:%M:%S', localtime(c['from'])),c['open'],c['close'],'RED')
      red+=1
    else:print(strftime('%Y-%m-%d %H:%M:%S', localtime(c['from'])),c['open'],c['close'],'GRAY')

  # Conditions for trade
  if last_candle['open']<last_candle['close']: # last candle is green
    if green == 0 or abs(penultimate_candle_size/last_candle_size)>2: ACTION = 'put'
    else: ACTION= 'call'
    
  elif last_candle['open']>last_candle['close']:# last candle is red
    if red == 0 or abs(penultimate_candle_size/last_candle_size)>2: ACTION = 'call'
    else: ACTION= 'put'
  else:
    if prev_candles[-2]['open']>prev_candles[-2]['close']:
      ACTION = 'put'
    elif prev_candles[-2]['open']<prev_candles[-2]['close']:
      ACTION = 'call'
  
  check,id=iqoption.buy(Money,ACTIVES,ACTION,expirations_mode)
  return id
    
Money = 0
profit = 0
last_result = 0
expirations_mode = 5
expiry_time = 60*expirations_mode
while True:
    id = 0
    taken = 0
    if last_result>0 and last_result<Money:
        Money+=last_result
    else: Money,profit=3,0
    minute = strftime('%M', localtime(time.time()))
#   if int(minute)%5==0 and not taken:
    if not taken:
        id = take_trade("EURJPY",Money,expiry_time,expirations_mode) 
        last_result = iqoption.check_win_v3(id)
        profit += last_result
        print(profit,iqoption.get_balance())
