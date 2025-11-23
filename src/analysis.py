import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Try importing talib, handle failure gracefully
try:
    import talib
    HAS_TALIB = True
except ImportError:
    HAS_TALIB = False
    print("TA-Lib not found. Using Pandas for technical indicators.")

class NewsAnalyzer:
    """
    Class for performing Exploratory Data Analysis (EDA) on news data.
    """
    def __init__(self, df):
        self.df = df

    def get_headline_stats(self):
        """Calculates basic statistics for headline lengths."""
        self.df['headline_len'] = self.df['headline'].apply(len)
        return self.df['headline_len'].describe()

    def get_top_publishers(self, n=10):
        """Returns the top N publishers by article count."""
        return self.df['publisher'].value_counts().head(n)

    def get_daily_publication_counts(self):
        """Returns the number of articles published per day."""
        # Ensure date is datetime index
        if not isinstance(self.df.index, pd.DatetimeIndex):
            self.df = self.df.set_index('date')
        
        # Resample by Day ('D') and count
        daily_counts = self.df.resample('D')['headline'].count()
        return daily_counts

class StockAnalyzer:
    """
    Class for calculating technical indicators on stock data.
    """
    def __init__(self, df):
        self.df = df

    def add_moving_average(self, window=20):
        """Adds a Simple Moving Average (SMA) column."""
        if HAS_TALIB:
            self.df[f'SMA_{window}'] = talib.SMA(self.df['Close'], timeperiod=window)
        else:
            self.df[f'SMA_{window}'] = self.df['Close'].rolling(window=window).mean()
        return self.df

    def add_rsi(self, window=14):
        """Adds a Relative Strength Index (RSI) column."""
        if HAS_TALIB:
            self.df['RSI'] = talib.RSI(self.df['Close'], timeperiod=window)
        else:
            # Basic RSI calculation using Pandas if TA-Lib is missing
            delta = self.df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            self.df['RSI'] = 100 - (100 / (1 + rs))
        return self.df