import requests
from bs4 import BeautifulSoup
import re
import json
import ast
import datetime
from db import DB


class clawler:
    def __init__(self):
        self.db = DB()

    # 爬取实时播报
    def clawRealtime(self):
        timestamp = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        url = 'http://auto.sohu.com/sptopic/20-182-kb-d0c/2020pneumoniaReatime.html'
        strhtml = requests.get(url)
        soup = BeautifulSoup(strhtml.text, 'lxml')
        alldata = re.search(r'{"title":"实时播报",".*(?=;)', strhtml.text)
        dic_alldata = json.loads(str(alldata.group()))
        data = {'timestamp': timestamp, 'data': dic_alldata}
        self.db.insert(collection='realtimenews', data=data)

    # 爬取省市历史数据
    def clawHistory(self,place):
        timestamp = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province='+place
        strhtml = requests.get(url)
        soup = BeautifulSoup(strhtml.text, 'lxml')

        dic_alldata = json.loads(str(strhtml.text))
        provincehistory = {'timestamp':timestamp,'place':place,'dataList':dic_alldata['data']}
        self.db.insert(collection='provincehistory', data=provincehistory)


    def run(self):
        # 爬取的地址
        url = 'https://news.ifeng.com/c/special/7tPlDSzDgVk'
        strhtml = requests.get(url)
        soup = BeautifulSoup(strhtml.text,'lxml')
        alldata = re.search(r'{"borderImgUrl":"",".*(?=;)',strhtml.text)

        dic_alldata = json.loads(str(alldata.group()))


        #print(dic_alldata)

        # 全国累计
        self.insertLeiji(leijitwomonthdata=dic_alldata['leiji'],leijidata=dic_alldata['yiqing_v2']['dataList'][15])

        # 全国省市实时情况
        self.insertYiqingv2(data=dic_alldata['yiqing_v2'])

        # 全球累计实时情况
        self.insertWorlddata(leijidata=dic_alldata['leiji']['dataList'],countrydata=dic_alldata['yiqing_v2']['dataList'][29])




    # 存储全国累计
    def insertLeiji(self,leijitwomonthdata,leijidata):
        timestamp = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        leijitwomonthdata['timestamp'] = timestamp
        self.db.insert(collection='leijitwomonth',data = leijitwomonthdata)
        leiji = {'dataList':leijidata,'timestamp':timestamp}
        self.db.insert(collection='leiji',data = leiji)

    # 存储全国省市实时情况
    def insertYiqingv2(self,data):
        timestamp = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        data['timestamp'] = timestamp
        self.db.insert(collection='yiqingv2',data=data)
        city = {'timestamp': timestamp}
        #city['dataList']

    # 存储全球累计实时情况
    def insertWorlddata(self,leijidata,countrydata):
        timestamp = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        data = {'timestamp':timestamp,'leijidata':leijidata,'countrydata':countrydata}
        self.db.insert(collection='leijiworld',data=data)

if __name__ == '__main__':
    clawler = clawler()
    clawler.run()
    clawler.clawHistory(place='河北')
    clawler.clawHistory(place='湖北')
    clawler.clawRealtime()