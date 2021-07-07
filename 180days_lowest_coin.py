#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 비현코패키지

# 모든 함수를 한번에 실행

# 거래소 구조 설명 https://docs.upbit.com/docs
# 원화거래 / BTC 거래 / USDT 거래
# 1.업비트의 코인 종류 체크

from urllib.parse import urlencode
import hashlib
import uuid
import jwt
import os
import pandas as pd
import time
import requests
import json
# get_ipython().system('pip install upbit-client')
from upbit.client import Upbit


# 주문취소
def order_cancel(ud):
    query = {
        'uuid': ud,
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.delete(server_url + "/v1/order",
                          params=query, headers=headers)

    print(res.json())


def coins(current):
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails": "true"}
    response = requests.request("GET", url, params=querystring)
    response_json = json.loads(response.text)

    KRWticker = []
    BTCticker = []
    USDTticker = []

    for a in response_json:
        #     print(a['market'])
        if "KRW-" in a['market']:
            KRWticker.append(a['market'])
        elif "BTC-" in a['market']:
            BTCticker.append(a['market'])
        elif "USDT-" in a['market']:
            USDTticker.append(a['market'])
    ticker = {
        "KRW": KRWticker,
        "BTC": BTCticker,
        "USDT": USDTticker
    }
#     print(ticker)
    if current == "ALL":
        ticker = ticker
    else:
        ticker = ticker[current]
    return ticker


# 암호화폐 시세조회


def coin_price(coin):
    url = "https://api.upbit.com/v1/orderbook"
    querystring = {"markets": coin}
    response = requests.request("GET", url, params=querystring)
    response_json = json.loads(response.text)
    coin_now_price = response_json[0]["orderbook_units"][0]["ask_price"]
    return coin_now_price
# 시세 호가 정보(Orderbook) 조회 // 호가 정보 조회


def coin_history(coin, time1='minute', time2=""):
    url = f"https://api.upbit.com/v1/candles/{time1}/{time2}"

    querystring = {"market": coin, "count": "200"}

    response = requests.request("GET", url, params=querystring)
    response_json = json.loads(response.text)
    # print(type(response_json))
    df = pd.DataFrame(response_json)
    return df

# 로그인


def login():
    # f = open("upbit_api_key.txt")
    # lines = f.readlines()
    global access_key
    global secret_key
    # access_key = str(lines[0].strip())
    # secret_key = str(lines[1].strip())
    access_key = input("access_key : ")
    secret_key = input("secret_key : ")
    # f.close


login()

# order_list 보는법


def order_list():
    client = Upbit(access_key, secret_key)
    resp = client.Order.Order_info_all()
    return resp['result']


# 나의 계좌 잔액 조회


def balance():
    global server_url
    server_url = 'https://api.upbit.com'

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/accounts", headers=headers)
#     print(res.json())
    return res.json()


balance()
# 매수(지정가)


# access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
# secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
# server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

def buy_limit(coin, volume, price):
    query = {
        'market': coin,
        'side': 'bid',
        'volume': volume,
        'price': price,
        'ord_type': 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders",
                        params=query, headers=headers)
    print(res.json())
    return res.json()


# 매수(시장가)


# access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
# secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
# server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

def buy_market(coin, price):
    query = {
        'market': coin,
        'side': 'bid',
        'volume': '',
        'price': price,
        'ord_type': 'price',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders",
                        params=query, headers=headers)
    print(res.json())
    return res.json()


# 매도(지정가)


# access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
# secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
# server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

def sell_limit(coin, volume, price):
    query = {
        'market': coin,
        'side': 'ask',
        'volume': volume,
        'price': price,
        'ord_type': 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders",
                        params=query, headers=headers)
    print(res.json())
    return res.json()

# 매도(시장가)


# access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
# secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
# server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

def sell_market(coin, volume):
    query = {
        'market': coin,
        'side': 'ask',
        'volume': volume,
        'price': '',
        'ord_type': 'market',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders",
                        params=query, headers=headers)
    print(res.json())
    return res.json()


# In[ ]:


# 판매가격을 설정한다. 업비트 기준으로 구매가능한 단위로 바꿔준다.
# ex-  35432원에 구매를 하고싶더라도, 해당 가격으로는 구매하지 못한다. 35430원 VS35440원 둘중에 하나를 골라야 한다.

def price_trim(price_trim):

    # ~10원 미만[소수점 둘째자리]
    if price_trim < 10:
        price_trim = round(price_trim, 2)

    # 10~100원 미만 - [소수점첫째자리]
    elif price_trim < 100:
        price_trim = round(price_trim, 1)

    # 100~1,000원 미만 - [1원단위]
    elif price_trim < 1000:
        price_trim = round(price_trim)

    # 1,000~10,000원 미만[5원단위]
    elif price_trim < 10000:
        price_trim = round(price_trim*2, -1)/2

    # 10,000~100,000원 미만[10원단위]
    elif price_trim < 100000:
        price_trim = round(price_trim, -1)

    # 100,000~500,000원 미만 [50원단위]
    elif price_trim < 500000:
        price_trim = round(price_trim*2, -2)/2

    # 500,000원~1,000,000원 미만[100원단위]
    elif price_trim < 1000000:
        price_trim = round(price_trim, -2)

    # 1,000,000~2,000,000 [500원단위]
    elif price_trim < 2000000:
        price_trim = round(price_trim*2, -3)/2

    # 2,000,000 이상 [1000원단위]
    else:
        price_trim = round(price_trim, -3)

    return price_trim


while True:

    try:
        # 1분봉으로 200분 안에 제일 하락을 많이 한 코인을 찾기
        # coin_history("KRW-BTC","minutes",30)
        tickers = coins("KRW")
        decrease_top_score = 0.001
        # ticker = "KRW-BTC"
        print("첫번째포문시작")

        tickers2 = []
        for tic in tickers:
            if tic == "KRW-KMD":
                print("제외")
            elif tic == "KRW-MARO":
                print("제외")
            elif tic == "KRW-PCI":
                print("제외")
            elif tic == "KRW-OBSR":
                print("제외")
            elif tic == "KRW-SOLVE":
                print("제외")
            elif tic == "KRW-QTCON":
                print("제외")
            elif tic == "KRW-ADX":
                print("제외")
            elif tic == "KRW-LBC":
                print("제외")
            elif tic == "KRW-IGNIS":
                print("제외")
            elif tic == "KRW-DMT":
                print("제외")
            elif tic == "KRW-EMC2":
                print("제외")
            elif tic == "KRW-TSHP":
                print("제외")
            elif tic == "KRW-LAMB":
                print("제외")
            elif tic == "KRW-EDR":
                print("제외")
            elif tic == "KRW-PXL":
                print("제외")
            elif tic == "KRW-PICA":
                print("제외")
            elif tic == "KRW-RDD":
                print("제외")
            elif tic == "KRW-RINGX":
                print("제외")
            elif tic == "KRW-VITE":
                print("제외")
            elif tic == "KRW-ITAM":
                print("제외")
            elif tic == "KRW-SYS":
                print("제외")
            elif tic == "KRW-BASIC":
                print("제외")
            elif tic == "KRW-NXT":
                print("제외")
            elif tic == "KRW-BFT":
                print("제외")
            elif tic == "KRW-NCASH":
                print("제외")
            elif tic == "KRW-FSN":
                print("제외")
            elif tic == "KRW-PI":
                print("제외")
            elif tic == "KRW-RCN":
                print("제외")
            elif tic == "KRW-PRO":
                print("제외")
            elif tic == "KRW-ANT":
                print("제외")
            else:
                tickers2.append(tic)

        tickers = tickers2
################################################################################################################
#         for ticker in tickers:
#             time.sleep(0.5)
#             coin_1_m = coin_history(ticker,'minutes',1)
# #             print(coin_1_m)
#             max_high_price = coin_1_m["high_price"].max()
#             now_price = coin_price(ticker)
#         #     print(ticker)
#         #     print(max_high_price)
#         #     print(now_price)
#         #     print("하락률 : " + str(round(((1-(now_price/max_high_price))*100),3)) + "%")
#             decrease_percent = round(((1-(now_price/max_high_price))*100),3)
#             if decrease_percent > decrease_top_score :
#                 decrease_top_score = decrease_percent
#                 decrease_top_score_ticker = [ticker,max_high_price,now_price,(-1)*decrease_percent]

        ratio = -1

        for ticker in tickers:
            time.sleep(0.5)
            df = coin_history(ticker, 'days')
            lowest_price = df['low_price'].min()
            now_price = coin_price(ticker)
            low_distance = (lowest_price-now_price)/lowest_price
            print(ticker)
            print(low_distance)
            if ratio < low_distance:
                ratio = low_distance
                decrease_top_score_ticker = [
                    ticker, lowest_price, now_price, ratio]

#################################################################################################################
        print(decrease_top_score_ticker)
        print("두번째포문시작")
        for a in balance():
            if a['currency'] == 'KRW':
                print(a['balance'])
                buy_amount = float(a['balance'])*0.10
                print(round(buy_amount, -2))
                buy_amount = round(buy_amount, -2)

        # 해당 코인을 시장가에 구매
        # buy_market()
        buy_market(decrease_top_score_ticker[0], buy_amount)
        time.sleep(3)

        # 구매한 코인이 2% 상승했을 때 판매
        # 판매해야하는 가격
        sell_price = price_trim(coin_price(decrease_top_score_ticker[0])*1.02)
        # 가지고있는 코인갯수
        print("세번째포문시작")
        for a in balance():
            if a['currency'] == decrease_top_score_ticker[0].replace("KRW-", ""):
                sell_balance = a['balance']
        # 지정가에 판매
        sell_limit(decrease_top_score_ticker[0], sell_balance, sell_price)

        import datetime
        now = datetime.datetime.now()
        now
        SONJULTIME = 0
        while True:

            time.sleep(60)

            now1 = datetime.datetime.now()
            diff = now1-now
            if SONJULTIME == 0:
                if diff > datetime.timedelta(seconds=180):
                    break
            elif SONJULTIME == 1:
                if diff > datetime.timedelta(seconds=10800):
                    break
             # 중간에 손절이 일어나면 3시간 대기한다.

            try:

                mycl = balance()
                for mcl in mycl:

                    time.sleep(1)
                    if mcl['currency'] == "KRW":
                        print("검사안함")
                    else:
                        print("검사진행")
                        # 코인현재가격
                        now_price = coin_price("KRW-"+mcl['currency'])
                        print(now_price*1)
                        # avg_buy_price
                        avg_buy_price = float(mcl['avg_buy_price'])
                        print(avg_buy_price*1)
                        # 비교하기
                        if avg_buy_price*0.9 > now_price:
                            print("팔아야겠네")
                            for odl in order_list():
                                time.sleep(1)
                                if mcl['currency'] == odl['market'].replace("KRW-", ""):
                                    order_cancel(odl['uuid'])
                                    time.sleep(1)
                            for bal in balance():
                                time.sleep(1)
                                if bal['currency'] == mcl['currency']:
                                    sell_balance = float(bal['balance'])
                            sell_market("KRW-"+mcl['currency'], sell_balance)
                            time.sleep(1)
#                             SONJULTIME=1
            except:
                print("3분 기다리는 동안 오류가 발생했음1")
                print(mcl)
           # 현재 매수평균가보다 호가가 10% 이상 떨어지면, 해당코인 관련 모든 주문을 취소하고 손절한다.
                # 이 검사기간은, 쉬는 기간동안 계속 진행한다. (방식, for문에서 시작시점을 기준으로 30분이 지날때까지 반복)
        print("다음 루프를 시작합니다.")


#         time.sleep(180)
    except:
        print("3분 기다리는 동안 오류가 발생했음2")
        time.sleep(180)
    # 30분단위로 반복


# In[ ]:
