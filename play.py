# stock_data_downloader.py
import pandas as pd
import streamlit as st
import yfinance as yf
import requests


# data = yf.download("AAPL", start="2023-12-01", end="2023-12-24")
# print(data)


# try:
#     ticker_information = yf.Ticker("googgg").info
#     print(ticker_information)
# except requests.exceptions.HTTPError as err:
#     print(f"HTTP error occurred. ")
# except Exception as err:
#     print(f"Other error occurred: {err}")



def get_ticker_info(ticker):
    """Retrieve Ticker object and information for a given stock ticker.

    Parameters:
    ticker (str): The ticker symbol of the stock.

    Returns:
    Tuple[Ticker, dict]: The Ticker object and a dictionary containing stock information.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        ticker_info = ticker_obj.info
         
        return ticker_obj, ticker_info

    except requests.exceptions.HTTPError as e:
        print(
            f"HTTP error occurred while fetching information for {ticker}")
        return None, None
    except Exception as e:
        print(
            f"An error occurred while fetching information for {ticker}")
        return None, None
    
obj, info = get_ticker_info(ticker="gggggg")
print('obj :',obj)
print('info :' ,info)
