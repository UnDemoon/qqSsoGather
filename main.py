'''
@Description:
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
@LastEditors: Demoon
@LastEditTime: 2020-07-01 11:13:46
'''
#  基础模块
import sys
import time
import json
#   selenium相关
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
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
from browsermobproxy import Server
#   工具集
import utils as mytools


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
        # self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint |   # 使能最小化按钮
        #                     QtCore.Qt.WindowCloseButtonHint |      # 使能关闭按钮
        #                     QtCore.Qt.WindowStaysOnTop

    #   数据初始化
    def _initdata(self):
        with open("./config-default.json", encoding='utf-8') as defcfg:
            cfg = json.load(defcfg)
            self.account_info = cfg['account_list']
            for k, item in enumerate(self.account_info):
                self.account_select.addItem(self.account_info[k]["name"], k)
        notelist = cfg['instructions'].split('；')
        for line in notelist:
            self.log(line, False)

    #   按钮触发
    def signin(self):
        account_index = self.account_select.currentData()
        account = self.account_info[account_index]
        self.log(account['name'] + ' - 开始')
        self.lgGether(account)

    #   登录并采集
    def lgGether(self, acc_info):
        self.browser, wait, proxy = browserInit()
        cookies = lgm.loginByBrowser(self.browser, "https://sso.e.qq.com/login/hub?sso_redirect_uri=https%3A%2F%2Fe.qq.com%2Fads%2F&service_tag=10", wait)
        if not cookies:
            self.log("Error in get cookies")
        #   线程运行采集
        gaThr = GatherThread(self.browser, cookies, proxy, acc_info['name'] + ' - !完成!')
        gaThr.sig.completed.connect(self.log)
        self.threadPools.append(gaThr)  # 加入线程池，局域变量线程未完成完后销毁导致异常
        gaThr.start()

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
    def __init__(self, browser, cookies, proxy, loginfo):
        super().__init__()
        self.cookies = cookies  # (ck1, ck2)
        self.info = loginfo
        self.browser = browser
        self.proxy = proxy
        self.sig = CompletionSignal()

    def run(self):
        cookies = self.cookies
        #   开发平台数据采集
        gather = DataGather(cookies)
        accs = gather.listAccount()
        g_kt = None
        acCookies = None
        UpData = UploadData()
        for ac in accs:
            if g_kt and acCookies:
                subGater = DataGather(acCookies)
                data = subGater.dataPlan(g_kt, ac.get('account_id'))
                UpData.up('addQqSsoCampaign', data)
            else:
                acCookies = lgm.loginAccount(self.browser, ac.get('url', None))
                result = self.proxy.har
                for entry in result['log']['entries']:
                    _url = entry['request']['url']
                    # 根据URL找到数据接口
                    if "ad.qq.com/ap/report/adgroup_list" in _url:
                        sp1 = _url.find('g_tk')
                        sp2 = _url.find('owner')
                        g_kt = _url[sp1+5:sp2-1]
                        break
                        break
        self.browser.quit()
        self.sig.completed.emit(self.info)


# # 浏览器开启
# def browserInit():
#     server = Server('.\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat')
#     server.start()
#     proxy = server.create_proxy()
#     # 实例化一个chrome浏览器
#     chrome_options = webdriver.ChromeOptions()
#     # options.add_argument(".\ChromePortable\App\Chrome\chrome.exe");
#     chrome_options.binary_location = ".\\ChromePortable\\App\\Chrome\\chrome.exe"
#     chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
#     # chrome_options = webdriver.ChromeOptions()
#     # chrome_options.add_argument('--headless')
#     # chrome_options.add_argument('--disable-gpu')
#     # browser = webdriver.Chrome(options=chrome_options)
#     browser = webdriver.Chrome(options=chrome_options)
#     # 设置等待超时
#     wait = WebDriverWait(browser, 100)
#     return (browser, wait, proxy)

# 浏览器开启
def browserInit():
    server = Server(".\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat") 
    server.start()
    proxy = server.create_proxy()
    proxy.new_har("douyin", options={'captureHeaders': True, 'captureContent': True})
    #   firfox 调用 browsermob-proxy 方法
    profile = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    browser = webdriver.Firefox(firefox_profile=profile)
    wait = WebDriverWait(browser, 100)
    return (browser, wait, proxy)


if __name__ == '__main__':
    # 定义为全局变量，方便其他模块使用
    global URL, RUN_EVN
    # 登录界面的url
    now = time.localtime()
    t = time.strftime("%Y%m%d%H%M", now)
    try:
        RUN_EVN = sys.argv[1]
    except Exception:
        pass
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
