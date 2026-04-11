"""
Stock Buy and Hold

Asset class: Stocks
Data source: Yahoo Finance (free)
Description: Buys a single stock and holds it. The simplest possible strategy.
"""

from datetime import datetime
from lumibot.strategies import Strategy
from lumibot.backtesting import YahooDataBacktesting


class BuyAndHold(Strategy):
    parameters = {"symbol": "SPY"}

    def initialize(self):
        self.sleeptime = "1D"

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        price = self.get_last_price(symbol)
        self.log_message(f"{symbol}: ${price:.2f}")

        if not self.get_position(symbol):
            quantity = int(self.portfolio_value // price)
            order = self.create_order(symbol, quantity, "buy")
            self.submit_order(order)


if __name__ == "__main__":
    BuyAndHold.backtest(
        YahooDataBacktesting,
        datetime(2020, 1, 1),
        datetime(2024, 1, 1),
        benchmark_asset="SPY",
    )
