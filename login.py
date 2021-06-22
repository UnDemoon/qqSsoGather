"""
@Description:
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
LastEditors: Please set LastEditors
LastEditTime: 2021-03-17 11:14:55
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
# import time


# login
def loginByBrowser(browser, url):
    cookies = None
    browser.set_page_load_timeout(60)
    try:
        browser.get(url)
    except Exception:
        # browser.refresh()   # 主动刷新
        browser.execute_script("window.stop()")    # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
    #   长等待 是否到达账号列表
    long_wait = WebDriverWait(browser, 120)
    login_flag = False
    try:
        login_flag = long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.icon-avator')))
    except Exception:
        pass
    if login_flag:
        if login_flag.get_attribute('id') == 'tablebottom':
            cookies = browser.get_cookies()
        else:
            cookies = browser.get_cookies()
    return cookies
