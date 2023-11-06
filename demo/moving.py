import requests
from web3 import Web3
from eth_account import Account
import time
import unittest
import random
import allure
import os
import subprocess
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
import logging


BASE_URL = "https://uat-xplus.trytryc.com"
HEADERS = {
    "Appver": "1.0.0",
    "Osver": "1.0.0",
    "Plat": "pc",
    "Content-Type": "application/json",
    "Authorization": ""
}

class ApiUtils:
    def __init__(self, base_url):
        self.base_url = base_url
        self.address = "0x460a6603418b26a9968a0687e2c19dead9c94dd6"
        self.private_key = "361e8eed934170511e8d0fd1ae3d71f1996fc529aceeba202d2ca67e484cc4c4"

    def get_login_headers(self):
        return HEADERS

    def get_access_token(self):
        login_url = BASE_URL + "/im/api/user/login/address"
        login_headers = self.get_login_headers()

        address, private_key = self.generate_random_wallet()

        timestamp = int(time.time())
        msg = f"Welcome to Xplus Meteor Portal.\nPlease sign this message to login Xplus Meteor Portal.\n\nTimestamp:{timestamp}"

        w3 = Web3()
        acct = Account().from_key(self.private_key)

        eth_message = f"\x19Ethereum Signed Message:\n{len(msg)}{msg}"
        message_hash = w3.keccak(text=eth_message)

        signature = w3.eth.account.signHash(message_hash, private_key=acct.key)

        data = {
            "address": self.address,
            "msg": msg,
            "signature": signature.signature.hex(),
        }

        response = requests.post(login_url, headers=login_headers, json=data)
        print("Login Response:", response.text)  # 打印登录响应

        if response.status_code == 200:
            login_result = response.json()
            access_token = login_result.get("data", {}).get("bearerToken", "")
            HEADERS["Authorization"] = f"{access_token}"  # Update the Authorization header
            return access_token
        else:
            raise ValueError(f"登录请求失败: {response.status_code}")

    def generate_random_wallet(self):
        w3 = Web3()
        acct = w3.eth.account.create()
        return acct.address, acct.key.hex()

    def get_user_info(self):
        user_info_url = BASE_URL + "/im/api/user/info"
        user_info_headers = self.get_login_headers()  # Use the login headers
        response = requests.get(user_info_url, headers=user_info_headers)
        print("User Info Response:", response.text)  # 打印用户信息响应

        if response.status_code == 200:
            user_info = response.json()
            return user_info
        else:
            raise ValueError(f"Failed to get user info: {response.status_code}")

    def get_red_envelope_feed_message_list(self, page_size=100, pre_page_last_id=""):
        red_envelope_feed_message_list_url = BASE_URL + "/im/api/red_envelope/feed_message_list"
        red_envelope_feed_message_list_headers = self.get_login_headers()

        data = {
            "pageSize": page_size,
            "prePageLastId": pre_page_last_id
        }

        response = requests.post(red_envelope_feed_message_list_url, headers=red_envelope_feed_message_list_headers,
                                 json=data)
        print("Red Envelope Feed Message List Response:", response.text)

        if response.status_code == 200:
            red_envelope_feed_message_list = response.json()
            return red_envelope_feed_message_list
        else:
            raise ValueError(f"Failed to get red envelope feed message list: {response.status_code}")

    def publish_feed(self, community_id, text):
        publish_url = BASE_URL + "/feed/api/feed/publish"
        publish_headers = self.get_login_headers()
        random_text = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(3))
        data = {
            "communityId": community_id,
            "contentType": 1,
            "text": text + random_text,  # Append the random text to the provided text
            "subscriptionIds": []
        }
        response = requests.post(publish_url, headers=publish_headers, json=data)
        print(f"Publish Feed Response:", response.text)

        if response.status_code == 200:
            publish_result = response.json()
            return publish_result
        else:
            raise ValueError(f"Failed to publish feed: {response.status_code}")

    def get_feed_list(self, page_size=10, order_by=1):
        feed_list_url = BASE_URL + "/feed/api/feed/list"
        feed_list_headers = self.get_login_headers()  # Use the same headers as the login

        data = {
            "pageSize": page_size,
            "orderBy": order_by
        }

        response = requests.post(feed_list_url, headers=feed_list_headers, json=data)
        print("Feed List Response:", response.text)

        if response.status_code == 200:
            feed_list = response.json()
            return feed_list
        else:
            raise ValueError(f"Failed to get feed list: {response.status_code}")

    def like_feed(self, feed_id, community_id):
        like_url = BASE_URL + "/feed/api/feed/like/update/like"
        like_headers = self.get_login_headers()
        data = {
            "feedId": feed_id,
            "communityId": community_id
        }
        response = requests.post(like_url, headers=like_headers, json=data)
        print(f"Like Feed {feed_id} Response:", response.text)

        if response.status_code == 200:
            like_result = response.json()
            return like_result
        else:
            raise ValueError(f"Failed to like feed: {response.status_code}")

    def post_comment(self, feed_id, community_id, content):
        comment_url = BASE_URL + "/feed/api/feed/comment/post"
        comment_headers = self.get_login_headers()
        data = {
            "feedId": feed_id,
            "content": content,
            "communityId": community_id
        }
        response = requests.post(comment_url, headers=comment_headers, json=data)
        print(f"Post Comment on Feed {feed_id} Response:", response.text)  # 打印评论响应

        if response.status_code == 200:
            comment_result = response.json()
            return comment_result
        else:
            raise ValueError(f"Failed to post comment: {response.status_code}")

    def repost_feed(self, community_id, repost_feed_id, text):
        repost_url = BASE_URL + "/feed/api/feed/repost"
        repost_headers = self.get_login_headers()
        data = {
            "communityId": community_id,
            "repostFeedId": repost_feed_id,
            "text": text
        }
        response = requests.post(repost_url, headers=repost_headers, json=data)
        print(f"Repost Feed {repost_feed_id} Response:", response.text)

        if response.status_code == 200:
            repost_result = response.json()
            return repost_result
        else:
            raise ValueError(f"Failed to repost feed: {response.status_code}")


@allure.feature("API Tests")
class TestApiUtils(unittest.TestCase):
    def setUp(self):
        self.api_utils = ApiUtils(BASE_URL)
        self.access_token = self.api_utils.get_access_token()

    @allure.story("User Info")
    def test_get_user_info(self):
        user_info = self.api_utils.get_user_info()
        self.assertTrue("data" in user_info)

    @allure.story("Red Envelope Feed Message List")
    def test_red_envelope_feed_message_list(self):
        red_envelope_feed_message_list = self.api_utils.get_red_envelope_feed_message_list()
        self.assertTrue("data" in red_envelope_feed_message_list)

    @allure.story("Publish Feed")
    def test_publish_feed(self):
        community_id = "1716707821359337472"
        text = "Test publish feed text "
        publish_result = self.api_utils.publish_feed(community_id, text)
        self.assertTrue("data" in publish_result)

    @allure.story("Feed List")
    def test_get_feed_list(self):
        feed_list = self.api_utils.get_feed_list()
        self.assertTrue("data" in feed_list)

        if "data" in feed_list and "list" in feed_list["data"]:
            first_six_feeds = feed_list["data"]["list"][:6]
            for feed in first_six_feeds:
                if "id" in feed:
                    feed_id = feed["id"]
                    community_id = feed["communityId"]
                    like_result = self.api_utils.like_feed(feed_id, community_id)

                    # Generate a random comment content
                    comment_content = str(random.randint(1, 10))
                    comment_result = self.api_utils.post_comment(feed_id, community_id, comment_content)

    @allure.story("Repost Feeds")
    def test_repost_feeds(self):
        feed_list = self.api_utils.get_feed_list()
        self.assertTrue("data" in feed_list)

        if "data" in feed_list and "list" in feed_list["data"]:
            first_three_feeds = feed_list["data"]["list"][:3]
            for feed in first_three_feeds:
                if "id" in feed:
                    community_id = feed["communityId"]
                    repost_feed_id = feed["id"]
                    text = "3"  # Replace with your desired text
                    repost_result = self.api_utils.repost_feed(community_id, repost_feed_id, text)

if __name__ == "__main__":
    unittest.main()