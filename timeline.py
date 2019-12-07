import sys
import tweepy
import json

from models import UserType, User, Tweet
from utils import remove_emoji

# emoji unicode causes the program to crash, attempted this solution:
# https://stackoverflow.com/questions/47436649/trying-to-extract-tweets-with-tweepy-but-emojis-make-it-crash
# but it didnt' work, instead went with outright removing the emojis as shown here:
# https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-pytho

def load_credentials():
    with open("credentials.txt") as creds_file:
        return json.load(creds_file)

def get_user(api, username, user_type=UserType.UNKNOWN):
    tweets_cursor = tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode="extended")
    return User(tweets_cursor, user_type)

if __name__ == "__main__":
    username = "StadiaFan" # the twitter handle of an account to scrub the timeline of

    creds = load_credentials()
    auth = tweepy.OAuthHandler(creds['key'], creds['key_secret'])
    auth.set_access_token(creds['token'], creds['token_secret'])
    api = tweepy.API(auth)

    if not api.verify_credentials():
        print('Bad credentials!')
        sys.exit(1)

    user = get_user(api, username)
    print(user)
