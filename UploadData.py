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


def filelog(msg):
    # return True
    file_path = './log.log'
    with open(file_path, "a") as f:
        f.write(str(datetime.datetime.now()))
        f.write("\n")
        f.write(msg)
        f.write("\n\n")


class UploadData:
    def __init__(
        self,
        account='qqcollect',
        pwd='huoyi123456',
        secret_key='a77744a080161e3c5c71ee7421fedab0fc52b18dd5fcd90ea637e132fa07850c',
        platform_type='GatherOppoData',
    ):
        with open("./config-default.json", encoding='utf-8') as defcfg:
            cfg = json.load(defcfg)
        self.host = cfg['upload_host']
        self.secret_key = secret_key
        self.urls = {
            'token':
            self.host + '/api/'+platform_type+'/accessToken.html',
            'oppo_retain':
            self.host + '/api/GatherOppoData/addOppoCollectRetain.html',
            'oppo_payment':
            self.host + '/api/GatherOppoData/addOppoCollectPayment.html',
            'oppo_report':
            self.host + '/api/GatherOppoData/addOppoCollectAdvReport.html',
            'oppo_subRetain':
            self.host + '/api/GatherOppoData/subAddOppoCollectRetain.html',
            'vivo_basic':
            self.host + '/api/GatherVivoData/addVivoCollectBasic.html',
            'vivo_subBasic':
            self.host + '/api/GatherVivoData/subAddVivoCollectBasic.html',
            'vivo_app':
            self.host + '/api/GatherVivoData/addVivoCollectApp.html',
            'vivo_position':
            self.host + '/api/GatherVivoData/addVivoCollectPosition.html',
            'vivo_adv':
            self.host + '/api/GatherVivoData/addVivoCollectAdv.html',
            
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
