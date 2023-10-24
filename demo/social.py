import requests
from web3 import Web3
from eth_account import Account
import time
import unittest
import random

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
        self.address = "0x1fF3e7e46eA4e6052C0D4af2f683717dd81145dC"
        self.private_key = "1907d7eb94d72deb998bde7b3d0627558a38c24dda9609b0d82214a14913447a"

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

        if response.status_code == 200:
            user_info = response.json()
            return user_info
        else:
            raise ValueError(f"Failed to get user info: {response.status_code}")

    def get_feed_list(self, page_size=10, order_by=1):
        feed_list_url = BASE_URL + "/feed/api/feed/list"
        feed_list_headers = self.get_login_headers()  # Use the same headers as the login

        data = {
            "pageSize": page_size,
            "orderBy": order_by
        }

        response = requests.post(feed_list_url, headers=feed_list_headers, json=data)

        if response.status_code == 200:
            feed_list = response.json()
            return feed_list
        else:
            raise ValueError(f"Failed to get feed list: {response.status_code}")

    def post_feed(self, community_id, content, images):
        publish_url = BASE_URL + "/feed/api/feed/publish"
        publish_headers = self.get_login_headers()
        data = {
            "communityId": community_id,
            "contentType": 2,
            "text": content,
            "images": images,
            "subscriptionIds": []
        }
        response = requests.post(publish_url, headers=publish_headers, json=data)
        if response.status_code == 200:
            publish_result = response.json()
            return publish_result
        else:
            raise ValueError(f"Failed to post feed: {response.status_code}")

class TestApiUtils(unittest.TestCase):
    def setUp(self):
        self.api_utils = ApiUtils(BASE_URL)
        self.access_token = self.api_utils.get_access_token()

    def test_get_user_info(self):
        user_info = self.api_utils.get_user_info()
        print("User Info Response:", user_info)
        self.assertTrue("data" in user_info)

    def test_get_feed_list(self):
        feed_list = self.api_utils.get_feed_list()
        print("Feed List Response:", feed_list)
        self.assertTrue("data" in feed_list)

    def test_post_feed_random(self):
        community_id = "1716707821359337472"
        for i in range(2):
            text_content = f"M{i + 1}"
            image_url = "https://xplus-img.trytryc.com/img/2023-10-24/2f3f8bbc-b4ce-4531-bc48-4234cfa9de87.jpeg"
            images = [image_url]
            publish_result = self.api_utils.post_feed(community_id, text_content, images)
            print(f"Posted Feed {text_content}: {publish_result}")

if __name__ == "__main__":
    unittest.main()