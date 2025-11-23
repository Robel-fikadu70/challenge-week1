# Week 1 Challenge: Financial News & Stock Price Analysis

This repository contains the interim submission for the Week 1 Challenge. The goal is to analyze financial news sentiment and correlate it with stock market movements for Nova Financial Solutions.

## 📂 Folder Structure
The project is organized as follows:
*   **.github/workflows**: CI/CD configuration for automated testing.
*   **data**: Contains the `raw_analyst_rating.csv` and `yfinance_data` (ignored by Git).
*   **notebooks**: Jupyter notebooks for EDA and visualization.
*   **src**: Modular Python scripts for data loading and analysis.
*   **tests**: Unit tests to ensure code stability.

## 🚀 Setup Instructions
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Robel-fikadu70/challenge-week1
    cd challenge-week1
    ```

2.  **Create and activate virtual environment**:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 📊 Work Accomplished (Interim)
**Task 1: Git & Environment**
- [x] Set up Python environment with Virtualenv.
- [x] Implemented modular code structure (src/notebooks).
- [x] Configured GitHub Actions (CI/CD).

**Task 2: Quantitative Analysis**
- [x] Created `DataLoader` class to handle CSV ingestion.
- [x] Performed EDA on News Data (Headline lengths, Publisher stats).
- [x] Calculated Technical Indicators (SMA, RSI) for AAPL stock.

## 🧪 Running the Code
To see the analysis, run the Jupyter Notebook:
```bash
jupyter notebook notebooks/1_eda_news.ipynb