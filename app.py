import json
from typing import Union
import redis
from redis.commands.json.path import Path
from ipwhois import IPWhois
from fastapi import FastAPI

r = redis.Redis(host='localhost', port=6379, db=0, password='eYVX7EwVmmxHLCDmwMtyKV83soLd2t81', username='default')
app = FastAPI()


@app.get("/{ip}")
def whois_ip(ip:str):
    # try:
        cache = r.json().get(ip)
        if cache:
            print("from cache")
            return cache
        else:
            request = json.dumps(IPWhois(ip).lookup_rdap())
            r.json().set(ip, Path.root_path(), request, decode_keys=False)
            r.expire(name=ip, time=3600)
            print("from whois")
            return request
    # except:
    #     return {}
