"""
Stock Momentum Rotation

Asset class: Stocks
Data source: Yahoo Finance (free)
Description: Ranks a universe of stocks by 12-month momentum.
Holds the top N performers, rebalances monthly.
"""

from datetime import datetime
from lumibot.strategies import Strategy
from lumibot.backtesting import YahooDataBacktesting


class MomentumRotation(Strategy):
    parameters = {
        "universe": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "JPM", "V", "UNH"],
        "top_n": 3,
        "lookback_days": 252,
    }

    def initialize(self):
        self.sleeptime = "1D"
        self.vars.last_rebalance = None

    def on_trading_iteration(self):
        current_date = self.get_datetime().date()

        # Rebalance monthly (first trading day of each month)
        if self.vars.last_rebalance and current_date.month == self.vars.last_rebalance.month:
            return

        universe = self.parameters["universe"]
        lookback = self.parameters["lookback_days"]
        top_n = self.parameters["top_n"]

        # Calculate momentum for each stock
        momentum_scores = {}
        for symbol in universe:
            bars = self.get_historical_prices(symbol, lookback + 5)
            if bars is not None and len(bars.df) >= lookback:
                df = bars.df
                momentum_scores[symbol] = df["close"].iloc[-1] / df["close"].iloc[0] - 1

        if not momentum_scores:
            return

        # Pick top N by momentum
        ranked = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)
        winners = [symbol for symbol, score in ranked[:top_n]]

        self.log_message(f"Top {top_n} by momentum: {winners}")

        # Sell anything not in winners
        for position in self.get_positions():
            if position.symbol not in winners:
                self.sell_all(position.symbol)

        # Equal-weight the winners
        target_value = self.portfolio_value / top_n
        for symbol in winners:
            price = self.get_last_price(symbol)
            if price and price > 0:
                target_qty = int(target_value // price)
                current_position = self.get_position(symbol)
                current_qty = current_position.quantity if current_position else 0

                diff = target_qty - current_qty
                if diff > 0:
                    order = self.create_order(symbol, diff, "buy")
                    self.submit_order(order)
                elif diff < 0:
                    order = self.create_order(symbol, abs(diff), "sell")
                    self.submit_order(order)

        self.vars.last_rebalance = current_date


if __name__ == "__main__":
    MomentumRotation.backtest(
        YahooDataBacktesting,
        datetime(2020, 1, 1),
        datetime(2024, 1, 1),
        benchmark_asset="SPY",
    )
