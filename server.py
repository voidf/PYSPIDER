from fastapi import *

from pydantic import BaseModel

from typing import Optional

import aiohttp
import datetime
import uvicorn
import ujson
import json
from mongoengine import *
from decimal import Decimal


connect('DOGECOIN_MONITOR', host='localhost', port=27017)

class Stock(Document):
    dat = DateTimeField()
    val = DecimalField(precision=20)
    

class BTCHisInfo(Document):
    dat = DateTimeField()
    open = DecimalField(precision=20)
    close = DecimalField(precision=20)
    high = DecimalField(precision=20)
    low = DecimalField(precision=20)

app = FastAPI()

async def on_request_start(session, trace_config_ctx, params):
    print("Starting %s request for %s. I will send: %s" % (params.method, params.url, params.headers))

async def on_request_end(session, trace_config_ctx, params):
    print("Ending %s request for %s. I sent: %s" % (params.method, params.url, params.headers))
tracecfg = aiohttp.TraceConfig()
tracecfg.on_request_start.append(on_request_start)
tracecfg.on_request_end.append(on_request_end)

async def make_req(dvd:int):
    ima = datetime.datetime.now()
    prv = ima - datetime.timedelta(days=dvd)
    async with aiohttp.ClientSession(trace_configs=[tracecfg]) as s:      
        async with s.get(
            f'''https://api.nasdaq.com/api/quote/DOGE/chart?assetclass=crypto&fromdate={prv.strftime('%Y-%m-%d')}&todate={ima.strftime('%Y-%m-%d')}''',
            headers={
                "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "accept-encoding":"gzip, deflate, br",
                "accept-language":"zh-CN,zh;q=0.9",
                "cache-control":"no-cache",
                "dnt":"1",
                "pragma":"no-cache",
                "sec-fetch-mode":"navigate",
                "sec-fetch-site":"none",
                "sec-fetch-user":"?1",
                "upgrade-insecure-requests":"1",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
            }
        ) as r:
            res = await r.text()
            print(json.loads(res))
        return res

async def make_req2(dvd: int):
    ima = datetime.datetime.now()
    prv = ima - datetime.timedelta(days=dvd)
    async with aiohttp.ClientSession(trace_configs=[tracecfg]) as s:      
        async with s.get(
            f'''https://api.nasdaq.com/api/quote/BTC/historical?assetclass=crypto&fromdate={prv.strftime('%Y-%m-%d')}&limit={dvd}8&todate={ima.strftime('%Y-%m-%d')}''',
            headers={
                "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "accept-encoding":"gzip, deflate, br",
                "accept-language":"zh-CN,zh;q=0.9",
                "cache-control":"no-cache",
                "dnt":"1",
                "pragma":"no-cache",
                "sec-fetch-mode":"navigate",
                "sec-fetch-site":"none",
                "sec-fetch-user":"?1",
                "upgrade-insecure-requests":"1",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
            }
        ) as r:
            res = await r.text()
            print(json.loads(res))
        return res
    

def save_and_get_len(res:str):
    for i in json.loads(res)["data"]['chart']:
        d = datetime.datetime.strptime(i['z']['dateTime'], "%m/%d/%Y")
        print(d)
        pre = Stock.objects(dat=d)
        if pre:
            pre.delete()

        Stock(
            dat=d,
            val=Decimal(i['z']['value'])
        ).save()
    return len(Stock.objects())


import matplotlib.pyplot as plt
import mpl_finance as mpf
from matplotlib.pylab import date2num

@app.get('/{prv}')
async def master(prv: int):
    s = ujson.loads(await make_req2(prv))['data']['tradesTable']['rows']
    li = []
    for raw in s:
        _date = datetime.datetime.strptime(raw['date'], "%m/%d/%Y")
        _close = Decimal(raw['close'])
        _open = Decimal(raw['open'])
        _high = Decimal(raw['high'])
        _low = Decimal(raw['low'])
        li.append((date2num(_date), _open, _high, _low, _close))
    print(*li)
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis_date()
    plt.yticks()
    plt.xticks(rotation=45)
    plt.xlabel("History")
    plt.ylabel("USD")

    mpf.candlestick_ohlc(ax, li, width=1.5, colorup='r', colordown='green')

    plt.grid()

    plt.savefig('a.png')

    return li
    
    # return save_and_get_len(await make_req(prv))

@app.get('/draw')
async def draw_(prv: int):
    res = await make_req(prv)
    for i in json.loads(res)["data"]['chart']:
        d = datetime.datetime.strptime(i['z']['dateTime'], "%m/%d/%Y")
        print(d)




if __name__ == '__main__':
    uvicorn.run(app)
