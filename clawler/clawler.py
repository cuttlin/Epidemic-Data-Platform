import requests
from bs4 import BeautifulSoup
import re
import json
import ast
import datetime
from db import DB
import random
import time
from selenium import webdriver


class clawler:
    def __init__(self):
        self.db = DB()
        self.session = requests.session()
        self.user_agent_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
        ]
        self.rumorurl = "https://vp.fact.qq.com/loadmore?artnum=0&page=%s"
        self.header = {
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3269.3 Safari/537.36"
        }

    # 爬取谣言
    def clawrumors(self):
        timestamp = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        df_all = list()
        for rumorurl in [self.rumorurl % i for i in range(80)]:
            data_list = requests.get(rumorurl, headers = self.header).json()["content"]  #爬取的数据
            tempdata = [{'title':df["title"], 'date':df["date"], 'result':df["result"], 'explain':df["explain"], \
                         'tag':df["tag"],'author':df["author"],'authordesc':df["authordesc"],'abstract':df["abstract"]} for df in data_list]
            df_all.extend(tempdata)
        data = {'timestamp': timestamp, 'data': df_all}
        self.db.insert(collection='rumors', data=data)


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
    print(time.time())
    clawler = clawler()
    clawler.run()
    clawler.clawHistory(place='河北')
    clawler.clawHistory(place='湖北')
    clawler.clawRealtime()
    #clawler.clawrumors()
    print(time.time())