"""
SMA Crossover

Asset class: Stocks
Data source: Yahoo Finance (free)
Description: Classic moving average crossover strategy. Buys when fast SMA
crosses above slow SMA, sells when it crosses below.
"""

from datetime import datetime
from lumibot.strategies import Strategy
from lumibot.backtesting import YahooDataBacktesting


class SmaCrossover(Strategy):
    parameters = {
        "symbol": "AAPL",
        "fast_period": 10,
        "slow_period": 30,
    }

    def initialize(self):
        self.sleeptime = "1D"

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        fast = self.parameters["fast_period"]
        slow = self.parameters["slow_period"]

        bars = self.get_historical_prices(symbol, slow + 5)
        if bars is None:
            return

        df = bars.df
        sma_fast = df["close"].rolling(fast).mean().iloc[-1]
        sma_slow = df["close"].rolling(slow).mean().iloc[-1]

        has_position = self.get_position(symbol) is not None

        if sma_fast > sma_slow and not has_position:
            price = self.get_last_price(symbol)
            quantity = int(self.portfolio_value * 0.95 // price)
            if quantity > 0:
                order = self.create_order(symbol, quantity, "buy")
                self.submit_order(order)
                self.log_message(f"BUY {quantity} {symbol} (fast SMA {sma_fast:.2f} > slow SMA {sma_slow:.2f})")

        elif sma_fast < sma_slow and has_position:
            self.sell_all()
            self.log_message(f"SELL ALL {symbol} (fast SMA {sma_fast:.2f} < slow SMA {sma_slow:.2f})")


if __name__ == "__main__":
    SmaCrossover.backtest(
        YahooDataBacktesting,
        datetime(2020, 1, 1),
        datetime(2024, 1, 1),
        benchmark_asset="SPY",
    )
