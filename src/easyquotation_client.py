# -*- coding:utf-8 -*-
#
# Author: Muyang Chen
# Date: 2022-12-16

import easyquotation

class EasyQuotationClient(object):
    def __init__(self):
        self.quotation = easyquotation.use('sina') # 新浪 ['sina'] 腾讯 ['tencent', 'qq'] 
        easyquotation.update_stock_codes()
        self.share_id_map = dict()
        self.__build_share_id_map()

    def __build_share_id_map(self):
        shares_list = self.quotation.market_snapshot(prefix=True)
        for s_id in shares_list:
            self.share_id_map[shares_list[s_id]['name']] = s_id

    def read_stock_data(self, name):
        if name not in self.share_id_map:
            return {}
        s_id = self.share_id_map[name]
        data = self.quotation.stocks(s_id, prefix = True)[s_id]
        return data

    def read_now_price(self, name):
        data = self.read_stock_data(name)
        if not data:
            return -1
        return data['now']
