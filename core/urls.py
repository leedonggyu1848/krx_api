from krx_api.util.constants import Constants

baseurl = 'http://data.krx.co.kr/comm/bldAttendant/'

class Cmd(Constants):
  JSON = 'getJsonData.cmd'
  RESOURCE = 'executeForResourceBundle.cmd'

class Bld(Constants):
  TICKER = 'dbms/comm/finder/finder_stkisu'
  INVESTOR_ACTIVITIES_ACC = 'dbms/MDC/STAT/standard/MDCSTAT02301'
  INVESTOR_ACTIVITIES_EACHDAY = 'dbms/MDC/STAT/standard/MDCSTAT02303'
  ALL_STOCKS = 'dbms/MDC/STAT/standard/MDCSTAT01501'