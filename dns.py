#!/usr/bin/python3

from http import client
from base64 import b64encode
from sys import argv
from urllib import request
from re import compile
from urllib import parse
import config as cfg

def push_addess(name, address, alias):

    txt_data = "oa1:xkr recipient_address=" + address + "; recipient_name=" + alias + ";"

    conn = client.HTTPSConnection(cfg.whm["host"], cfg.whm["port"])
    credentials = cfg.whm["user"] + ":" + cfg.whm["passwd"];
    myAuth = b64encode(credentials.encode('ascii')).decode('ascii')
    authHeader = {'Authorization':'Basic ' + myAuth}
    conn.request('GET', '/json-api/cpanel?cpanel_jsonapi_version=2&cpanel_jsonapi_module=ZoneEdit&cpanel_jsonapi_func=add_zone_record&domain=xkr.se&class=IN&type=TXT&txtdata=' + parse.quote(txt_data) + '&name=' + name + '.xkr.se.&ttl=3600', headers=authHeader)
    myResponse = conn.getresponse()
    print(myResponse.getcode())
    data = myResponse.read()
    if myResponse.getcode() != 200:
        print('did not succeed')
    print (type(data.decode('ascii')))

############################################

def check_address(address):
    conn = client.HTTPSConnection(cfg.whm["host"], cfg.whm["port"])
    credentials = cfg.whm["user"] + ":" + cfg.whm["passwd"];
    myAuth = b64encode(credentials.encode('ascii')).decode('ascii')
    authHeader = {'Authorization':'Basic ' + myAuth}
    conn.request('GET', '/json-api/cpanel?cpanel_jsonapi_version=2&cpanel_jsonapi_module=ZoneEdit&cpanel_jsonapi_func=fetchzones', headers=authHeader)
    myResponse = conn.getresponse()
    print(myResponse.getcode())
    data = myResponse.read()
    if myResponse.getcode() != 200:
        print('did not succeed')
    print(data)
    try:
    	return '"' + address in data.decode('ascii')
    except UnicodeError:
        return '"' + address in data.decode('utf-8')
    else:
        pass


from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the XKR OpenAlias creator API. Use /add/username.xkr.se/SEKReXVgap3DWm1wKbL3okNZwu9SmFfubB2GLZkKer1pBQ22eqZN3VC2BKeotjfi58WN8k6VUhBqLD5NRWfwD9diTj5cxKrLfTM255a0fd7d7f6ead78a3586f3f7937caa18d809e8dad586900fd0122abe3bd651/nickname to register an address.!"

@app.route('/add/<name>/<address>/<alias>')
def add_address(name,address,alias):
    if (not check_address(name)):
        push_addess(name, address, alias)
    return 'You are reading ' + name + address + alias

if __name__ == '__main__':
    app.run(debug=True)
