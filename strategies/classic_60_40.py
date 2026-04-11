"""
Classic 60/40 Portfolio

Asset class: Stocks + Bonds
Data source: Yahoo Finance (free)
Description: Classic 60% stocks (SPY), 40% bonds (TLT) portfolio
with quarterly rebalancing when drift exceeds 5%.
"""

from datetime import datetime
from lumibot.strategies import Strategy
from lumibot.backtesting import YahooDataBacktesting


class Classic6040(Strategy):
    parameters = {
        "stock_symbol": "SPY",
        "bond_symbol": "TLT",
        "stock_weight": 0.60,
        "bond_weight": 0.40,
        "rebalance_threshold": 0.05,
    }

    def initialize(self):
        self.sleeptime = "1D"
        self.vars.last_rebalance = None

    def on_trading_iteration(self):
        current_date = self.get_datetime().date()

        # Rebalance quarterly or on first iteration
        should_rebalance = (
            self.first_iteration
            or self.vars.last_rebalance is None
            or (current_date.month - self.vars.last_rebalance.month) % 3 == 0
            and current_date.day <= 5
        )

        if not should_rebalance:
            # Check drift
            stock_pos = self.get_position(self.parameters["stock_symbol"])
            if stock_pos:
                stock_value = stock_pos.quantity * self.get_last_price(self.parameters["stock_symbol"])
                current_stock_weight = stock_value / self.portfolio_value
                drift = abs(current_stock_weight - self.parameters["stock_weight"])
                if drift > self.parameters["rebalance_threshold"]:
                    should_rebalance = True
                    self.log_message(f"Drift {drift:.1%} exceeds threshold, rebalancing")

        if not should_rebalance:
            return

        portfolio = self.portfolio_value
        for symbol, weight in [
            (self.parameters["stock_symbol"], self.parameters["stock_weight"]),
            (self.parameters["bond_symbol"], self.parameters["bond_weight"]),
        ]:
            price = self.get_last_price(symbol)
            if not price:
                continue

            target_qty = int((portfolio * weight) // price)
            current_position = self.get_position(symbol)
            current_qty = current_position.quantity if current_position else 0
            diff = target_qty - current_qty

            if diff > 0:
                self.submit_order(self.create_order(symbol, diff, "buy"))
            elif diff < 0:
                self.submit_order(self.create_order(symbol, abs(diff), "sell"))

        self.vars.last_rebalance = current_date
        self.log_message(f"Rebalanced to {self.parameters['stock_weight']:.0%}/{self.parameters['bond_weight']:.0%}")


if __name__ == "__main__":
    Classic6040.backtest(
        YahooDataBacktesting,
        datetime(2020, 1, 1),
        datetime(2024, 1, 1),
        benchmark_asset="SPY",
    )
