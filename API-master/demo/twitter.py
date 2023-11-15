import tweepy

# 替换以下信息为你的 Twitter API v2 Bearer Token
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAH6VqwEAAAAAy3kNofygcTDecuekFEQd%2FAI7Cxc%3DStnj6zBiLh6I2m61JLn82Dv7gUJ7k8GGy1n0N89Kq3wzwdH34Q'

# 验证
auth = tweepy.Client(auth_token=bearer_token, wait_on_rate_limit=True)
api = tweepy.API(auth)

try:
    # 替换以下信息为你要查找的用户的 Twitter 用户名（screen_name）
    target_user = 'target_user'

    # 查找用户信息
    user = api.get_user(screen_name=target_user)

    # 获取用户的前五条推文
    tweets = api.user_timeline(screen_name=target_user, count=5, tweet_mode="extended")

    print(f"User Name: {user.name}")
    print(f"User Screen Name: {user.screen_name}")
    print(f"Follower Count: {user.followers_count}")
    print(f"Description: {user.description}")
    print("\nLatest Tweets:")

    for tweet in tweets:
        print(f"\nTweet ID: {tweet.id}")
        print(f"Created at: {tweet.created_at}")
        print(f"Text: {tweet.full_text}")
except tweepy.TweepError as e:
    print(f"Error: {e}")
