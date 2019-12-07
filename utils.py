import re
import json
import tweepy

class Utils:
    def remove_emoji(string):
        emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001F900-\U0001F9FF"  # Twitter icons?
                               "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)

    def load_credentials():
        with open("credentials.txt") as creds_file:
            return json.load(creds_file)

    def get_user(api, username, user_type=UserType.UNKNOWN):
        tweets_cursor = tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode="extended")
        return User(tweets_cursor, user_type)

    def get_api():
        creds = load_credentials()
        auth = tweepy.OAuthHandler(creds['key'], creds['key_secret'])
        auth.set_access_token(creds['token'], creds['token_secret'])
        api = tweepy.API(auth)
        if not api.verify_credentials():
            print('Bad credentials!')
            sys.exit(1)
        return api
