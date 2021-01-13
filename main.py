'''
@Description:
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
LastEditors: Please set LastEditors
LastEditTime: 2021-01-13 16:00:33
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
        logging.debug("browserInit succee")
        cookies = lgm.loginByBrowser(self.browser, "https://sso.e.qq.com/login/hub?sso_redirect_uri=https%3A%2F%2Fe.qq.com%2Fads%2F&service_tag=10")
        if cookies:
            #   线程运行采集
            gaThr = GatherThread(self.browser, cookies, '!完成!')
            gaThr.sig.completed.connect(self.log)
            self.threadPools.append(gaThr)  # 加入线程池，局域变量线程未完成完后销毁导致异常
            gaThr.start()
        else:
            self.log("登录异常，获取cookies失败，请稍后重试！")

    #    输出信息
    def log(self, text, line=True):
        if line:
            self.logView.appendPlainText('-' * 20)
        self.logView.appendPlainText(text)
        return True


#   自定义的信号  完成信号
class CompletionSignal(QObject):
    completed = pyqtSignal(str)


# gather采集线程
class GatherThread(QThread):
    def __init__(self, browser, cookies, loginfo):
        super().__init__()
        self.cookies = cookies  # (ck1, ck2)
        self.info = loginfo
        self.browser = browser
        self.sig = CompletionSignal()

    def run(self):
        cookies = self.cookies
        #   开发平台数据采集
        gather = DataGather(cookies)
        accs = gather.listAccount()
        UpData = UploadData()
        for ac in accs:
            acCookies = lgm.loginAccount(self.browser, ac.get('url', None))
            if not acCookies:
                logging.error("Error in get account cookies params={}".format(str(ac)))
                continue
            subGater = DataGather(acCookies)
            data = subGater.dataPlan(ac.get('account_id'))
            UpData.up('addQqSsoCampaign', data)
        self.browser.quit()
        self.sig.completed.emit(self.info)


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


# 浏览器开启
def browserInit():
    # 实例化一个chrome浏览器
    chrome_options = webdriver.ChromeOptions()
    # options.add_argument(".\ChromePortable\App\Chrome\chrome.exe");
    chrome_options.binary_location = ".\\ChromePortable\\App\\Chrome\\chrome.exe"
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')   #   静默开启
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
    logInit()
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
