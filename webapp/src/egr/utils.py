import requests as r
import datetime
from typing import Literal
import time
import aiohttp
import asyncio

ENDPOIN = "http://egr.gov.by/api/v2/egr/getBaseInfoByPeriod/{}/{}"
NAME_1_ENDPOINT = 'http://egr.gov.by/api/v2/egr/getJurNamesByRegNum/{}'
NAME_2_ENDPOINT = 'http://egr.gov.by/api/v2/egr/getIPFIOByRegNum/{}'
VTELS_1_ENDPOINT = 'http://egr.gov.by/api/v2/egr/getAddressByRegNum/{}'
one_day_delta = datetime.timedelta(days=1)

def vnaim_fetcher(nkvob: Literal[1, 2], ngrn: int):
    if nkvob == 1:
        res = r.get(NAME_1_ENDPOINT.format(ngrn))
        if res.status_code != 200:
            return 'err'
        vnaim = res.json()[0].get('vnaim')
        return vnaim
    elif nkvob == 2:
        res = r.get(NAME_2_ENDPOINT.format(ngrn))
        if res.status_code != 200:
            return 'err'
        vnaim = res.json()[0].get('vfio')
        return vnaim
    return "err"

def vtels_fetcher(nkvob: Literal[1, 2], ngrn: int):
    print(VTELS_1_ENDPOINT.format(ngrn))
    res = r.get(VTELS_1_ENDPOINT.format(ngrn))
    if res.status_code != 200:
        return 'err'
    vtels = res.json()[0].get('vtels')
    return vtels

def egr_fetcher(start_date: datetime.datetime.date=None, stop_date: datetime.datetime.date=None)->list:
    if start_date is None:
        start_date = datetime.datetime.now().date() - one_day_delta
        
    if stop_date is None:
        start_date = datetime.datetime.now().date()
    start_date = start_date.strftime('%d.%m.%Y')
    stop_date = stop_date.strftime('%d.%m.%Y')
    print(start_date, stop_date)
    res = r.get(ENDPOIN.format(start_date, stop_date))
    if res.status_code != 200:
        return []
    return res.json()


def data_combiner(start_date: datetime.datetime.date=None, stop_date: datetime.datetime.date=None):
    egr_data = egr_fetcher(start_date, stop_date)
    result = []
    total = len(egr_data)
    # return
    for num, obj in enumerate(egr_data):
        ngrn = obj.get("ngrn")
        time.sleep(0.1)
        print("==========" + str(num) + f"============ of {total}")
        result.append({
            'ngrn': ngrn,
            'vnuzp': obj['nsi00212']['vnuzp'],
            'vnaim': vnaim_fetcher(obj['nsi00211']['nkvob'], ngrn),
            'vtels': vtels_fetcher(obj['nsi00211']['nkvob'], ngrn),
        })
    return result


