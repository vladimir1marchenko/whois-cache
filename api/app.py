import json
from typing import Union
import redis
from redis.commands.json.path import Path
from ipwhois import IPWhois
import whois
from fastapi import FastAPI

r = redis.Redis(host='cache', port=6379, db=0, password='eYVX7EwVmmxHLCDmwMtyKV83soLd2t81', username='default')
app = FastAPI()


@app.get("/whois/ip/{ip}")
def whois_ip(ip:str):
    try:
        cache = r.json().get(ip)
        if cache:
            return cache
        else:
            request = json.loads(json.dumps(IPWhois(ip).lookup_rdap()))
            print(request)
            print(type(request))
            r.json().set(ip, Path.root_path(), request, decode_keys=False)
            r.expire(name=ip, time=3600)
            return request
    except:
        return {}

@app.get("/whois/domain/{domain}")
def whois_domain(domain:str):
    try:
        cache = r.json().get(domain)
        if cache:
            print("from cache")
            return cache
        else:
            request = json.loads(json.dumps(whois.whois(domain), indent=4, sort_keys=True, default=str))
            r.json().set(domain, Path.root_path(), request, decode_keys=False)
            r.expire(name=domain, time=3600)
            return request
    except:
        return {}


@app.get("/")
def root():
    return {"message": "Hello!"}