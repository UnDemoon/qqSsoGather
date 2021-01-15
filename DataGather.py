'''
@Description: oppo数据采集类
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
LastEditors: Please set LastEditors
LastEditTime: 2021-01-15 18:13:40
'''
import json
import requests
import utils as mytools
import logging


class DataGather:
    def __init__(self, cookie):
        self.colloctConf = {
            'get_portal_data': {
                'url': 'https://sso.e.qq.com/login/get_portal_data',
                'data': {
                    "service_tag": "10"
                }
            },
            'campaign_data': {
                'url': 'https://ad.qq.com/ap/report/campaign_list?',
                'data': {}
            },
            'spe_login': {
                'url': 'https://ad.qq.com/tap/v1/login/login_info',
                'data': {}
            },
            'spe_acc_list': {
                'url': 'https://ad.qq.com/tap/v1/account_daily_report/list',
                'data': {
                    "user_id": 0,
                    "start_date_millons": 1610553600000,  # 毫秒级时间戳
                    "end_date_millons": 1610639999000,
                    "need_yesterday_data": 0,
                    "dynamic_field_list": [
                        "balance", "view_count", "valid_click_count", "ctr",
                        "cpc", "cost"
                    ],
                    "filter_empty_data": 1,
                    "page": 1,
                    "page_size": 50
                }
            }
        }
        #   配置requests session
        sess = requests.session()  # 新建session
        c = requests.cookies.RequestsCookieJar()  # 添加cookies到CookieJar
        for i in cookie:
            c.set(i["name"], i['value'])
            if i['name'] == 'gdt_protect':
                self.g_tk = mytools.getACSRFToken(gdt_protect=i['value'])
            elif i['name'] == 'skey':
                self.g_tk = mytools.getACSRFToken(skey=i['value'])
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
        max_try = 3
        while (res.get('code') != 0) and (res.get('errno') != 0) and (max_try > 0):
            mytools.randomSleep()
            res = self._subPost(url, para)
            max_try = max_try - 1
        return res

    #   post子方法
    def _subPost(self, url, para):
        res = {}
        try:
            r = self.req.post(url, para)
            res = r.json()
        except BaseException as e:
            logging.WARNING(str(e))
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
            "referer":
            "https: //sso.e.qq.com/login/portal?service_tag=10&sso_redirect_uri=https%3A%2F%2Fe.qq.com%2Fads%2F",
            "sec-ch-ua":
            '"Google Chrome";v="87", "\"Not;A\\Brand";v="99", "Chromium";v="87"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4270.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        cf = self.colloctConf
        data = self._post(cf['get_portal_data']['url'],
                          json.dumps(cf['get_portal_data']['data']))
        #   获取账号列表失败
        try:
            account_list = data['data'][0]['account_list']
        except Exception:
            account_list = []
        return account_list

    '''
    description: 列出账号列表 - 特殊账号
    param {*} self
    return {dict}
    '''

    def listAccountSpe(self):
        acc_info = self.loginAccSpe()
        self.req.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/json; charset=UTF-8",
            "origin": "https://ad.qq.com",
            "referer": "https://ad.qq.com/worktable/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4270.0 Safari/537.36"
            }
        #   构建发送数据
        cf = self.colloctConf
        payload = cf['spe_acc_list']['data']
        payload['user_id'] = acc_info['user_id']
        suix, euix = mytools.timeLag()
        payload['start_date_millons'] = int(str(suix) + '000')
        payload['end_date_millons'] = int(str(euix) + '000')
        #   发送
        data = self._post(cf['spe_acc_list']['url'], json.dumps(payload))
        account_list = []
        #   结果处理
        try:
            for item in data['data']['list']:
                account_list.append({
                    "account_id": item['account_id'],
                    "url": "https://ad.qq.com/atlas/{0}/admanage/adgroup".format(str(item['account_id']))
                })
        except Exception:
            pass
        return account_list

    def loginAccSpe(self):
        cf = self.colloctConf
        data = self._post(cf['spe_login']['url'], "")
        return data['data']

    #   获取推广计划数据
    def dataPlan(self, own_id):
        res_list = []
        cf = self.colloctConf
        url = cf['campaign_data']['url']
        data = {
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
        self.req.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-length": "211",
            "content-type": "application/json",
            "origin": "https://ad.qq.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 OPR/70.0.3728.154",
            "x-requested-with": "XMLHttpRequest",
        }
        parm = {
            "g_tk": self.g_tk,
            "owner": own_id,
            "advertiser_id": own_id,
            # "trace_id": "294e3e58-14ab-ef91-dd0d-0d03b660cf13",
            # "g_trans_id": "d7629a32-00a0-8d08-3f1f-b9c4a648b19a",
            # "unicode": "1",
            # "post_format": "json"
        }
        for key in parm:
            url += str(key) + "=" + str(parm[key]) + "&"
        for dt in mytools.dateList():
            day = dt.strftime('%Y%m%d')
            day_str = str(dt)
            data['page'] = 1  # 重新计页
            data['rpt_filter']['time_range']['start_date'] = day
            data['rpt_filter']['time_range']['end_date'] = day
            data_json_str = json.dumps(data)
            res = self._post(url, data_json_str)
            res_list += self.dataDeal(res, day_str)
            while res['data']['conf']['page'] < res['data']['conf'][
                    'total_page']:
                mytools.randomSleep()
                data['page'] = data['page'] + 1  # 翻页
                data_json_str = json.dumps(data)
                res = self._post(url, data_json_str)
                res_list += self.dataDeal(res, day_str)
        return res_list

    @staticmethod
    def dataDeal(campaign_data: dict, day: str):
        """
        处理返回的数据
        """
        res = []
        try:
            for item in campaign_data['data']['list']:
                one = {
                    'day': day,
                    'cid': item['cid'],
                    'campaign_name': item['campaign_name'],
                    'cost': item['cost'],
                    'ctr': item['ctr'],
                    'ka_view_count': item['ka_view_count'],
                    'valid_click_count': item['valid_click_count'],
                }
                res.append(one)
        except Exception:
            pass
        return res
