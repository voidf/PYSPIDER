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

@app.get('/')
async def master():
    return await make_req(8)

if __name__ == '__main__':
    uvicorn.run(app)
