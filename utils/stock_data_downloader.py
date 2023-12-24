# stock_data_downloader.py
# import pandas as pd
import streamlit as st
import yfinance as yf

class StockDataDownloader:
    def __init__(self):
        pass

    def _get_ticker_info(self, ticker):
        """Retrieve Ticker object and information for a given stock ticker.

        Parameters:
        ticker (str): The ticker symbol of the stock.

        Returns:
        Tuple[Ticker, dict]: The Ticker object and a dictionary containing stock information.
        """
        try:
            ticker_obj = yf.Ticker(ticker)
            ticker_info = ticker_obj.info

            if ticker_info is None:
                st.error(f"No information found for ticker symbol: {ticker}")
                return None, None
            else:
                return ticker_obj, ticker_info

        except Exception as e:
            st.error(
                f"An error occurred while fetching information for {ticker}:")
            return None, None

    def format_number_abbreviated(self, number):
            """
            Format a number in an abbreviated form based on its magnitude.

            Parameters:
            number (float): The number to be formatted.

            Returns:
            str: The formatted string representing the number in abbreviated form (e.g., T, B, M, K).
            """
            try:
                if number is None:
                    return "N/A"

                abs_number = abs(number)

                if abs_number >= 1e12:
                    return f'{number / 1e12:.2f} T'
                elif abs_number >= 1e9:
                    return f'{number / 1e9:.2f} B'
                elif abs_number >= 1e6:
                    return f'{number / 1e6:.2f} M'
                elif abs_number >= 1e3:
                    return f'{number / 1e3:.2f} K'
                else:
                    return f'{number:.2f}'

            except Exception as e:
                # Handle any unexpected exceptions
                st.error(f"An error occurred while formatting the number: {e}")
                return "Error"

    @st.cache_resource
    def download_stock_info(_self, ticker, start_date=None, end_date=None):
        """Retrieve stock information for a given ticker, including data, company info, valuation measures, and financial highlights.

        Parameters:
        ticker (str): The ticker symbol of the stock.
        start_date (datetime): The start date of the date range for stock data (default: None).
        end_date (datetime): The end date of the date range for stock data (default: None).

        Returns:
        dict: A dictionary containing stock information.
        """
        result = {}

        # Download stock data
        try:
            data = yf.download(ticker, start=start_date, end=end_date)

            if data.empty:
                st.error(f"No data found for ticker symbol: {ticker}")
                result['data'] = None
            else:
                data.reset_index(inplace=True)
                result['data'] = data

            # Retrieve company information
            ticker_obj, ticker_info = _self._get_ticker_info(ticker)

            if ticker_info is None:
                result['company_info'] = None
            else:
                company_dict = {
                    'sector': ticker_info.get('sector', 'N/A'),
                    'longBusinessSummary': ticker_info.get('longBusinessSummary', 'N/A'),
                    'auditRisk': ticker_info.get('auditRisk', 'N/A'),
                    'beta': ticker_info.get('beta', 'N/A'),
                    'trailingPE': ticker_info.get('trailingPE', 'N/A'),
                    'forwardPE': ticker_info.get('forwardPE', 'N/A'),
                    'currency': ticker_info.get('currency', 'N/A'),
                    'exchange': ticker_info.get('exchange', 'N/A'),
                    'shortName': ticker_info.get('shortName', 'N/A'),
                    'recommendationMean': ticker_info.get("recommendationMean", 'N/A'),
                    'recommendationKey': ticker_info.get("recommendationKey", 'N/A')
                }
                result['company_info'] = company_dict

            # Retrieve valuation measures
            if ticker_info is None:
                result['valuation_measures'] = None
            else:
                valuation_dict = {
                    'marketCap': ticker_info.get('marketCap'),
                    'trailingPE': ticker_info.get("trailingPE"),
                    'forwardPE': ticker_info.get("forwardPE"),
                    'pegRatio': ticker_info.get("pegRatio")
                }
                result['valuation_measures'] = valuation_dict

            # Retrieve financial highlights
            if ticker_info is None:
                result['financial_highlights'] = None
            else:
                highlights_dict = {
                    "profitMargins": ticker_info.get("profitMargins"),
                    'totalCash': ticker_info.get("totalCash"),
                    "totalRevenue": ticker_info.get("totalRevenue"),
                    "debtToEquity": ticker_info.get("debtToEquity"),
                    'totalDebt': ticker_info.get("totalDebt"),
                    'totalRevenue': ticker_info.get('totalRevenue'),
                    'debtToEquity': ticker_info.get('debtToEquity'),
                    'earningsGrowth': ticker_info.get('earningsGrowth')
                }
                result['financial_highlights'] = highlights_dict

        except Exception as e:
            st.error(f"An error occurred: {e}")
            result = {key: None for key in result.keys()}

        return result

# Usage example:
# data_downloader = StockDataDownloader()
# result = data_downloader.download_stock_info('AAPL', start_date=pd.to_datetime('2022-01-01'), end_date=pd.to_datetime('2022-12-31'))
# print(result)
