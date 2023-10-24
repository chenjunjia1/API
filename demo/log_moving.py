import logging
import time

# Configure the logger
logging.basicConfig(filename='movinglogs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestAPIs:

    def get_feed_list(self):
        # Simulate getting the feed list
        feed_list = [{"feedId": "1", "communityId": "A"}, {"feedId": "2", "communityId": "B"}, {"feedId": "3", "communityId": "C"}]
        # Log that you retrieved the feed list
        logging.info("Retrieved feed list: %s", feed_list)
        return feed_list

    def like_feed(self, feed_id, community_id):
        # Simulate liking a feed
        logging.info("Liked feed - feedId: %s, communityId: %s", feed_id, community_id)

    def comment_feed(self, feed_id, community_id, content):
        # Simulate commenting on a feed
        logging.info("Commented on feed - feedId: %s, communityId: %s, content: %s", feed_id, community_id, content)

    def test_interactions(self):
        feed_list = self.get_feed_list()
        for i, feed in enumerate(feed_list):
            if isinstance(feed, dict):
                feed_id = feed.get("feedId")
                community_id = feed.get("communityId")
                if i < 10:
                    self.like_feed(feed_id, community_id)
                if i % 2 == 0:
                    content = f"Random Comment {int(time.time())}"
                    self.comment_feed(feed_id, community_id, content)

if __name__ == "__main__":
    test = TestAPIs()
    test.test_interactions()
