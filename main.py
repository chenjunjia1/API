import unittest
import allure
import os
import subprocess
from config import BASE_URL
from api.api_utils import ApiUtils
from tests.test_api import TestAPIs

# 导入你的测试类
from tests.test_api import TestAPIs

if __name__ == "__main__":
    # 运行测试
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestAPIs)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)

    # 清除Allure报告缓存
    clear_cache_command = ["allure", "clean"]
    subprocess.run(clear_cache_command, shell=True)

    # 生成Allure报告
    generate_command = ["allure", "generate", "allure-results", "--clean"]
    subprocess.run(generate_command, shell=True)

    # 打开Allure报告
    open_command = ["allure", "open"]
    subprocess.run(open_command, shell=True)