from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backtest import backtest

# # Run the backtest
# bt = Backtest()
# profit, profit_rate = bt.get_profit()
# print(f"总收益：{profit}，收益率：{profit_rate}")

StartTime = "2023-01-01"
EndTime = "2023-12-31"
StockId = "000001"


class Server(viewsets.GenericViewSet):

    @action(detail=False, methods=['post'])
    def set_cycle_and_stock(self, request, *args, **kwargs):
        print("请求设置周期和股票")
        # data = json.loads(request.body)
        data = request.data
        startTime = data['startTime']
        endTime = data['endTime']
        stockId = data['stockId']
        try:
            StartTime = startTime
            EndTime = endTime
            StockId = stockId
            resp = {
                'status': True,
                'message': '成功设置周期和股票'
            }
            print("成功设置周期和股票")
        except:
            resp = {
                'status': False,
                'message': '设置周期和股票失败'
            }
            print("设置周期和股票失败")
        return Response(resp)

    @action(detail=False, methods=['get'])
    def get_result(self, request, *args, **kwargs):
        print("请求获取结果")
        try:
            # Run the backtest
            bt = backtest.Backtest()
            profit, profit_rate = bt.get_profit()
            print(f"总收益：{profit}，收益率：{profit_rate}")
            resp = {
                'status': True,
                'data': {
                    'profit': profit,
                    'profitRate': profit_rate
                },
                'message': '成功获取结果'
            }
        except:
            resp = {
                'status': False,
                'message': '获取结果失败'
            }
            print("获取结果失败")
        return Response(resp)
