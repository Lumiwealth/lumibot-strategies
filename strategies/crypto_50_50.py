"""
Crypto 50/50

Asset class: Crypto
Data source: Yahoo Finance (free)
Description: Equal-weight Bitcoin and Ethereum portfolio with monthly rebalancing.
"""

from datetime import datetime
from lumibot.strategies import Strategy
from lumibot.backtesting import YahooDataBacktesting


class Crypto5050(Strategy):
    parameters = {
        "assets": ["BTC-USD", "ETH-USD"],
        "rebalance_day": 1,
    }

    def initialize(self):
        self.sleeptime = "1D"
        self.vars.last_rebalance_month = None

    def on_trading_iteration(self):
        current_date = self.get_datetime().date()
        assets = self.parameters["assets"]
        weight = 1.0 / len(assets)

        # Rebalance on first iteration or first trading day of each month
        if (
            not self.first_iteration
            and self.vars.last_rebalance_month == current_date.month
        ):
            return

        portfolio = self.portfolio_value
        for symbol in assets:
            price = self.get_last_price(symbol)
            if not price:
                continue

            target_qty = (portfolio * weight) / price
            current_position = self.get_position(symbol)
            current_qty = current_position.quantity if current_position else 0
            diff = target_qty - current_qty

            if abs(diff * price) < 10:
                continue

            if diff > 0:
                self.submit_order(self.create_order(symbol, diff, "buy"))
            elif diff < 0:
                self.submit_order(self.create_order(symbol, abs(diff), "sell"))

        self.vars.last_rebalance_month = current_date.month
        self.log_message(f"Rebalanced: equal weight across {assets}")


if __name__ == "__main__":
    Crypto5050.backtest(
        YahooDataBacktesting,
        datetime(2021, 1, 1),
        datetime(2024, 1, 1),
        benchmark_asset="BTC-USD",
    )
