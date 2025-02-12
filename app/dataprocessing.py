import pandas as pd
from holdings_fetcher import get_etf_holdings_from_stock_analysis, get_mutualfunds_holdings_from_stock_analysis
from utils import convert_us_format, update_dict, return_top_k, add_other

def process_excel_file(df):
    # Skip header if it exists (first row contains column names)
    if df.iloc[0].iloc[0].upper() not in ['ETF', 'MF', 'IS']:
        df = df.iloc[1:]
    
    etfs = []
    mutualfunds = []
    stocks = []
    
    for _, row in df.iterrows():
        fund_type, ticker, amount = row.iloc[0].upper(), row.iloc[1], float(row.iloc[2])       
        fund_entry = {"ticker": ticker, "amount": amount}
        
        if fund_type == "ETF":
            etfs.append(fund_entry)
        elif fund_type == "MF":
            mutualfunds.append(fund_entry)
        elif fund_type == "IS":
            stocks.append(fund_entry)
    
    return etfs, mutualfunds, stocks


def calculate_exposure(etfs, mutualfunds, stocks):
    exposure = {}
    total_portfolio = sum(fund["amount"] for fund in etfs + mutualfunds + stocks)

    for fund in etfs:
        ticker = fund["ticker"]
        allocation = fund["amount"] / total_portfolio
        etf_holdings = get_etf_holdings_from_stock_analysis(ticker) or {}
        exposure = update_dict(exposure, {k: v * allocation for k, v in etf_holdings.items()})

    for fund in mutualfunds:
        ticker = fund["ticker"]
        allocation = fund["amount"] / total_portfolio
        mf_holdings = get_mutualfunds_holdings_from_stock_analysis(ticker) or {}
        exposure = update_dict(exposure, {k: v * allocation for k, v in mf_holdings.items()})

    for stock in stocks:
        ticker = stock["ticker"]
        allocation = 100 * stock["amount"] / total_portfolio
        exposure[ticker] = exposure.get(ticker, 0) + allocation

    exposure = return_top_k(exposure, 30)
    exposure = add_other(exposure)

    return exposure