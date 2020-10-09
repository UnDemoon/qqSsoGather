'''
@Description: oppo数据采集类
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
@LastEditors: Demoon
@LastEditTime: 2020-07-01 11:36:41
'''
import json
import requests
import datetime
import utils as mytools


class DataGather:
    def __init__(self, cookie):
        print(cookie)
        self.colloctConf = {
            'get_portal_data': {
                'url': 'https://sso.e.qq.com/login/get_portal_data',
                'data': {
                    "service_tag": "10"
                }
            },
            'campaign_data': {
                'url': 'https://ad.qq.com/ap/report/campaign_list?',
                'data': {
                    "biz_filter": {
                        "status": 999
                    },
                    "rpt_filter": {
                        "time_dimension": 3,
                        "time_range": {
                            "start_date": "20201009",
                            "end_date": "20201009"
                        },
                        "time_line": 1
                    },
                    "order_by": {},
                    "page": 1,
                    "page_size": 20,
                    "data": ["list"]
                }
            }
        }
        self.accounts = []
        #   配置requests session
        sess = requests.session()  # 新建session
        c = requests.cookies.RequestsCookieJar()  # 添加cookies到CookieJar
        for i in cookie:
            c.set(i["name"], i['value'])
            if i['name'] == 'oadstk':
                self.oadstk = i['value']
        sess.cookies.update(c)  # 更新session里cookies
        self.req = sess

    #   get 方法
    def _subGet(self, url):
        res = {}
        res = self.req.get(url)
        return res

    #   post 方法
    def _post(self, url, para):
        res = self._subPost(url, para)
        while (res.get('code') != 0) and (res.get('errno') != 0):
            mytools.randomSleep()
            res = self._subPost(url, para)
        return res

    #   post子方法
    def _subPost(self, url, para):
        res = {}
        try:
            r = self.req.post(url, para)
            res = r.json()
            print(res)
        except BaseException as e:
            print(str(e))
        return res

    # 获取用户列
    def listAccount(self):
        self.req.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-length": "20",
            "content-type": "application/json; charset=UTF-8",
            "origin": "https: //sso.e.qq.com",
            "referer": "https: //sso.e.qq.com/login/portal?service_tag=10&sso_redirect_uri=https%3A%2F%2Fe.qq.com%2Fads%2F",
            "sec-ch-ua": '"Google Chrome";v="87", "\"Not;A\\Brand";v="99", "Chromium";v="87"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4270.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        cf = self.colloctConf
        data = self._post(cf['get_portal_data']['url'], json.dumps(cf['get_portal_data']['data']))
        self.accounts = data['data'][0]['account_list']
        return self.accounts

    #   获取推广计划数据
    def dataPlan(self):
        parm = {
            "g_tk": "1205599923",
            "owner": "17777724",
            "advertiser_id": "17777724",
            "trace_id": "294e3e58-14ab-ef91-dd0d-0d03b660cf13",
            "g_trans_id": "d7629a32-00a0-8d08-3f1f-b9c4a648b19a",
            "unicode": "1",
            "post_format": "json"
        }
        cf = self.colloctConf
        url = cf['campaign_data']['url']
        for key in parm:
            url += key+"="+parm[key]+"&"
        print(url)
        data = self._post(url, json.dumps(cf['campaign_data']['data']))
        return data
