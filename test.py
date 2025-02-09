from backtest.backtest import Backtest

# Run the backtest
bt = Backtest()
profit, profit_rate = bt.get_profit()
print(f"总收益：{profit}，收益率：{profit_rate}")