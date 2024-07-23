from email import header
from faulthandler import disable
from gettext import find
from webbrowser import Chrome
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# using selenium to send request for yahoo fin website

options = Options()
options.add_argument("--disable-notifications")

chrome = webdriver.Chrome('./data analysis_final project/chromedriver', chrome_options=options)
url = 'https://finance.yahoo.com/quote/%5EIXIC/history?period1=978307200&period2=1640995200&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true'
#headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
chrome.get(url)

for x in range(1,4):
    chrome.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(5)

sp = BeautifulSoup(chrome.page_source, 'lxml')

# find sp500 table
nasdaq = sp.find('table')

# find date
day = nasdaq.find_all('td', class_="Py(10px) Ta(start) Pend(10px)")

# find price and vol
price = nasdaq.find_all('td', class_="Py(10px) Pstart(10px)")

# assign to dif variable
stock_date = []
stock_open = []
stock_high = []
stock_low = []
stock_close = []
stock_aclose = []
stock_vol = []

# assign for dates
for i in range(len(day)):
    stock_date.append(day[i].text)

# assign for prices
for i in range(len(price)):
    if i % 6 == 0:
        stock_open.append(price[i].text)
    elif i % 6 == 1:
        stock_high.append(price[i].text)
    elif i % 6 == 2:
        stock_low.append(price[i].text)
    elif i % 6 == 3:
        stock_close.append(price[i].text)
    elif i % 6 == 4:
        stock_aclose.append(price[i].text)
    elif i % 6 == 5:
        stock_vol.append(price[i].text)    

# output to csv file

nasdaq_table = pd.DataFrame({
    "Date": stock_date,
    "Open": stock_open,
    "High": stock_high,
    "Low": stock_low,
    "Close": stock_close,
    "Adj Close": stock_aclose,
    "Volume": stock_vol,
})
nasdaq_table.to_csv('data analysis_final project/nasdaq_data.csv', index=False)


