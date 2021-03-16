'''
Author: your name
Date: 2021-03-16 14:33:53
LastEditTime: 2021-03-16 14:48:35
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /qqSsoGather/main_user.py
'''
'''
@Description:
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
LastEditors: Please set LastEditors
LastEditTime: 2021-03-11 10:28:55
'''
#  基础模块
import sys
import json
import logging
#   selenium相关
from selenium import webdriver
#   qt5
from PyQt5 import QtWidgets
from PyQt5.Qt import QThread
from PyQt5.QtCore import (pyqtSignal, QObject)
#   引入ui文件
from home import Ui_MainWindow as Ui
#   引入登录模块
import login as lgm
#   引入requests类
from DataGather import DataGather
from UploadData import UploadData
#   工具集
# import utils as mytools


class MyApp(QtWidgets.QMainWindow, Ui):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.account_info = None
        self.browser = None
        self.threadPools = []
        Ui.__init__(self)
        self.setupUi(self)
        self._initdata()
        self.signinButton.clicked.connect(self.signin)

    #   数据初始化
    def _initdata(self):
        with open("./config-default.json", encoding='utf-8') as defcfg:
            cfg = json.load(defcfg)
            self.account_info = cfg['account_list']
        notelist = cfg['instructions'].split('；')
        for line in notelist:
            self.log(line, False)

    #   按钮触发
    def signin(self):
        self.lgGether()

    #   登录并采集
    def lgGether(self):
        self.log(' 开始')
        self.browser = browserInit()
        c_type, cookies = lgm.loginByBrowser(self.browser, "https://sso.e.qq.com/login/hub?sso_redirect_uri=https%3A%2F%2Fe.qq.com%2Fads%2F&service_tag=10")
        if c_type and cookies:
            # print(cookies)
            account = next((item for item in cookies if item.get('name', None) == 'ptui_loginuin'), None)
            print(account)
            return False
        else:
            self.log("登录异常，获取cookies失败，请稍后重新启动再次尝试！")

    #    输出信息
    def log(self, text, line=True):
        if line:
            self.logView.appendPlainText('-' * 20)
        self.logView.appendPlainText(text)
        return True


# 浏览器开启
def browserInit():
    # 实例化一个chrome浏览器
    chrome_options = webdriver.ChromeOptions()
    # options.add_argument(".\ChromePortable\App\Chrome\chrome.exe");
    chrome_options.binary_location = ".\\ChromePortable\\App\\Chrome\\chrome.exe"
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')   #   静默开启
    # chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--ignore-certificate-error")   # ssl 问题
    chrome_options.add_argument("--ignore-ssl-errors")
    # chrome_options.add_argument('--disable-gpu')
    # browser = webdriver.Chrome(options=chrome_options)
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()
    # 设置等待超时
    return browser

if __name__ == '__main__':
    # 定义为全局变量，方便其他模块使用
    global URL, RUN_EVN
    # 登录界面的url
    try:
        RUN_EVN = sys.argv[1]
    except Exception:
        RUN_EVN = "product"
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
