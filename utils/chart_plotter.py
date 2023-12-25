# chart_plotter.py
import streamlit as st
# import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import pandas as pd
from datetime import datetime, timedelta


class ChartPlotter():
    
    def plot_stock_data(self, data):
        """
        Plot stock closing price as a line and volume as a bar chart using Plotly.

        Parameters:
        data (DataFrame): A pandas DataFrame containing stock data.
        """
        try:
            # Check if data is not empty
            if data is not None and not data.empty:
                # Create subplot with a secondary y-axis
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                # Add line chart for closing price
                fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Closing Price'),
                              secondary_y=False)

                # Add bar chart for volume
                fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], name='Volume', opacity=0.5),
                              secondary_y=True)

                # Update axis labels and title
                fig.update_layout(title_text='Stock Closing Price and Volume',
                                  xaxis_title='Date',
                                  yaxis_title='Closing Price',
                                  yaxis2_title='Volume')

                # Show the plot
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.warning("No data available for plotting.")

        except Exception as e:
            st.error(f"An error occurred while plotting the stock data: {e}")
        
    def plot_bollinger_bands(self, bollinger_data, chart_title="Bollinger Bands 1 year"):
        """
        Plot Bollinger Bands along with closing price using Plotly Express.

        Parameters:
        bollinger_data (DataFrame): DataFrame with Date, Close, BBU_20_2.0, and BBL_20_2.0 columns.

        Returns:
        Figure: A Plotly Express figure.
        """
        try:
            # Calculate the date 365 days ago from the last date in your data
            one_year_ago = bollinger_data['Date'].max() - timedelta(days=365)

            # Filter rows for the last 365 days
            bollinger_data = bollinger_data[bollinger_data['Date'] >= one_year_ago]
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Add lines for Bollinger Bands
            fig.add_trace(go.Scatter(x=bollinger_data['Date'], y=bollinger_data['BBU_20_2.0'], mode='lines', name='BBU_20_2.0', line=dict(color='gray')), secondary_y=False)
            fig.add_trace(go.Scatter(x=bollinger_data['Date'], y=bollinger_data['BBL_20_2.0'], mode='lines', name='BBL_20_2.0', line=dict(color='gray')), secondary_y=False)
            fig.add_trace(go.Scatter(x=bollinger_data['Date'], y=bollinger_data['Close'], mode='lines', name='Close', line=dict(color='cyan')), secondary_y=False)

            # Update layout to include the chart title
            fig.update_layout(
                title_text=chart_title,
                yaxis_title='Close Price'
                )
            
            return fig # Return the Plotly figure directly, without converting to a dictionary
        except Exception as e:
            print(f"An error occurred while plotting Bollinger Bands: {e}")
            return None


    def plot_macd_indicators(self, macd_data, chart_title="MACD Indicators Last 90 days"):
        """
        Plot MACD indicators using Plotly Express.

        Parameters:
        bollinger_data (DataFrame): DataFrame with Date, MACD_8_21_9, MACDh_8_21_9, MACDs_821_9 columns.

        Returns:
        Figure: A Plotly Express figure.
        """
        try:
            # Calculate the date 365 days ago from the last date in your data
            one_month_ago = macd_data['Date'].max() - timedelta(days=90)

            # Filter rows for the last 365 days
            macd_data = macd_data[macd_data['Date'] >= one_month_ago]
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Add lines for MACD-related indicators
            fig.add_trace(go.Scatter(x=macd_data['Date'], y=macd_data['MACD_12_26_9'], mode='lines', name='MACD_12_26_9', line=dict(color='yellow')), secondary_y=True)
            #fig.add_trace(go.Scatter(x=macd_data['Date'], y=macd_data['MACDh_9_26_9'], mode='lines', name='MACDh_9_26_9'), secondary_y=True)
            fig.add_trace(go.Scatter(x=macd_data['Date'], y=macd_data['MACDs_12_26_9'], mode='lines', name='MACDs_12_26_9', line=dict(color='red')), secondary_y=True)
            fig.add_trace(go.Scatter(x=macd_data['Date'],y=macd_data['Close'], mode='lines', name='Close', line=dict(color='cyan')), secondary_y=False)

            # Update layout to include the chart title
            fig.update_layout(
                title_text=chart_title,
                yaxis_title='Close Price',
                yaxis2_title='MACD'

                )

            return fig  # Return the Plotly figure directly, without converting to a dictionary
        except Exception as e:
            print(f"An error occurred while plotting MACD Indicators: {e}")
            return None

    def plot_rsi_and_close(self, data, chart_title="RSI and Close Price Last 90 Days"):
        """
        Plot RSI and close price using Plotly.

        Parameters:
        data (DataFrame): DataFrame with Date, Close, and RSI columns.

        Returns:
        Figure: A Plotly figure.
        """
        try:
            # Calculate the date 90 days ago from the last date in your data
            ninety_days_ago = data['Date'].max() - timedelta(days=90)

            # Filter rows for the last 90 days
            data = data[data['Date'] >= ninety_days_ago]
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Add lines for Close price and RSI
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close', line=dict(color='cyan')), secondary_y=False)
            fig.add_trace(go.Scatter(x=data['Date'], y=data['RSI_14'], mode='lines', name='RSI_14', line=dict(color='yellow')), secondary_y=True)

            # Update layout to include the chart title and axis titles
            fig.update_layout(
                title_text=chart_title,
                yaxis_title='Close Price',
                yaxis2_title='RSI_14'
            )

            return fig  # Return the Plotly figure directly, without converting to a dictionary
        except Exception as e:
            print(f"An error occurred while plotting RSI and Close Price: {e}")
            return None
        
    def plot_simple_moving_averages(self, data, chart_title="Simple Moving Average 50 and 200 days Last 500 days"):
        try:
            # Calculate the date 500 days ago from the last date in your data
            fivehundred_days_ago = data['Date'].max() - timedelta(days=500)

            # Filter rows for the last 500 days
            data = data[data['Date'] >= fivehundred_days_ago]
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Add lines for Close price and RSI
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close', line=dict(color='cyan')), secondary_y=False)
            fig.add_trace(go.Scatter(x=data['Date'], y=data['SMA_50'], mode='lines', name='SMA_50', line=dict(color='yellow')), secondary_y=True)
            fig.add_trace(go.Scatter(x=data['Date'], y=data['SMA_200'], mode='lines', name='SMA_200', line=dict(color='pink')), secondary_y=True)

            # Update layout to include the chart title and axis titles
            fig.update_layout(
                title_text=chart_title,
                yaxis_title='Close Price',
                yaxis2_title='SMA'
            )

            return fig  # Return the Plotly figure directly, without converting to a dictionary
        except Exception as e:
            print(f"An error occurred while plotting Simple Moving Average 50 and 200 days: {e}")
            return None
