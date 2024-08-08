import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    options = Options()
    options.add_argument("--disable-notifications")
    service = Service("./data analysis_final project/web crawling/chromedriver")
    return webdriver.Chrome(service=service, options=options)

def scroll_page(driver, scrolls=50, delay=3):
    for _ in range(scrolls):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(delay)

def parse_table(soup):
    table = soup.find("table")
    dates = table.find_all("td", class_="Py(10px) Ta(start) Pend(10px)")
    prices = table.find_all("td", class_="Py(10px) Pstart(10px)")
    return dates, prices

def extract_data(dates, prices):
    stock_data = {
        "Date": [date.text for date in dates],
        "Open": [], "High": [], "Low": [], "Close": [], "Adj Close": [], "Volume": []
    }
    
    for i, price in enumerate(prices):
        stock_data[list(stock_data.keys())[1 + i % 6]].append(price.text)
    
    return stock_data

def main():
    urls = [
        "https://finance.yahoo.com/quote/%5EDJI/history?period1=1609459200&period2=1645401600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true", # dow jones
        "https://finance.yahoo.com/quote/%5EIXIC/history?period1=978307200&period2=1640995200&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true" # nasdaq
        'https://finance.yahoo.com/quote/%5EGSPC/history?period1=1609459200&period2=1645401600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true' # s&p500
        'https://finance.yahoo.com/quote/%5ETWII/history?period1=978307200&period2=1640995200&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true' # twii
    ]
    driver = setup_driver()

    for url in urls:
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            scroll_page(driver)
            
            soup = BeautifulSoup(driver.page_source, "lxml")
            dates, prices = parse_table(soup)
            stock_data = extract_data(dates, prices)
            
            nasdaq_table = pd.DataFrame(stock_data)
            nasdaq_table.to_csv("data analysis_final project/web crawling/dowj_data_test2.csv", index=False)
            print("Data successfully scraped and saved to CSV.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            driver.quit()

if __name__ == "__main__":
    main()