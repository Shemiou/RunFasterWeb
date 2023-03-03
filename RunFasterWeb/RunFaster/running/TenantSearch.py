# -*- coding:utf-8 -*-
import os, sys, time
import unittest

from playwright.sync_api import sync_playwright

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import RunFaster.common as common

env = sys.argv[1]


class TenantSearch(unittest.TestCase):
    '查询'

    @classmethod
    def setUpClass(cls):
        sp = sync_playwright().start()
        browser = sp.chromium.launch(channel="chrome", headless=True)

        context = browser.new_context(
            ignore_https_errors=True
        )

        # 创建page
        cls.page = context.new_page()

        # 开始监听page请求
        cls.page.on("response", common.on_response)

        # 如有需要登录的账号， 先登录
        common.login_tianpeng(cls.page, env=env)

    def test_001(self):
        '用例'
        pass




if __name__ == '__main__':
    common.html_runner('TenantSearch')
