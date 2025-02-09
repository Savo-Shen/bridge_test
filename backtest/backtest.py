import os
import pandas as pd
#导入backtrader框架  
import backtrader as bt 

# 创建策略继承bt.Strategy 
class SavoStrategy(bt.Strategy): 

    def log(self, txt, dt=None): 
        # 记录策略的执行日志  
        dt = dt or self.datas[0].datetime.date(0) 
        print('%s, %s' % (dt.isoformat(), txt)) 

    def __init__(self): 
        # 保存收盘价的引用  
        self.dataclose = self.datas[0].close
        # 12日移动平均线
        self.m1 = bt.indicators.SimpleMovingAverage(self.datas[0], period=12) 
        # 26日移动平均线
        self.m2 = bt.indicators.SimpleMovingAverage(self.datas[0], period=26)
        self.order = None

    def next(self): 
        # if self.order:  # 检查是否有指令等待执行
        #     return
        
        cash = 1000000  # 获取当前现金
        price = self.data.close[0]  # 获取当前收盘价
        investment = cash * 0.2  # 计算买入金额（本金的20%）
        size = investment / price  # 计算买入数量

        # 记录收盘价  
        
        # 买入条件：当12日的价格均线穿越(>)26日的价格均线时买入。
        if self.m1[0] > self.m2[0] and self.m1[-1] < self.m2[-1]:  
            if size > 0:
                self.log('BUY, %.2f' % size)
                self.log('Close, %.2f' % self.dataclose[0]) 
                self.order = self.buy(size=size)  # 买入
                self.log(f"12日均线：{self.m1[0]}，26日均线：{self.m2[0]}")
        

        # 卖出条件：当价格跌破26均线时卖出。
        if self.m1[0] < self.m2[0] and self.m1[-1] > self.m2[-1]:  
            if size > 0 and self.position.size > size:
                self.log('SELL, %.2f' % size)
                self.log('Close, %.2f' % self.dataclose[0]) 
                self.order = self.sell(size=size)  # 卖出
            elif self.position.size > 0:
                self.log('SELL, %.2f' % self.position.size)
                self.log('Close, %.2f' % self.dataclose[0]) 
                self.order = self.sell(size=self.position.size)
            self.log(f"12日均线：{self.m1[0]}，26日均线：{self.m2[0]}")
        # self.log(f"持仓：{self.position.size}")

class Backtest:
    def __init__(self):
        self.cerebro = bt.Cerebro() 
        self.cerebro.broker = bt.brokers.BackBroker(slip_perc=0.0001)
        self.cerebro.broker.setcash(1000000) 
        self.cerebro.addstrategy(SavoStrategy) 

 
        current_work_dir = os.path.dirname(__file__)  # 当前文件所在的目录
        
        data_path = os.path.join(current_work_dir, 'res/data/000001历史数据.csv')  # 再加上它的相对路径，这样可以动态生成绝对路径

        # 数据预处理
        # 如果csv要读取Volume，其中数据就必须是数字
        df = pd.read_csv(data_path)
        df.drop(columns=['涨跌幅'], inplace=True)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df["volume"] = df["volume"].replace({"M": "*1e6", "K": "*1e3"}, regex=True).map(pd.eval).astype(int)
        df = df.sort_values(by="datetime")
        df.set_index("datetime", inplace=True)
        data = bt.feeds.PandasData(dataname=df)

        # 回测
        self.cerebro.adddata(data)
        print('组合期初资金: %.2f' % self.cerebro.broker.getvalue()) 
        self.cerebro.run() 
        print('组合期末资金: %.2f' % self.cerebro.broker.getvalue())
        self.cerebro.plot() # 绘制图形
        
        # 返回总收益和收益率
        self.profit = self.cerebro.broker.getvalue() -  1000000
        self.profit_rate = (self.cerebro.broker.getvalue() -  1000000) / 1000000

    def get_profit(self):
        return self.profit, self.profit_rate
