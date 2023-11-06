import requests
from web3 import Web3
from eth_account import Account
import time
import random
import unittest

BASE_URL = "https://uat-xplus.trytryc.com"
HEADERS = {
    "Appver": "1.0.0",
    "Osver": "1.0.0",
    "Plat": "pc",
    "Content-Type": "application/json",
    "Authorization": ""
}

# 六个不同的评论内容
comments = [
    "Be cheerful and hopeful!",
    "It’s up to you how far you’ll go!",
    "You don’t have time to be timid!",
    "Light tomorrow with today!",
    "Energy and persistent conquer all things!",
    "Understand yourself in order to better understanding others!",
]


class ApiUtils:
    def __init__(self, base_url):
        self.base_url = base_url
        self.address = "0x460A6603418B26A9968a0687E2C19DeAd9c94dD6"
        self.private_key = "361e8eed934170511e8d0fd1ae3d71f1996fc529aceeba202d2ca67e484cc4c4"

    def get_login_headers(self):
        return HEADERS

    def get_access_token(self):
        login_url = BASE_URL + "/im/api/user/login/address"
        login_headers = self.get_login_headers()

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
        print("Login Response:", response.text)

        if response.status_code == 200:
            login_result = response.json()
            access_token = login_result.get("data", {}).get("bearerToken", "")
            HEADERS["Authorization"] = f"{access_token}"
            return access_token
        else:
            raise ValueError(f"登录请求失败: {response.status_code}")

    def query_dynamic_list(self):
        query_url = BASE_URL + "/im/api/user/info"
        query_headers = self.get_login_headers()

        response = requests.get(query_url, headers=query_headers)
        print("user info Response:", response.text)

        if response.status_code == 200:
            dynamic_list = response.json()
            return dynamic_list
        else:
            raise ValueError(f"查询动态列表请求失败: {response.status_code}")

    def get_community_ids(self):
        user_info = self.query_dynamic_list()
        community_list = user_info.get("data", {}).get("community", [])
        return [community["id"] for community in community_list]

    def get_latest_dynamic_list(self, count=6):
        list_url = BASE_URL + "/feed/api/feed/list"
        list_headers = self.get_login_headers()

        data = {
            "pageSize": count,
            "orderBy": 1
        }

        response = requests.post(list_url, headers=list_headers, json=data)
        dynamic_list = response.json()

        if response.status_code == 200:
            return dynamic_list["data"]["list"]
        else:
            raise ValueError(f"获取最近动态列表请求失败: {response.status_code}")

    def post_comment(self, feed_id, content, community_id):
        comment_url = BASE_URL + "/feed/api/feed/comment/post"
        comment_headers = self.get_login_headers()

        data = {
            "feedId": feed_id,
            "content": content,
            "communityId": community_id
        }

        response = requests.post(comment_url, headers=comment_headers, json=data)
        print("Post Comment Response:", response.text)

        if response.status_code != 200:
            raise ValueError(f"评论请求失败: {response.status_code}")

    def publish_text_dynamic(self, community_id, text):
        publish_url = BASE_URL + "/feed/api/feed/publish"
        publish_headers = self.get_login_headers()

        text_data = {
            "communityId": community_id,
            "contentType": 1,
            "text": text,
            "subscriptionIds": []
        }

        response = requests.post(publish_url, headers=publish_headers, json=text_data)
        print("Publish Text Dynamic Response:", response.text)

        if response.status_code != 200:
            raise ValueError(f"发布文本动态请求失败: {response.status_code}")

    def publish_image_dynamic(self, community_id, image_url, text):
        publish_url = BASE_URL + "/feed/api/feed/publish"
        publish_headers = self.get_login_headers()

        image_data = {
            "communityId": community_id,
            "contentType": 2,
            "text": text,
            "images": [image_url],
            "subscriptionIds": []
        }

        response = requests.post(publish_url, headers=publish_headers, json=image_data)
        print("Publish Image Dynamic Response:", response.text)

        if response.status_code != 200:
            raise ValueError(f"发布图片动态请求失败: {response.status_code}")

    def publish_video_dynamic(self, community_id, video_url, thumbnail_url, text):
        publish_url = BASE_URL + "/feed/api/feed/publish"
        publish_headers = self.get_login_headers()

        video_data = {
            "communityId": community_id,
            "contentType": 3,
            "text": text,
            "video": video_url,
            "videoThumbnail": thumbnail_url,
            "subscriptionIds": []
        }

        response = requests.post(publish_url, headers=publish_headers, json=video_data)
        print("Publish Video Dynamic Response:", response.text)

        if response.status_code != 200:
            raise ValueError(f"发布视频动态请求失败: {response.status_code}")

    def repost_dynamic(self, community_id, repost_feed_id, text):
        repost_url = BASE_URL + "/feed/api/feed/repost"
        repost_headers = self.get_login_headers()

        data = {
            "communityId": community_id,
            "repostFeedId": repost_feed_id,
            "text": text
        }

        response = requests.post(repost_url, headers=repost_headers, json=data)
        print("Repost Dynamic Response:", response.text)

        if response.status_code == 200:
            repost_result = response.json()
            repost_id = repost_result.get("data", {}).get("id", "")
            return repost_id
        else:
            raise ValueError(f"转发动态请求失败: {response.status_code}")


class TestDynamicActions(unittest.TestCase):
    def setUp(self):
        self.api = ApiUtils(BASE_URL)
        self.access_token = self.api.get_access_token()
        self.community_ids = self.api.get_community_ids()
        self.assertTrue(len(self.community_ids) >= 6)

    def test_publish_interact_with_dynamic(self):
        text_dynamic_text = "Text Dynamic"
        image_dynamic_text = "Image Dynamic"
        video_dynamic_text = "Video Dynamic"

        # 发布三种不同类型的动态
        for i in range(3):
            community_id = self.community_ids[i]

            if i % 3 == 0:
                self.api.publish_text_dynamic(community_id, text_dynamic_text)
            elif i % 3 == 1:
                image_url = "https://xplus-img.trytryc.com/img/2023-10-27/bfe8fe4c-8c91-4814-b8f0-95e80927a01c.jpeg"
                self.api.publish_image_dynamic(community_id, image_url, image_dynamic_text)
            else:
                video_url = "https://xplus-img.trytryc.com/2023-10-27/2d17f116-79d8-4b0c-8c92-9a3e5f2545fd.mp4"
                thumbnail_url = "https://xplus-img.trytryc.com/img/2023-10-27/17c0f2b1-c178-4f16-92cb-2ba0c9ba8393.png"
                self.api.publish_video_dynamic(community_id, video_url, thumbnail_url, video_dynamic_text)

        # 等待5秒
        time.sleep(5)

        # 获取最近的动态
        latest_dynamic_list = self.api.get_latest_dynamic_list(count=3)

        # 对每条动态进行一次转发和三次评论
        for dynamic in latest_dynamic_list:
            feed_id = dynamic["id"]

            for _ in range(3):
                content = random.choice(comments)  # 随机选择一个评论内容
                community_id = random.choice(self.community_ids)  # 使用不同社区
                self.api.post_comment(feed_id, content, community_id)

            text = random.choice(comments)  # 随机选择一个评论内容
            self.api.repost_dynamic(community_id, feed_id, text)

            # Add comments to the reposted dynamic
            reposted_dynamic = self.api.get_latest_dynamic_list(count=1)[0]
            reposted_feed_id = reposted_dynamic["id"]
            for _ in range(3):
                content = random.choice(comments)  # 随机选择一个评论内容
                community_id = random.choice(self.community_ids)  # 使用不同社区
                self.api.post_comment(reposted_feed_id, content, community_id)


if __name__ == "__main__":
    unittest.main()
