import unittest
import subprocess

from tests.test_api import TestAPIs

if __name__ == "__main__":

    clear_cache_command = ["allure", "clean"]
    subprocess.run(clear_cache_command, shell=True)

    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestAPIs)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)

    generate_command = ["allure", "generate", "allure-results", "--clean"]
    subprocess.run(generate_command, shell=True)

    open_command = ["allure", "open"]
    process = subprocess.run(open_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    if process.returncode == 0:
        report_url = process.stdout.decode("utf-8")
        print(f"Allure report URL: {report_url}")
    else:
        print("Failed to open Allure report.")
