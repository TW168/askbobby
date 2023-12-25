# technical_indicators.py
import pandas_ta as ta
import pandas as pd

class TechnicalIndicators:
    def __init__(self) -> None:
        pass

    def calculate_indicators(self, data):
        """
        Calculate common technical indicators using pandas_ta.

        Parameters:
        data (DataFrame): A pandas DataFrame containing stock data.

        Returns:
        DataFrame: A new DataFrame with added columns for technical indicators.
        """
        try:
            # Ensure that the DataFrame is sorted by date
            data = data.sort_values(by='Date')

            # Define sample strategy 
            sample_strategy_definition = ta.Strategy(
                name="Custom Strategy",
                description="SMA 50,200, BBANDS, RSI, MACD, Volume SMA 20, OHLC4, EMA, DONCHIAN, and ADX",
                ta=[
                    {"kind": "sma", "length": 50},
                    {"kind": "sma", "length": 200},
                    {"kind": "bbands", "length": 20},
                    {"kind": "rsi"},
                    {"kind": "macd", "fast": 12, "slow": 26, "signal":9},
                    {"kind": "sma", "close": "volume", "length": 20, "prefix": "VOLUME"},
                    {"kind": "ohlc4"},
                    {"kind": "donchian", "lower_length": 10, "upper_length": 15},
                    {"kind": "ema", "close": "OHLC4", "length": 10, "suffix": "OHLC4"},
                    {"kind": "adx", "length":14},
                ]
            )

            # Apply sample_strategy_definition
            data.ta.strategy(sample_strategy_definition, append=True)
            return data

        except Exception as e:
            print(f"An error occurred while calculating technical indicators: {e}")
            return None

# Example usage
# Assuming 'df' is your stock data DataFrame
# technical_indicators = TechnicalIndicators()
# df_with_indicators = technical_indicators.calculate_indicators(df)
