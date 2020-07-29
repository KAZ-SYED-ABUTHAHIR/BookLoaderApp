""""
Module to generate a Proxy pool from https://free-proxy-list.net/
"""

import soupipy as spy
import random as rnd  

def getProxyPool() -> list:
    return [{'http':'http://' + prxy, 'https':'http://' + prxy} for prxy in
    spy.getSoup('https://free-proxy-list.net/#').find('textarea', class_='form-control').text.split('\n')[3:-1]]

proxyPool = getProxyPool()
    
def getRndProxy() -> dict:
    return rnd.choice(proxyPool)
