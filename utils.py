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


def logFile(strings: str, file='debug-log.log'):
    """
    字符串写入文件
    """
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    with open(file, 'a+') as f:
        f.write('\n')
        f.write(now)
        f.write('\n')
        f.write(strings)
        f.write('\n')


# if __name__ == "__main__":
#     print(dateList())
