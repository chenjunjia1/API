import schedule
import time
import subprocess

def run_code():
    subprocess.run(["python", "E:\python3.8\API\demo\moving.py"])  # 替换为你的代码文件的路径

scheduler = schedule.Scheduler()

scheduler.every(1).minutes.do(run_code)

while True:
    scheduler.run_pending()
    time.sleep(1)
