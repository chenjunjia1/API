import unittest
import allure
import os
import subprocess
from config import BASE_URL
from api.api_utils import ApiUtils
from tests.test_api import TestAPIs

from tests.test_api import TestAPIs

if __name__ == "__main__":

    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestAPIs)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)

    clear_cache_command = ["allure", "clean"]
    subprocess.run(clear_cache_command, shell=True)

    generate_command = ["allure", "generate", "allure-results", "--clean"]
    subprocess.run(generate_command, shell=True)

    open_command = ["allure", "open"]
    subprocess.run(open_command, shell=True)