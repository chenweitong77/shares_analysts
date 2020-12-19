# -*- coding:utf-8 -*-
#
# Author: Muyang Chen
# Date: 2020-12-09

import tushare as ts
import datetime


class TushareClient(object):
    def __init__(self, token):
        ts.set_token(token)
        self.pro = ts.pro_api()

    def read_stock_basic(self):
        data = self.pro.query(
            'stock_basic', exchange='', list_status='L',
            fields='ts_code,symbol,name,area,industry,list_date')
        return data

    def read_daily_data(self, ts_code, pre_day_num=0):
        cur_data = datetime.datetime.now()
        cur_data = cur_data + datetime.timedelta(days=-1)
        pre_data = cur_data + datetime.timedelta(days=-pre_day_num)
        cur_data = '%s' % cur_data.strftime('%Y%m%d')
        pre_data = '%s' % pre_data.strftime('%Y%m%d')
        data = self.pro.daily(
            ts_code=ts_code, start_date=pre_data, end_date=cur_data)
        return data
