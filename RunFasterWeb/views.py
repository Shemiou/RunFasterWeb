# -*- coding:utf-8 -*-
import os, sys, json, django, subprocess
from django.shortcuts import render
from django.http import HttpResponse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RunFaster.settings')
django.setup()

BASEDIRPATH = os.path.dirname(os.path.realpath(__file__))

from RunFaster.running.models import *
from RunFaster.running.monitor import *
from RunFaster.common import *


def index(request):
    return render(request, 'index.html', get_case_all())


def get_case_all():
    cases = list(Case.objects.all().order_by('run_id').values())

    return {'cases': cases}


# 运行单条用例
def RunCaseOne(run_id, env):
    '''
    :param run_id: 用例执行ID
    :return:
    '''
    # 获取脚本位置
    run_file = BASEDIRPATH + '/RunFaster/running/' + Case.objects.filter(run_id=run_id)[0].run_file

    # 执行脚本
    run_command = 'python ' + run_file + '.py ' + env
    subprocess.call(run_command, shell=True)


def RunCaseEnv(env):
    cases = list(Case.objects.all().order_by('run_id').values())
    for case in cases:
        if env == 'pre':
            if case['run_main'] == 'TRUE':
                # 仅执行核心用例
                RunCaseOne(case['run_id'], 'pre')
        else:
            # 执行全用例
            RunCaseOne(case['run_id'], 'online')
    # 运行结束后发送结果
    result_all()


# 执行一条用例
def runCaseOne(request, run_id):
    '''
    :param run_id:
    :return:
    '''
    # 默认使用线上环境
    RunCaseOne(run_id=run_id, env='online')
    return HttpResponse('运行完成')


# 执行预发布核心用例
def runCaseKeyPre(request):
    '''
    :param request:
    :return:
    '''
    RunCaseEnv('pre')
    return HttpResponse('运行完成')


def runCaseKeyOnline(request):
    cases = list(Case.objects.filter(run_main='TRUE').order_by('run_id').values())
    for case in cases:
        RunCaseOne(case['run_id'], 'online')


# 执行全用例
def runCaseAll(request):
    '''
    :param request:
    :return:
    '''
    RunCaseEnv(env='online')
    return HttpResponse('运行完成')


# 执行监控
def runMonitor(request):
    """
    :param request:
    :return:
    """
    RunMonitor()
    return HttpResponse('运行完成')


# 关闭监控
def stopMonitor(request):
    """
    :param request:
    :return:
    """
    StopMonitor()
    return HttpResponse('运行完成')


# 查看测试报告
def reviewReport(request, run_id):
    '''
    :param run_file:
    :return:
    '''
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    CASE_REPORT_DIR = os.path.join(BASE_DIR, 'RunFaster/running/reports')

    report_path = os.path.join(CASE_REPORT_DIR, '%s.html' % str(Case.objects.filter(run_id=run_id)[0].run_file))

    return render(request, report_path)
