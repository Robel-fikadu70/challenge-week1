import pandas as pd
import os

class DataLoader:
    """
    A class to handle loading and basic processing of financial news 
    and stock market datasets.
    """
    
    def __init__(self, data_path):
        """
        Initializes the DataLoader with the path to the data directory.
        
        Args:
            data_path (str): Path to the folder containing data files.
        """
        self.data_path = data_path

    def load_news_data(self, filename):
        """
        Loads the news dataset from a CSV file.
        
        Args:
            filename (str): Name of the CSV file (e.g., 'raw_analyst_rating.csv').
            
        Returns:
            pd.DataFrame: Loaded data with converted date column.
        """
        file_path = os.path.join(self.data_path, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"Loading news data from {file_path}...")
        df = pd.read_csv(file_path)
        
        # Convert date to datetime immediately to ensure data quality
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
            
        return df

    def load_stock_data(self, stock_symbol):
        """
        Loads stock data for a specific symbol.
        
        Args:
            stock_symbol (str): Ticker symbol (e.g., 'AAPL').
            
        Returns:
            pd.DataFrame: Stock data.
        """
        # Construct path assuming yfinance_data folder structure
        file_path = os.path.join(self.data_path, 'yfinance_data', f'{stock_symbol}.csv')
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Stock file not found for: {stock_symbol}")

        print(f"Loading stock data for {stock_symbol}...")
        df = pd.read_csv(file_path)
        
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            
        return df