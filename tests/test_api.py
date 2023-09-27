import unittest
import allure
from api.api_utils import ApiUtils
from config import BASE_URL
from my_logging import logger  # 导入日志记录器


@allure.epic("API Testing")
class TestAPIs(unittest.TestCase):
    def setUp(self):
        self.api_utils = ApiUtils(BASE_URL)

        # 在setUp方法中添加注释，这些注释将应用于所有测试方法
        self.api_utils.test_feature = "Publish Feed"
        self.api_utils.test_story = "Text Feed"

    def tearDown(self):
        # 清除设置的注释，以防止其影响其他测试
        delattr(self.api_utils, 'test_feature')
        delattr(self.api_utils, 'test_story')

    def test_publish_feed_text(self):
        with allure.step("Publish Text Feed"):
            try:
                self.api_utils.publish_feed(content_type=1)
                for _ in range(3):
                    self.api_utils.publish_feed(content_type=1)
                logger.info("Publish Feed - Text: Success")
            except Exception as e:
                logger.error(f"Publish Feed - Text: Failed, Error: {str(e)}")

    def test_publish_feed_text_image(self):
        with allure.step("Publish Text Feed with Image"):
            try:
                self.api_utils.publish_feed(content_type=2)
                count = 0
                while count < 3:
                    self.api_utils.publish_feed(content_type=2)
                    count += 1
                logger.info("Publish Feed - Text with Image: Success")
            except Exception as e:
                logger.error(f"Publish Feed - Text with Image: Failed, Error: {str(e)}")

    def test_publish_feed_text_video(self):
        with allure.step("Publish Text Feed with Video"):
            try:
                self.api_utils.publish_feed(content_type=3)
                logger.info("Publish Feed - Text with Video: Success")
            except Exception as e:
                logger.error(f"Publish Feed - Text with Video: Failed, Error: {str(e)}")

    def test_get_community_list(self):
        with allure.step("Get Community List"):
            try:
                community_list_result = self.api_utils.get_community_list()
                allure.attach("Community List Response", community_list_result, allure.attachment_type.TEXT)
                logger.info("Get Community List: Success")
            except Exception as e:
                logger.error(f"Get Community List: Failed, Error: {str(e)}")

    def test_get_account_list(self):
        with allure.step("Get Account List"):
            try:
                account_list_result = self.api_utils.get_account_list()
                allure.attach("Account List Response", account_list_result, allure.attachment_type.TEXT)
                logger.info("Get Account List: Success")
            except Exception as e:
                logger.error(f"Get Account List: Failed, Error: {str(e)}")

    def test_get_fomo_list(self):
        with allure.step("Get FOMO List"):
            try:
                fomo_list_result = self.api_utils.get_fomo_list()
                allure.attach("FOMO List Response", fomo_list_result, allure.attachment_type.TEXT)
                logger.info("Get FOMO List: Success")
            except Exception as e:
                logger.error(f"Get FOMO List: Failed, Error: {str(e)}")

    def test_get_feed_list(self):
        with allure.step("Get feed List"):
            try:
                feed_list_result = self.api_utils.get_feed_list()
                allure.attach("feed List Response", feed_list_result, allure.attachment_type.TEXT)
                logger.info("Get feed List: Success")
            except Exception as e:
                logger.error(f"Get feed List: Failed, Error: {str(e)}")
