"""
Drift Rebalancer

Asset class: Multi-Asset (Stocks)
Data source: Yahoo Finance (free)
Description: Maintains a target portfolio allocation and rebalances
when any position drifts beyond a configurable threshold.
"""

from datetime import datetime
from lumibot.strategies import Strategy
from lumibot.backtesting import YahooDataBacktesting


class DriftRebalancer(Strategy):
    parameters = {
        "targets": {
            "SPY": 0.40,   # 40% US large cap
            "QQQ": 0.25,   # 25% tech/growth
            "IWM": 0.15,   # 15% small cap
            "TLT": 0.15,   # 15% long-term bonds
            "GLD": 0.05,   # 5% gold
        },
        "drift_threshold": 0.03,  # 3% drift triggers rebalance
    }

    def initialize(self):
        self.sleeptime = "1D"

    def on_trading_iteration(self):
        targets = self.parameters["targets"]
        threshold = self.parameters["drift_threshold"]
        portfolio = self.portfolio_value

        # Calculate current weights
        needs_rebalance = self.first_iteration
        for symbol, target_weight in targets.items():
            position = self.get_position(symbol)
            if position:
                price = self.get_last_price(symbol)
                current_weight = (position.quantity * price) / portfolio
                drift = abs(current_weight - target_weight)
                if drift > threshold:
                    needs_rebalance = True
                    self.log_message(f"{symbol}: current {current_weight:.1%}, target {target_weight:.1%}, drift {drift:.1%}")
            else:
                needs_rebalance = True

        if not needs_rebalance:
            return

        # Rebalance
        self.log_message("Rebalancing portfolio")
        for symbol, target_weight in targets.items():
            price = self.get_last_price(symbol)
            if not price:
                continue

            target_qty = int((portfolio * target_weight) // price)
            position = self.get_position(symbol)
            current_qty = position.quantity if position else 0
            diff = target_qty - current_qty

            if diff > 0:
                self.submit_order(self.create_order(symbol, diff, "buy"))
            elif diff < 0:
                self.submit_order(self.create_order(symbol, abs(diff), "sell"))


if __name__ == "__main__":
    DriftRebalancer.backtest(
        YahooDataBacktesting,
        datetime(2020, 1, 1),
        datetime(2024, 1, 1),
        benchmark_asset="SPY",
    )
