'''
@Description: 
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
@LastEditors: Demoon
@LastEditTime: 2020-06-12 10:24:36
'''
import requests
import json
import time
import datetime


class UploadData:
    def __init__(
        self,
        account='houduan',
        pwd='hd666666',
        secret_key='cd283176e1e2c2a69a00e76a52742d42a4ae0b3780eec48fae289977008e9a3b',
    ):
        with open("./config-default.json", encoding='utf-8') as defcfg:
            cfg = json.load(defcfg)
        self.host = cfg['upload_host']
        self.secret_key = secret_key
        self.urls = {
            'token':
            self.host + '/api/WeixinData/accessToken.html',
            'addQqSsoCampaign':
            self.host + '/api/WeixinData/addQqSsoCampaign.html',
        }
        self.token = self.getToken(account, pwd)

    def getToken(self, acc, pwd):
        data = {
            'account': acc,
            'password': pwd,
            'secret_key': self.secret_key,
            'timestamp': time.time()
        }
        res = self.post(self.urls['token'], data)
        return res['Result']['token']

    #   post 方法
    def post(self, url, data):
        res = {}
        try:
            r = requests.post(url=url, data=data)
            res = r.json()
            print(res)
        except BaseException as e:
            print(str(e))
        return res

    def up(self, data_type, post_data):
        #   转换为字符串
        post_data = json.JSONEncoder().encode(post_data)
        #   构建数据
        data = {'token': self.token, 'data': post_data}
        #   发送
        self.subUp(self.urls[data_type], data)

    #   上传数据重传机制
    def subUp(self, url, data, time=3):
        if time > 0:
            res = self.post(url, data)
            if res.get('Status') != 200:
                time.sleep(2)
                self.subUp(url, data, time - 1)
