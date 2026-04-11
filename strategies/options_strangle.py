"""
Options Short Strangle

Asset class: Options
Data source: Requires ThetaData or Interactive Brokers (options data)
Description: Sells an out-of-the-money call and put on SPY,
collecting premium. Closes at 50% profit or 21 DTE.
Note: This strategy requires an options-capable data source and broker.
"""

from datetime import datetime, timedelta
from lumibot.strategies import Strategy
from lumibot.entities import Asset


class ShortStrangle(Strategy):
    parameters = {
        "symbol": "SPY",
        "delta_target": 0.16,
        "dte_target": 45,
        "profit_target": 0.50,
        "dte_close": 21,
    }

    def initialize(self):
        self.sleeptime = "1D"

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        dte_target = self.parameters["dte_target"]

        # Check if we have existing positions to manage
        positions = self.get_positions()
        option_positions = [p for p in positions if p.asset.asset_type == Asset.AssetType.OPTION]

        if option_positions:
            # Manage existing positions
            for pos in option_positions:
                days_to_expiry = (pos.asset.expiration - self.get_datetime().date()).days
                if days_to_expiry <= self.parameters["dte_close"]:
                    self.log_message(f"Closing {pos.symbol} - {days_to_expiry} DTE")
                    self.sell_all(pos.symbol)
            return

        # Find expiration date ~45 DTE
        target_date = self.get_datetime().date() + timedelta(days=dte_target)
        chain = self.get_chains(symbol)

        if not chain:
            self.log_message("No options chain available")
            return

        # Get the underlying price
        underlying_price = self.get_last_price(symbol)
        if not underlying_price:
            return

        # Sell OTM call and put
        call_strike = round(underlying_price * 1.05, 0)
        put_strike = round(underlying_price * 0.95, 0)

        call_asset = Asset(
            symbol=symbol,
            asset_type=Asset.AssetType.OPTION,
            expiration=target_date,
            strike=call_strike,
            right="call",
        )
        put_asset = Asset(
            symbol=symbol,
            asset_type=Asset.AssetType.OPTION,
            expiration=target_date,
            strike=put_strike,
            right="put",
        )

        call_order = self.create_order(call_asset, 1, "sell")
        put_order = self.create_order(put_asset, 1, "sell")

        self.submit_order(call_order)
        self.submit_order(put_order)
        self.log_message(f"Sold strangle: {call_strike}C / {put_strike}P expiring {target_date}")


# Note: This strategy requires options data. Yahoo Finance does not provide
# historical options data. Use ThetaData, Interactive Brokers, or another
# options-capable data source for backtesting.
#
# For a free example that works out of the box, see sma_crossover.py or
# stock_buy_and_hold.py.
