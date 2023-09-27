import os
import logging
from logging.handlers import TimedRotatingFileHandler
from config import BASE_URL  # 导入运行环境配置

# 创建一个名为 "logs" 的文件夹，如果它不存在的话
log_folder = "logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# 配置日志记录器
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

# 创建一个TimedRotatingFileHandler，按日期切换日志文件，但不使用backupCount参数
log_file = os.path.join(log_folder, "test_log.log")

# 在每次运行前清除日志文件内容
with open(log_file, "w") as log_file_clear:
    log_file_clear.write("")

file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=0, encoding='utf-8', delay=False, utc=False, atTime=None)

# 创建一个格式化器并设置日志记录格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将文件处理程序添加到日志记录器
logger.addHandler(file_handler)

# 记录BASE_URL的值到日志
logger.info(f"BASE_URL: {BASE_URL}")

# 现在，您可以使用logger.info，logger.error等方法记录其他日志
logger.info("This is an info message.")
logger.error("This is an error message.")
