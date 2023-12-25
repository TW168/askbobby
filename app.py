# app.py
import pandas as pd
import streamlit as st
from utils.stock_data_downloader import StockDataDownloader
from utils.chart_plotter import ChartPlotter
from utils.technical_indicators import TechnicalIndicators

# Set up the Streamlit page
st.set_page_config(
    page_title="Bob",
    page_icon="📊",
    layout='wide',
)
st.title('This is Bob')


def format_number_abbreviated(number):
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


# Create an instance of StockDataDownloader
data_downloader = StockDataDownloader()

# Expander for getting stock data
with st.expander('Get Stock Data', expanded=True):
    # Get user input
    ticker = st.text_input('Ticker ', value='AAPL')
    start_date = st.date_input(
        'Start Date', value=pd.to_datetime('1900-01-01'))
    end_date = st.date_input('End Date', value=pd.to_datetime('today'))

# Expander for displaying stock information
with st.expander(f'{ticker.upper()} - Stock Information', expanded=True):
    try:
        # Use download_stock_info method
        stock_info = data_downloader.download_stock_info(
            ticker, start_date, end_date)

        if 'data' in stock_info and stock_info['data'] is not None:
            # Check if 'company_info' is in stock_info
            if 'company_info' in stock_info:
                # Display company information
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    col1.metric('Company Name', stock_info['company_info'].get(
                        'shortName', 'N/A'))
                    col1.metric(
                        'Sector', stock_info['company_info'].get('sector'))
                    col1.metric(
                        'Exchange', stock_info['company_info'].get("exchange"))
                    col1.metric(
                        'Currency', stock_info['company_info'].get('currency'))
            else:
                st.write("No company information available.")

            # Stock Valuation Measures
            with col2:
                col2.metric('Beta', stock_info['company_info'].get('beta'))
                market_cap = stock_info['valuation_measures'].get('marketCap')
                formatted_market_cap = format_number_abbreviated(market_cap)
                col2.metric('Market Cap', formatted_market_cap)

            # Yahoo! recommendation
            with col3:
                col3.metric('Yahoo! Recommendation Mean',
                            stock_info['company_info'].get("recommendationMean"))
                col3.metric('Yahoo! Recommend',
                            stock_info['company_info'].get('recommendationKey'))

            # Stock Financial information
            with col4:
                total_cash = stock_info['financial_highlights'].get(
                    'totalCash')
                formatted_total_cash = format_number_abbreviated(total_cash)
                col4.metric('Total Cash', formatted_total_cash)
                total_debt_to_equity = stock_info['financial_highlights'].get(
                    'debtToEquity')
                formatted_total_debt_to_equity = f"{total_debt_to_equity:.1f}%" if total_debt_to_equity is not None else "N/A"
                col4.metric('Total Debt/Equity (mrq)',
                            formatted_total_debt_to_equity)
        else:
            st.warning(
                f"No information available for the stock with ticker '{ticker}'.")

    except Exception as e:
        st.error(f"An error occurred while fetching stock information: {e}")

    # Add the "Brought to you by Yahoo! Finance" with a link and smaller font
    # st.markdown("<small>Brought to you by [Yahoo! Finance](https://finance.yahoo.com/)</small>", unsafe_allow_html=True)

# Company Business Summary
with st.expander(f'{ticker.upper()} - Business Summary', expanded=False):
    if 'company_info' in stock_info:
        st.write(stock_info['company_info'].get("longBusinessSummary"))
    else:
        st.write("No company information available.")


# Expander for displaying stock closing price and indicators
with st.expander(f'{ticker.upper()} - Stock Closing Price and Indicators', expanded=True):
    # Check if 'data' is in stock_info
    if 'data' in stock_info and stock_info['data'] is not None:
        # Create an instance of ChartPlotter
        plotter = ChartPlotter()

        # Plot stock data using Plotly
        plotter.plot_stock_data(stock_info['data'])

        # Use the TechnicalIndicators class to calculate indicators
        technical_indicators = TechnicalIndicators()
        df_with_indicators = technical_indicators.calculate_indicators(stock_info['data'])

        # Use the ChartPlotter class to plot Bollinger Bands
        if df_with_indicators is not None and not df_with_indicators.empty:
            col1, col2 = st.columns(2)

            with col1:
                # Extract Bollinger Bands data from df_with_indicators
                bollinger_bands_data = df_with_indicators[['Date', 'Close', 'BBU_20_2.0', 'BBL_20_2.0']]
                # Create a line chart for Bollinger Bands
                bollinger_fig = plotter.plot_bollinger_bands(bollinger_bands_data)
                # Show the plot using Streamlit
                st.plotly_chart(bollinger_fig)

                # Extract RSI data from df_with_indicators
                rsi_data = df_with_indicators[['Date', 'Close', 'RSI_14']]
                rsi_fig = plotter.plot_rsi_and_close(rsi_data)
                # Show the plot using Streamlit
                st.plotly_chart(rsi_fig)
                st.markdown(body="RSI readings range from zero to 100, with readings above 70 generally interpreted as indicating overbought conditions and readings below 30 indicating oversold conditions.")

            with col2:
                # Extract MACD data from df_with_indicators
                macd_data = df_with_indicators[['Date', 'Close', 'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9']]
                macd_fig = plotter.plot_macd_indicators(macd_data)
                # Show the plot using Streamlit
                st.plotly_chart(macd_fig)
                st.markdown(body="When the MACD yellow line crosses above the signal red line (to buy) or falls below it (to sell).", unsafe_allow_html=True)

                # Extract Moving Average data from df_with_indicators
                sma_data = df_with_indicators[['Date', 'Close', 'SMA_50', 'SMA_200']]
                # Create a line chart for Moving Averages
                sma_fig = plotter.plot_simple_moving_averages(sma_data)
                # Show the plot using Streamlit
                st.plotly_chart(sma_fig)

        else:
            st.warning("No data available for plotting.")
    else:
        st.warning("No data available.")
