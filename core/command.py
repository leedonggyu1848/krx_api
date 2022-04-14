import requests
import json
from core.urls import Bld, Cmd, baseurl
    
class WrongStockCode(Exception):
    pass

class Ticker:
  def __init__(self, data):
      self.full_code = data['full_code'] # KR<code>
      self.code = data['short_code'] # stock code
      self.stock_name = data['codeName'] # stock name 
      self.market_code = data['marketCode']
      self.market_name_KOR = data['marketName']
      self.market_name_ENG = data['marketEngName']
  
  def get_finder(self)->str:
      return f"{self.code}/{self.stock_name}"

class ApiCommand:
  _locale = 'ko_KR'
  
  def __new__(cls, *args, **kargs):
    if not hasattr(cls, "_instance"):
      cls._instance = super().__new__(cls)
    return cls._instance
  
  def all_stocks(self, type=1)->dict:
    opt = ('ALL', 'STK', 'KSQ', 'KNX')
    pass
    #todo
    

  def ticker(self, code:str)->Ticker:
    print(Cmd.JSON)
    url = baseurl+Cmd.JSON
    payload = {  
      'locale' : self._locale,
      'bld' : Bld.TICKER,
      'typeNo' : 0,
      'searchText' : code
    }
    
    res = requests.get(url, data=payload)
    try:
        data = json.loads(res.text)['block1']
    except:
        raise ConnectionError
    if len(data) == 0:
        raise WrongStockCode
    return Ticker(data[0])

  def investor_activities_acc(
      self, 
      ticker:Ticker, 
      start:str, 
      end=None,
    )->dict:
    start = self.closest_business_work_date(start)
    if not end:
        end = start
    else:
      end = self.closest_business_work_date(end)
    url = baseurl+Cmd.JSON
    payload = {
        'bld' : Bld.INVESTOR_ACTIVITIES_ACC,
        'locale': self._locale,
        'isuCd': ticker.full_code,
        'strtDd': start,
        'endDd': end,
    }
    res = requests.get(url, data=payload)
    try:
        data = json.loads(res.text)['output']
    except:
        raise ConnectionError
    return data

  
  def investor_activities_eachday(
      self, 
      ticker:Ticker, 
      start:str, 
      end=None,
      type=1,
      bid=3,
    )->dict:
    '''
    type => 1: 거래량 | 2: 거래대금
    bid => 1: 매수 | 2:매도 | 3: 순매수
    '''

    start = self.closest_business_work_date(start)
    if not end:
      end = start
    else:
      end = self.closest_business_work_date(end)
    url = baseurl+Cmd.JSON
    payload = {
      'bld': Bld.INVESTOR_ACTIVITIES_EACHDAY,
      'locale': self._locale,
      'trdVolVal': type,
      'askBid': bid,
      'isuCd': ticker.full_code,
      'strtDd': start,
      'endDd': end,
      }

    res = requests.get(url, data=payload)
    try:
        data = json.loads(res.text)['output']
    except:
        raise ConnectionError
    return data
  
  def closest_business_work_date(self, date:str)->str:
    url = baseurl+Cmd.RESOURCE
    query = {
      'baseName':'krx.mdc.i18n.component',
      'key':'B161.bld',
      'inDate':date
    }

    res = requests.get(url, params=query)
    try:
      data = json.loads(res.text)['result']['output']['bis_work_dt']
    except:
        raise ConnectionError
    return data