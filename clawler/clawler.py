import requests
from bs4 import BeautifulSoup
import re

url = 'https://news.ifeng.com/c/special/7tPlDSzDgVk'
strhtml = requests.get(url)
soup = BeautifulSoup(strhtml.text,'lxml')

data = re.search(r'\\',strhtml.text)
print(data)
#print(soup.prettify())
#data = soup.select('#root > div > div.data_header_27UAPS09 > div.sum1_1pU-jgIe > div.num1_3n92B7R8 > span:nth-child(2)')
#print(strhtml.text)
#print(data.)