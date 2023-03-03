# -*- coding:utf-8 -*-
import os, sys, unittest
# 测试报告
from jd_HTMLTestRunner import HTMLTestRunner
# 钉钉
from dingtalkchatbot.chatbot import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RunFaster.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django
django.setup()

from RunFaster.running.models import Case


def env_switch(env):
    """
    :param env: 如果有多个环境，在此处进行切换
    :return:
    """
    if env == "pre":
        return "https://prerelease-xxx.xxx.com/"
    else:
        return "https://xxx.xxx.com/"


def login_tianpeng(page, env):
    """
    :param page: 登录
    :return: 
    """
    page.set_default_timeout(40000)

    # 进行登录操作
    pass


def send_request_error(error_info):
    """
    钉钉发送告警信息
    :param error_info:
    :return:
    """
    url = "https://oapi.dingtalk.com/robot/send?access_token="

    data = "### UI自动化\n\n" \
           "> #### 请求失败URL : %s \n\n" % str(error_info['url']) + \
           "> #### 请求失败STATUS : %s \n\n" % str(error_info['status']) + \
           "> #### 执行时间 : %s\n" % time.strftime("%Y-%m-%d %X")

    DingtalkChatbot(url).send_markdown(title="UI自动化", text=data)


def send_result_error(case_name, result):
    """
    :param case_name:
    :param result:
    :return:
    """
    url = "https://oapi.dingtalk.com/robot/send?access_token="

    data = ""

    if case_name == '全用例':
        data = "### UI自动化\n\n" \
               "> #### 执行总条数 : %s \n\n" % str(result['sum']) + \
               "> #### 执行失败条数 : %s \n\n" % str(result['failure_count']) + \
               "> #### 自动化后台 : %s\n" % str("http://auto.com/index/") + \
               "> #### 执行时间 : %s\n" % time.strftime("%Y-%m-%d %X")
    else:
        data = "### UI自动化\n\n" \
               "> #### 执行失败用例 : %s \n\n" % str(case_name) + \
               "> #### 执行失败条数 : %s \n\n" % str(result.failure_count + result.error_count) + \
               "> #### 自动化后台 : %s\n" % str("http://auto.com/index/") + \
               "> #### 执行时间 : %s\n" % time.strftime("%Y-%m-%d %X")

    DingtalkChatbot(url).send_markdown(title="天蓬UI自动化", text=data)
    # print("**********", result.failure_count, result.success_count, result.error_count, result.skipped_count)


def result_all():
    """
    全部用例执行结束后，发送结果
    :return:
    """
    Cases = Case.objects.all().values()
    run_fail_count = 0
    run_success_count = 0

    for case in Cases:
        run_fail_count += case['run_fail_count']
        run_success_count += case['run_success_count']

    result = {'failure_count': run_fail_count, 'sum': run_success_count + run_fail_count}

    if run_fail_count > 0:
        send_result_error('全用例', result)


def on_response(response):
    """
    监听Web页面请求
    :param response:
    :return:
    """
    # 请求结果
    status = response.status
    if status >= 400:
        # 请求url
        url = response.url

        # 开始告警

        send_request_error({"url": url, "status": status})

    # print(status, response.url)


from asgiref.sync import sync_to_async


def html_runner(filename):
    """
    :param filename: 执行用例 && 生成报告
    :return:
    """
    run_file = filename + '.py'
    suite = unittest.TestLoader().discover(".", run_file)

    report_path = os.path.dirname(os.path.realpath(__file__))
    file = open(os.path.join(report_path, 'running/reports/' + filename + '.html'), "wb")
    result = HTMLTestRunner(stream=file, title="我的测试报告").run(suite)

    file.close()

    # 发送执行结果
    update_report(filename, result)


def update_report(filename, result):
    run_fail_count = result.failure_count + result.error_count
    run_success_count = result.success_count
    run_result = 'Success'
    if run_fail_count > 0:
        run_result = 'Fail'

    import datetime
    from datetime import timezone, timedelta
    run_time = str(datetime.datetime.now().replace(tzinfo=timezone(timedelta(hours=8))))[:19]

    sync_to_async(Case.objects.filter(run_file=filename).update(run_time=run_time, run_result=run_result,
                                                                run_fail_count=run_fail_count,
                                                                run_success_count=run_success_count))


if __name__ == '__main__':
    html_runner()
