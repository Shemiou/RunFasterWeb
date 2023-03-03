# -*- coding:utf-8 -*-
import sys, os, time, logging, requests
import django

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AndroidTest.settings')
django.setup()
# --------------------------日志配置--------
logger = logging.getLogger("django")

from apscheduler.schedulers.background import BackgroundScheduler

aps = BackgroundScheduler(timezone='Asia/Shanghai')


def Monitor():
    requests.get('http://auto.com/index/runCaseKeyOnline/')


def RunAll():
    requests.get('http://auto.com/index/runCaseAll/')


def RunMonitor():
    # 第一个参数为目标函数，第二个为内置的一个名称，seconds为执行的间隔
    aps.add_job(Monitor, trigger='cron', hour='11-17,19-22', minute=0, second=0)
    aps.add_job(RunAll, trigger='cron', hour='10,18', minute=0, second=0)
    # 雷同与线程，启动线程任务
    aps.start()


def StopMonitor():
    ## 结束进程
    print(aps.get_jobs())
    if len(aps.get_jobs()) > 0:
        aps.shutdown(wait=False)
        aps.remove_all_jobs()
