'''
Author: Demoon
Date: 2020-09-28 15:41:31
LastEditTime: 2021-01-13 15:55:28
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /qqSsoGather/utils.py
'''
import random
import time
import datetime


#   随机间隔
def randomSleep():
    ret = random.uniform(0.3, 1.8)
    time.sleep(ret)


#   获取开始结束日期
def timeLag(daylag: int = 5, timetype: str = 'uix'):  # 日期间隔  类型 uix时间戳 day日期
    res = False
    endday = datetime.date.today()
    enduix = int(time.mktime(time.strptime(str(endday), '%Y-%m-%d')))
    startday = endday - datetime.timedelta(days=daylag)  # 默认最近几天
    startuix = int(time.mktime(time.strptime(str(startday), '%Y-%m-%d')))
    if timetype == 'uix':
        res = (startuix, enduix)
    else:
        res = (startday, endday)
    return res


#   生成最近n天日期
def dateList(daylen: int = 5):
    day = datetime.date.today()
    res = []
    for i in range(0, daylen):
        day = day - datetime.timedelta(days=1)
        res.append(day)
    return res

'''
description: qqsso平台api的g_tk计算
param {*}
return {*}
'''
def getACSRFToken(gdt_protect: str = "", skey: str = ""):
    e = 5381
    t = gdt_protect if gdt_protect else skey
    n = len(t)
    for a in range(0, n):
        e += (e << 5) + ord(t[a])
    return 2147483647 & e


# if __name__ == "__main__":
#     g_tk = getACSRFToken(skey="e69e8316c9185d36743a13cb5d8d1099b7eba5ab")
#     print(g_tk)
