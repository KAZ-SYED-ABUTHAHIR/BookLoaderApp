""""
Module to generate a Proxy pool from https://free-proxy-list.net/
"""
import requests
import soupipy as spy
import random as rnd  


def getProxyPool() -> list:
    return [{'http':'http://' + prxy, 'https':'https://' + prxy} for prxy in
    spy.getSoup('https://free-proxy-list.net/#').find('textarea', class_='form-control').text.split('\n')[3:-1]]

proxyPool = getProxyPool()
    
def getRndProxy(https=True) -> dict:
    return {'https': rnd.choice(proxyPool)['https']} if https else{'http': rnd.choice(proxyPool)['http']}
    

