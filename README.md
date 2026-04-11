# Lumibot Community Strategies

A collection of trading strategies for [Lumibot](https://github.com/Lumiwealth/lumibot). Browse, fork, backtest, and share your own.

## Strategies

| Strategy | Asset Class | Description |
|----------|------------|-------------|
| [Stock Buy and Hold](strategies/stock_buy_and_hold.py) | Stocks | Simple buy-and-hold with portfolio allocation |
| [SMA Crossover](strategies/sma_crossover.py) | Stocks | Classic moving average crossover signal |
| [Stock Momentum](strategies/stock_momentum.py) | Stocks | Momentum rotation across a stock universe |
| [Classic 60/40](strategies/classic_60_40.py) | Stocks + Bonds | Traditional 60% stocks, 40% bonds with rebalancing |
| [Crypto 50/50](strategies/crypto_50_50.py) | Crypto | Equal-weight Bitcoin and Ethereum |
| [Options Strangle](strategies/options_strangle.py) | Options | Short strangle strategy for premium collection |
| [Drift Rebalancer](strategies/drift_rebalancer.py) | Multi-Asset | Rebalance portfolio when drift exceeds threshold |

## Quick Start

```bash
pip install lumibot

# Run any strategy
python strategies/sma_crossover.py
```

## How to Contribute

We welcome community strategies! To submit yours:

1. Fork this repo
2. Add your strategy to the `strategies/` folder
3. Include a docstring with:
   - Strategy description (1-2 sentences)
   - Asset class (stocks, options, crypto, futures, forex)
   - Required data source (Yahoo is free, or specify ThetaData/Polygon/etc.)
   - Expected behavior (what it buys/sells and why)
4. Make sure it runs with `python strategies/your_strategy.py`
5. Open a pull request

### Strategy Template

```python
"""
My Strategy Name

Asset class: Stocks
Data source: Yahoo Finance (free)
Description: Brief description of what this strategy does.
"""

from datetime import datetime
from lumibot.strategies import Strategy
from lumibot.backtesting import YahooDataBacktesting

class MyStrategy(Strategy):
    parameters = {}

    def initialize(self):
        self.sleeptime = "1D"

    def on_trading_iteration(self):
        # Your strategy logic here
        pass

if __name__ == "__main__":
    MyStrategy.backtest(
        YahooDataBacktesting,
        datetime(2023, 1, 1),
        datetime(2024, 1, 1),
    )
```

## Resources

- [Lumibot Documentation](https://lumibot.lumiwealth.com/)
- [Lumibot GitHub](https://github.com/Lumiwealth/lumibot)
- [BotSpot Platform](https://botspot.trade/) (deploy strategies with AI, no code required)
- [Discord Community](https://discord.gg/TmMsJCKY3T)

## License

MIT
