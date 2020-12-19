# -*- coding:utf-8 -*-
#
# Author: Muyang Chen
# Date: 2020-12-09

import os
import time

import config
from tushare_pro_client import TushareClient


if __name__ == '__main__':
    base_path = os.path.dirname(__file__)
    tushare_client = TushareClient(config.token)

    # 获取股票列表.
    stock_basic = tushare_client.read_stock_basic()
    stock_basic_path = os.path.join(base_path, 'stock_basic.csv')
    stock_basic.to_csv(stock_basic_path, sep="\t", header=False)

    # 获取所有股票前一天数据
    daily_data_path = os.path.join(base_path, 'daily_data.csv')
    for i, ts_code in enumerate(stock_basic['ts_code']):
        daily_data = tushare_client.read_daily_data(ts_code)
        if i == 0:
            daily_data.to_csv(daily_data_path, sep="\t", header=False)
        else:
            daily_data.to_csv(daily_data_path, sep="\t",
                              header=False, mode='a')
        if (i+1) % 500 == 0:
            time.sleep(60)
