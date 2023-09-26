import unittest
import allure
from api.api_utils import ApiUtils
from config import BASE_URL

@allure.epic("API Testing")
class TestAPIs(unittest.TestCase):

    def setUp(self):
        self.api_utils = ApiUtils(BASE_URL)

    @allure.feature("Publish Feed - Text")
    @allure.story("Publish Text Feed")
    def test_publish_feed_text(self):
        with allure.step("Publish Text Feed"):
            self.api_utils.publish_feed(content_type=1)

    @allure.feature("Publish Feed - Text with Image")
    @allure.story("Publish Text Feed with Image")
    def test_publish_feed_text_image(self):
        with allure.step("Publish Text Feed with Image"):
            self.api_utils.publish_feed(content_type=2)

    @allure.feature("Publish Feed - Text with Video")
    @allure.story("Publish Text Feed with Video")
    def test_publish_feed_text_video(self):
        with allure.step("Publish Text Feed with Video"):
            self.api_utils.publish_feed(content_type=3)

    @allure.feature("Get Community List")
    @allure.story("Get Community List Information")
    def test_get_community_list(self):
        with allure.step("Get Community List"):
            community_list_result = self.api_utils.get_community_list()
            allure.attach("Community List Response", community_list_result, allure.attachment_type.TEXT)

    @allure.feature("Get Account List")
    @allure.story("Get Account List Information")
    def test_get_account_list(self):
        with allure.step("Get Account List"):
            account_list_result = self.api_utils.get_account_list()
            allure.attach("Account List Response", account_list_result, allure.attachment_type.TEXT)

    @allure.feature("Get FOMO List")
    @allure.story("Get FOMO List Information")
    def test_get_fomo_list(self):
        with allure.step("Get FOMO List"):
            fomo_list_result = self.api_utils.get_fomo_list()
            allure.attach("FOMO List Response", fomo_list_result, allure.attachment_type.TEXT)
