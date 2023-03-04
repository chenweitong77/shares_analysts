# -*- coding:utf-8 -*-
#
# Author: Muyang Chen
# Date: 2022-12-16
#
# 基于easyquotation方法，对部分股票价格进行监控，当出现大涨获大跌时进行报警.

import time
import winsound
from easyquotation_client import EasyQuotationClient


def alarm(freq, duration):
    # freq: 报警声音频率.
    # duration: 报警持续时间.
    freq = max(int(freq), 300)
    freq = min(int(freq), 800)
    winsound.Beep(int(freq), int(duration))
    time.sleep(duration / 1000)


def add_alarm_record(name, diff_ratio, alarm_dict):
    if abs(diff_ratio) < 0.05 and abs(diff_ratio) >= 0.03:
        alarm_dict[name] = 0.05
    elif abs(diff_ratio) < 0.08 and abs(diff_ratio) >= 0.05:
        alarm_dict[name] = max(alarm_dict[name], 0.08)
    elif abs(diff_ratio) < 0.1 and abs(diff_ratio) >= 0.08:
        alarm_dict[name] = max(alarm_dict[name], 0.1)
    elif abs(diff_ratio) >= 0.1:
        alarm_dict[name] = max(alarm_dict[name], 0.2)


def print_diff_ratio(name, now_price, diff_ratio):
    _str = "%.2f%%" % (diff_ratio * 100)
    if diff_ratio > 0:
        _str = '+' + _str
    print(name, now_price, _str)


if __name__ == '__main__':
    easyquotation_client = EasyQuotationClient()
    name_list = ('比亚迪', '中国平安', '森马服饰', '中芯国际', '沪深300ETF', '科创板50ETF', '上证指数')

    # 获取前一天股价信息.
    pre_day_map = dict()
    for name in name_list:
        s = easyquotation_client.read_stock_data(name)
        if not s:
            continue
        pre_day_close_price = s['close']
        pre_day_map[name] = pre_day_close_price

    # 持续获取当前股价.
    alarm_dict = dict()
    while True:
        print("===== %s =====" % time.ctime())
        for name in name_list:
            if name not in pre_day_map:
                continue

            pre_day_close_price = pre_day_map[name]
            now_price = easyquotation_client.read_now_price(name)
            diff_ratio = (now_price - pre_day_close_price) / \
                pre_day_close_price
            print_diff_ratio(name, now_price, diff_ratio)
            if abs(diff_ratio) < 0.03:
                # 变化幅度较小，不报警.
                continue
            elif name in alarm_dict and diff_ratio < alarm_dict[name]:
                # 该区间已报警过，不报警.
                continue
            else:
                alarm(abs(diff_ratio) * 10000, 1000)
                add_alarm_record(name, diff_ratio, alarm_dict)

        print(alarm_dict)
        print("================ END ================")
        time.sleep(30)
