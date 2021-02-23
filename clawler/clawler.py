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

    def run(self):
        # 爬取的地址
        url = 'https://news.ifeng.com/c/special/7tPlDSzDgVk'
        strhtml = requests.get(url)
        soup = BeautifulSoup(strhtml.text,'lxml')
        alldata = re.search(r'{"borderImgUrl":"",".*(?=;)',strhtml.text)

        dic_alldata = json.loads(str(alldata.group()))
        print(type(dic_alldata))
        print(dic_alldata)
        #dt = lj['dataList']
        #print(dt[0])
        #print(d['leiji'][0])
        #dt['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        # 全国累计
        self.insertLeiji(leijitwomonthdata=dic_alldata['leiji'],leijidata=dic_alldata['yiqing_v2']['dataList'][15])
        print(dic_alldata['yiqing_v2']['dataList'][15])

        # print(d)
        # print(d['borderImgUrl'])
        # print(d['customization']['data']['name'])
        #print(type(mes_dict))
        #print(soup.prettify())
        #data = soup.select('#root > div > div.data_header_27UAPS09 > div.sum1_1pU-jgIe > div.num1_3n92B7R8 > span:nth-child(2)')
        #print(strhtml.text)
        #print(data.)

    # 存储全国累计
    def insertLeiji(self,leijitwomonthdata,leijidata):
        timestamp = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        leijitwomonthdata['timestamp'] = timestamp
        self.db.insert(collection='leijitwomonth',data = leijitwomonthdata)
        leiji = {'dataList':leijidata,'timestamp':timestamp}
        self.db.insert(collection='leiji',data = leiji)

if __name__ == '__main__':
    clawler = clawler()
    clawler.run()