'''
@Description:
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
LastEditors: Please set LastEditors
LastEditTime: 2021-03-18 16:39:53
'''
#  基础模块
import sys
import json
import logging
#   selenium相关
#   threading
import threading
#   引入requests类
from DataGather import DataGather
from HouyiApi import HouyiApi
#   工具集
# import utils as mytools


# gather采集线程
class GatherThread(threading.Thread):
    def __init__(self, cookies_info: tuple, houyiapi: object):
        super().__init__()
        self.cookies_info = cookies_info
        self.api = houyiapi

    def run(self):
        conf_id, cookies = self.cookies_info
        #   开发平台数据采集
        gather = DataGather(cookies)
        accs = gather.listAccount() + gather.listAccountSpe()
        if not accs or len(accs) <= 0:
            self.api.up('notifyQqssoCookies', {'id': conf_id, 'run_res': 0})
        else:
            for ac in accs:
                data = gather.dataPlan(ac.get('account_id'))
                self.api.up('addQqSsoCampaign', data)
            self.api.up('notifyQqssoCookies', {'id': conf_id, 'run_res': 1})


'''
description: 日志初始化
return {*}
'''
def logInit():
    log_format = "%(asctime)s - %(levelname)s - %(message)s"  # 日志格式
    if "debug" == RUN_EVN.lower():
        log_file = './debug.log'
        log_level = logging.DEBUG
    else:
        log_file = './run.log'
        log_level = logging.WARNING
    logging.basicConfig(filename=log_file, level=log_level, format=log_format)


if __name__ == '__main__':
    global RUN_EVN
    # 登录界面的url
    try:
        RUN_EVN = sys.argv[1]
    except Exception:
        RUN_EVN = "product"
    #   获取后台cookies
    houyiapi = HouyiApi()
    conf_cookies = houyiapi.up('getQqssoCookies', '')
    for item in conf_cookies.get('Result', {}).get('List', []):
        try:
            cookies_info = (item.get('id'), json.loads(item.get('cookies')))
        except Exception:
            houyiapi.up('notifyQqssoCookies', {'id': item.get('id'), 'run_res': 0})
            continue
        thr = GatherThread(cookies_info, houyiapi)
        thr.start()
