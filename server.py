# 除了需要按requirements.txt安装外，还需要本地装一个MongoDB才能动（为了存入数据库）
# 当然存库其实是完全没有必要的，所以只用“直接爬”的话是完全没有问题的
from fastapi import *
from fastapi.responses import *
from pydantic import BaseModel

from typing import Optional

import aiohttp
import datetime
import uvicorn
import ujson
import json
from mongoengine import *
from decimal import Decimal

from io import BytesIO



connect('DOGECOIN_MONITOR', host='localhost', port=27017)

# class Stock(Document):
#     dat = DateTimeField()
#     val = DecimalField(precision=20)
    

class BTCHisInfo(Document):
    date = DateTimeField(primary_key=True)
    # date = DateTimeField()
    open = DecimalField(precision=20)
    close = DecimalField(precision=20)
    high = DecimalField(precision=20)
    low = DecimalField(precision=20)
    volume = StringField()
    def get_dict(self):
        return {
            'date':self.date.timestamp(),
            'open':self.open,
            'close':self.close,
            'high':self.high,
            'low':self.low,
            'volume':self.volume
        }
    

app = FastAPI()

async def on_request_start(session, trace_config_ctx, params):
    print("Starting %s request for %s. I will send: %s" % (params.method, params.url, params.headers))

async def on_request_end(session, trace_config_ctx, params):
    print("Ending %s request for %s. I sent: %s" % (params.method, params.url, params.headers))
tracecfg = aiohttp.TraceConfig()
tracecfg.on_request_start.append(on_request_start)
tracecfg.on_request_end.append(on_request_end)

async def make_req2(dvd: int, typ: str='BTC'):
    ima = datetime.datetime.now()
    prv = ima - datetime.timedelta(days=dvd)
    async with aiohttp.ClientSession(trace_configs=[tracecfg]) as s:      
        async with s.get(
            f'''https://api.nasdaq.com/api/quote/{typ}/historical?assetclass=crypto&fromdate={prv.strftime('%Y-%m-%d')}&limit={dvd}&todate={ima.strftime('%Y-%m-%d')}''',
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
    

import matplotlib.pyplot as plt
import matplotlib
import pandas
from cycler import cycler
import mplfinance as mpf
from matplotlib.pylab import date2num
import numpy


async def sketch(s: dict, typ: str='BTC') -> BytesIO:
    df = pandas.DataFrame.from_dict(s)
    df["datetime"] = pandas.to_datetime(df['date'])
    df.set_index("datetime",inplace=True)
    df.sort_index(ascending=True, inplace=True)
    df.drop(["date"], axis=1,inplace=True)
    df.drop(["volume"], axis=1,inplace=True)
    df[['open','close','high','low']] = df[['open','close','high','low']].astype('float64')
    # df[['volume']] = 0
    matplotlib.rcParams['axes.prop_cycle']=cycler(
        color=['dodgerblue', 'deeppink', 
        'navy', 'teal', 'maroon', 'darkorange', 
        'indigo']
    )

    matplotlib.rcParams['lines.linewidth']=.5

    buf = BytesIO()
    # kwa = {"savefig":b}

    mpf.plot(
        df,
        type='candle',
        mav=(7, 30, 60), 
        # volume=True, 
        title=f'{typ} historical',
        ylabel='USD $', 
        # ylabel_lower='Shares\nTraded Volume', 
        figratio=(15, 10), 
        figscale=2.0,
        style=mpf.make_mpf_style(
            gridaxis='both',
            gridstyle='-.',
            y_on_right=False,
            marketcolors=mpf.make_marketcolors(
                up='red',
                down='green',
                edge='i',
                wick='i',
                # volume='in',
                inherit=True
            )
        ),
        # **kwa
        savefig=buf
    )
    # print(buf)
    buf.seek(0)
    # print(buf.read())
    
    return buf

# @app.options('/master')
# async def masteroptions():
#     return Response(None, headers={
#         'Access-Control-Allow-Origin': '*',
#         "Access-Control-Allow-Methods": "POST, GET, PUT, OPTIONS, DELETE",
#         "Access-Control-Allow-Headers": "Access-Control-Allow-Origin"
#     })

@app.get('/master')
async def master(prv: int, typ: str='BTC'):
    s = ujson.loads(await make_req2(prv, typ))['data']['tradesTable']['rows']
    # print(s)
    # print(type(s))
    pic = await sketch(s, typ)
    return Response(pic.read(), media_type="image/png", headers={
        'Access-Control-Allow-Origin': '*',
        "Access-Control-Allow-Methods": "POST, GET, PUT, OPTIONS, DELETE",
        "Access-Control-Allow-Headers": "Access-Control-Allow-Origin"
    })

@app.get('/save')
async def save_1(prv: int, typ: str='BTC'):
    print(prv)
    # res = await make_req2(prv)
    # BTCHisInfo.pk = 'date'
    BTCHisInfo.objects().delete()
    for i in ujson.loads(await make_req2(prv))['data']['tradesTable']['rows']:
        # BTCHisInfo.objects(date=datetime.datetime.strptime(i['date'], "%m/%d/%Y")).delete()
        BTCHisInfo(**i).save()
    return Response(str(len(BTCHisInfo.objects())), headers={
        'Access-Control-Allow-Origin': '*',
        "Access-Control-Allow-Methods": "POST, GET, PUT, OPTIONS, DELETE",
        "Access-Control-Allow-Headers": "Access-Control-Allow-Origin"
    })

@app.get('/load')
async def load_1(typ: str='BTC'):
    # print(BTCHisInfo.objects().to_json())
    # j = ujson.loads(BTCHisInfo.objects().to_json())
    # print(j)
    pic = await sketch([j.get_dict() for j in BTCHisInfo.objects()], typ)
    return Response(pic.read(), media_type="image/png", headers={
        'Access-Control-Allow-Origin': '*',
        "Access-Control-Allow-Methods": "POST, GET, PUT, OPTIONS, DELETE",
        "Access-Control-Allow-Headers": "Access-Control-Allow-Origin"
    })

@app.get('/info')
async def info_1():
    l = [j.get_dict() for j in BTCHisInfo.objects()]
    # datetime.datetime.now().t
    # for p, i in enumerate(l):
    #     l[p]['date'] = i['date'].timestamp()
    return Response(ujson.dumps(l), headers={
        'Access-Control-Allow-Origin': '*',
        "Access-Control-Allow-Methods": "POST, GET, PUT, OPTIONS, DELETE",
        "Access-Control-Allow-Headers": "Access-Control-Allow-Origin"
    })

from bs4 import BeautifulSoup as BS

@app.get('/cryptocurrencies')
async def get_cryptocurrencies():
    async with aiohttp.ClientSession(trace_configs=[tracecfg]) as s:
        async with s.get(
            f'''https://www.nasdaq.com/market-activity/cryptocurrency''',
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
            # print(res)
        b = BS(res, 'html.parser')
        ccs = [i['data-symbol'] for i in b('tr', attrs={'data-asset-class':'cryptocurrency'})]
        print(ccs)

        return Response(ujson.dumps(ccs), headers={
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Methods": "POST, GET, PUT, OPTIONS, DELETE",
            "Access-Control-Allow-Headers": "Access-Control-Allow-Origin"
        })

import os
# import shlex
@app.get('/build/{b:path}')
async def file_proxy(b):
    print(os.getcwd())
    if '..' in b:
        return HTTPException(403, {'msg': '老师傅行行好别打了= ='})
    return FileResponse(f'{os.getcwd()}/build/{b.replace("..","")}')

if __name__ == '__main__':
    uvicorn.run(app)


# https://medium.com/swlh/building-an-amazing-cross-platform-pok%C3%A9dex-desktop-application-with-electron-react-and-5ed997a5c0f1