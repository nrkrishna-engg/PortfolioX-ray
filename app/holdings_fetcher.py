import requests
from bs4 import BeautifulSoup
from utils import convert_us_format

def get_etf_holdings_from_stock_analysis(ticker):
    url = f"https://stockanalysis.com/etf/{ticker}/holdings/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        rows = table.find("tbody").find_all("tr")

        holdings = {}
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 2:
                stock_symbol = columns[1].text.strip()
                percent = columns[3].text.strip()
                holdings[stock_symbol] = convert_us_format(percent)
        return holdings
    except:
        return None

def get_mutualfunds_holdings_from_stock_analysis(ticker):
    url = f"https://stockanalysis.com/quote/mutf/{ticker}/holdings/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        rows = table.find("tbody").find_all("tr")

        holdings = {}
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 2:
                stock_symbol = columns[1].text.strip()
                percent = columns[3].text.strip()
                holdings[stock_symbol] = convert_us_format(percent)
        return holdings
    except:
        return None
