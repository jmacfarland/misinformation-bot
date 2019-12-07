from enum import IntEnum
import json

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

    def __str__(self):
        return self.toJSON()

class Tweet(Object):
    def __init__(self, tweet):
        self.id = tweet['id']
        self.text = tweet['full_text']
        self.hashtag_count = len(tweet['entities']['hashtags'])
        self.mention_count = len(tweet['entities']['user_mentions'])
        self.url_count = len(tweet['entities']['urls'])
        self.time = tweet['created_at']
        self.retweet_count = tweet['retweet_count']
        self.favorite_count = tweet['favorite_count']

class UserType(IntEnum):
    UNKNOWN = 0
    HUMAN = 1
    BOT = 2

class User(Object):
    def __init__(self, tweets_cursor, type):
        # gather selected data points on user
        tweet_data = tweets_cursor.items(1)
        data = None
        for td in tweet_data:
            data = td._json['user']
        self.id = data['id']
        self.screen_name = data['screen_name']
        self.protected = data['protected']
        self.followers_count = data['followers_count']
        self.friends_count = data['friends_count']
        self.listed_count = data['listed_count']
        self.favourites_count = data['favourites_count']
        self.statuses_count = data['statuses_count']
        self.default_profile = data['default_profile']
        self.background_image_set = data['profile_background_image_url'] is not None
        self.verified = data['verified']
        self.geo_enabled = data['geo_enabled']
        self.type = type

        # attach selected data points on each tweet from user
        self.tweets = [Tweet(tweet._json) for tweet in tweets_cursor.items()]
