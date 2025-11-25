import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from collections import Counter

# Try importing talib, handle failure gracefully
try:
    import talib
    HAS_TALIB = True
except ImportError:
    HAS_TALIB = False
    print("TA-Lib not found. Using Pandas for technical indicators.")

class NewsAnalyzer:
    """
    Class for performing NLP and EDA on news data.
    """
    def __init__(self, df):
        self.df = df.copy()
        # Ensure date is datetime
        if 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce', utc=True)

    def get_headline_stats(self):
        """Calculates basic statistics for headline lengths."""
        self.df['headline_len'] = self.df['headline'].apply(len)
        return self.df['headline_len'].describe()

    def get_top_publishers(self, n=10):
        """Returns the top N publishers."""
        return self.df['publisher'].value_counts().head(n)

    def extract_common_keywords(self, n=20):
        """Task 1: Text Analysis - Identify common keywords."""
        all_text = " ".join(self.df['headline'].dropna().astype(str))
        words = all_text.lower().split()
        # Filter out short boring words (stopwords-ish)
        words = [w for w in words if len(w) > 4] 
        return Counter(words).most_common(n)

    def perform_sentiment_analysis(self):
        """Task 3: Calculate sentiment polarity (-1 to 1)."""
        # Using TextBlob for sentiment
        def get_sentiment(text):
            return TextBlob(str(text)).sentiment.polarity
        
        print("Calculating sentiment scores... this might take a moment.")
        self.df['sentiment_score'] = self.df['headline'].apply(get_sentiment)
        return self.df

    def get_daily_sentiment(self):
        """Aggregates sentiment by date."""
        # Group by date (normalize to just the day, remove time)
        self.df['date_only'] = self.df['date'].dt.date
        daily_sentiment = self.df.groupby('date_only')['sentiment_score'].mean()
        return daily_sentiment

class StockAnalyzer:
    """
    Class for calculating technical indicators on stock data.
    """
    def __init__(self, df):
        self.df = df.copy()

    def calculate_daily_returns(self):
        """Task 3: Calculate daily percentage change."""
        self.df['daily_return'] = self.df['Close'].pct_change()
        return self.df

    def add_moving_average(self, window=20):
        """Adds SMA."""
        if HAS_TALIB:
            self.df[f'SMA_{window}'] = talib.SMA(self.df['Close'], timeperiod=window)
        else:
            self.df[f'SMA_{window}'] = self.df['Close'].rolling(window=window).mean()
        return self.df

    def add_rsi(self, window=14):
        """Adds RSI."""
        if HAS_TALIB:
            self.df['RSI'] = talib.RSI(self.df['Close'], timeperiod=window)
        else:
            delta = self.df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            self.df['RSI'] = 100 - (100 / (1 + rs))
        return self.df

    def add_macd(self):
        """Task 2: Adds MACD (Moving Average Convergence Divergence)."""
        if HAS_TALIB:
            macd, macdsignal, macdhist = talib.MACD(self.df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
            self.df['MACD'] = macd
            self.df['MACD_Signal'] = macdsignal
        else:
            # Pandas implementation
            exp1 = self.df['Close'].ewm(span=12, adjust=False).mean()
            exp2 = self.df['Close'].ewm(span=26, adjust=False).mean()
            self.df['MACD'] = exp1 - exp2
            self.df['MACD_Signal'] = self.df['MACD'].ewm(span=9, adjust=False).mean()
        return self.df