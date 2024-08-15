from imports import *

#Dummy variables
stock_ticker = 'AMZN'
market_ticker = '^GSPC'


class RiskAnalyzer:

    # Initizialize with stock and market tickers, and lookbback period (set to two years by default)
    def __init__(self, stock_ticker, market_ticker, lookback_days=2*365):
        self.stock_ticker = stock_ticker
        self.market_ticker = market_ticker
        self.lookback_days = lookback_days
        self.stock_returns = None
        self.market_returns = None
    
    # Fetch historical prices and compute daily returns
    def get_returns(self, ticker):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days = self.lookback_days)
        prices = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
        returns = prices.pct_change().dropna()
        return returns
    
    # Load returns for stock and market index
    def load_returns(self):
        self.stock_returns = self.get_returns(self.stock_ticker)
        self.market_returns = self.get_returns(self.market_ticker)
    
    # Calculate beta (stock volatility relative to the market)
    def calculate_beta(self):
        self.load_returns()
        beta = np.cov(self.stock_returns, self.market_returns)[0, 1] / np.var(self.market_returns)
        return beta
    
    # Calculate systematic risk (market-related risk)
    def calculate_systematic_risk(self):
        beta = self.calculate_beta()
        systematic_risk = beta**2 * np.var(self.market_returns)
        return systematic_risk

    # Calculate unsystematic risk (stock-specific risk)
    def calculate_unsystematic_risk(self):
        self.load_returns()
        total_risk = np.var(self.stock_returns)
        systematic_risk = self.calculate_systematic_risk()
        unsystematic_risk = total_risk - systematic_risk
        return unsystematic_risk