import os
import logging
from logging.handlers import RotatingFileHandler
from config import BASE_URL  # 导入运行环境配置

# 创建一个名为 "logs" 的文件夹，如果它不存在的话
log_folder = "logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# 配置日志记录器
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

# 创建一个RotatingFileHandler，按文件大小进行切割并保留5个备份文件
log_file = os.path.join(log_folder, "test_log.log")
file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8')

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
