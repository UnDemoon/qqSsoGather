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
        #   获取今天日期 及 31日前日期
        todayuix = datetime.datetime.today()
        startuix = todayuix + datetime.timedelta(days=-8)  # 默认采8天  建议每7天采集一次
        self.colloctConf = {
            'get_portal_data': {
                'url': 'https://sso.e.qq.com/login/get_portal_data',
                'data': {
                    "service_tag": "10"
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

    #   post 方法
    def _post(self, url, para):
        res = self.subPost(url, para)
        while (res.get('code') != 0) and (res.get('errno') != 0):
            mytools.randomSleep()
            res = self.subPost(url, para)
        return res

    #   post子方法
    def subPost(self, url, para):
        res = {}
        try:
            r = self.req.post(url, para)
            res = r.json()
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
        for item in data['data'][0]['account_list']:
            self.accounts.append(item['url'])
        return self.accounts
