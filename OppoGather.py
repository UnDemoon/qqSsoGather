'''
@Description: oppo数据采集类
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
@LastEditors: Demoon
@LastEditTime: 2020-07-01 11:36:41
'''
import requests
import datetime
import utils as mytools


class OppoGather:
    def __init__(self, cookie):
        #   获取今天日期 及 31日前日期
        todayuix = datetime.datetime.today()
        startuix = todayuix + datetime.timedelta(days=-8)   # 默认采8天  建议每7天采集一次
        self.colloctConf = [
            {
                # 0     小游戏数据
                'url': 'https://open.oppomobile.com/h5game/index/list.json',
                'data': {
                            "offset": 0,
                            "limit": 100
                        }
            },
            {
                # 1   留存详情
                'url': 'https://open.oppomobile.com/h5game/index/access-retain-list',
                'data': {
                            'instant_id': '',
                            'start_time': startuix.strftime('%Y-%m-%d'),
                            'end_time': todayuix.strftime('%Y-%m-%d'),
                            'offset': 0,
                            'limit': 100
                        }
            },
            {
                # 2   付费详情
                'url': 'https://open.oppomobile.com/h5game/data/payment',
                'data': {
                            'instant_id': '',
                            'start_date': startuix.strftime('%Y-%m-%d'),
                            'end_date': todayuix.strftime('%Y-%m-%d'),
                            'offset': 0,
                            'limit': 100
                        }
            },
            {
                # 3   媒体列表(app列表)
                'url': 'https://u.oppomobile.com/union/app/Q/list',
                'data': {
                    'page': 1,
                    'rows': 100,
                    'sortMode': 1
                }
            },
            {
                # 4   广告位列表
                'url': 'https://u.oppomobile.com/union/order/Q/list',
                'data': {
                    'page': 1,
                    'rows': 500,
                    'sortMode': 1
                }
            },
            {
                # 5   收益记录详细列表
                'url': 'https://u.oppomobile.com/union/static/report/query',
                'data': {
                            'startTime': startuix.strftime('%Y%m%d'),
                            'endTime': todayuix.strftime('%Y%m%d'),
                            'page': 1,
                            'rows': 10,
                            'order': 'desc',
                            'orderBy': 'time',
                            'timeGranularity': 'day',
                            'metrics': 'clickRatio,cpc,ecpm,income,view,click,userBuyIncome',
                            'dimensions': 'posId',
                        }
            },
            {
                # 6   收入
                'url': 'https://u.oppomobile.com/union/static/report/query',
                'data': {
                            'startTime': startuix.strftime('%Y%m%d'),
                            'endTime': todayuix.strftime('%Y%m%d'),
                            'page': 1,
                            'rows': 10,
                            'order': 'desc',
                            'orderBy': 'time',
                            'timeGranularity': 'day',
                            'metrics': 'income',
                            'dimensions': 'appId',
                        }
            },
            {
                # 7   留存详情第二部分
                'url': 'https://open.oppomobile.com/h5game/index/surveylist',
                'data': {
                            'instant_id': '',
                            'start_time': startuix.strftime('%Y-%m-%d'),
                            'end_time': todayuix.strftime('%Y-%m-%d'),
                            'offset': 0,
                            'limit': 100
                        }
            }
        ]
        #   配置requests session
        sess = requests.session()  # 新建session
        c = requests.cookies.RequestsCookieJar()        # 添加cookies到CookieJar
        for i in cookie:
            c.set(i["name"], i['value'])
            if i['name'] == 'oadstk':
                self.oadstk = i['value']
        sess.cookies.update(c)  # 更新session里cookies
        self.req = sess

    #   post 方法
    def post(self, url, para):
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

    #   采集运行头
    def appCollect(self):
        cf = self.colloctConf
        data = self.post(cf[0]['url'], cf[0]['data'])
        retain = []
        payment = []
        for item in data['data']['rows']:
            temp = self.subAppCollect(1, item['app_id'])   # 留存接口－１
            retain += temp
            temp = self.subAppCollect(7, item['app_id'])    # 留存接口－２
            retain += temp
            temp = self.subAppCollect(2, item['app_id'])
            payment += temp
        return (retain, payment)

    #   获取详细信息
    def subAppCollect(self, configIndex, app_id):
        cf = self.colloctConf
        data = cf[configIndex]['data']
        data['instant_id'] = app_id
        res = self.post(cf[configIndex]['url'], data)
        #   处理数据
        for item in res['data']['rows']:
            item['appid'] = app_id
        return res['data']['rows']

    #   统计信息采集
    def advCollect(self):
        self.req.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "o": "t",
            "sec-fetch-dest": "empty",
            "oadstk": self.oadstk,
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "origin": "https://u.oppomobile.com"
        }
        #   广告联盟
        cf = self.colloctConf
        details_list = self.getPages(cf[5]['url'], cf[5]['data'])
        income = self.getPages(cf[6]['url'], cf[6]['data'])
        return (details_list, income)

    #   多页数据处理
    def getPages(self, url, data):
        res = []
        data['page'] = 1
        onepage = self.post(url, data)
        while len(onepage['data']['items']) > 0:
            res += onepage['data']['items']
            data['page'] = data['page'] + 1
            onepage = self.post(url, data)
        return res
