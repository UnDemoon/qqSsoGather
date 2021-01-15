'''
@Description: 
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
LastEditors: Please set LastEditors
LastEditTime: 2021-01-15 15:13:37
'''
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time


# login
def loginByBrowser(browser, url):
    cookies_type = 0
    cookies = None
    browser.set_page_load_timeout(60)
    try:
        browser.get(url)
    except BaseException:
        # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
        browser.execute_script("window.stop()")
    #   长等待 是否到达账号列表
    long_wait = WebDriverWait(browser, 120)
    login_flag = False
    try:
        login_flag = login_flag or long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tablebottom')))
    except BaseException:
        pass
    if login_flag:
        acc_items = browser.find_elements_by_xpath("//*[@id='tablebottom']//*[@class='ac-tableLine']")
        if len(acc_items) <= 0:
            next_url = 'https://ad.qq.com/worktable/'
            try:
                browser.get(next_url)
            except BaseException:
                # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
                browser.execute_script("window.stop()")
            long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.header-content .avatar')))
            cookies_type = 2
            cookies = browser.get_cookies()
        else:
            cookies_type = 1
            cookies = browser.get_cookies()
    return (cookies_type, cookies)


#   访问账号链接
def loginAccount(browser, url):
    try:
        browser.get(url)
    except BaseException:
        # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
        browser.execute_script("window.stop()")
    #   长等待 是否到达账号列表
    wait = WebDriverWait(browser, 30)
    login_flag = False
    try:
        login_flag = login_flag or wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.icon-avator')))
    except BaseException:
        pass
    if login_flag:
        cookies = browser.get_cookies()
        return cookies
    else:
        return False
