import sys
import tweepy
import json

from models import UserType, User, Tweet
from utils import Utils

# emoji unicode causes the program to crash, attempted this solution:
# https://stackoverflow.com/questions/47436649/trying-to-extract-tweets-with-tweepy-but-emojis-make-it-crash
# but it didnt' work, instead went with outright removing the emojis as shown here:
# https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-pytho



if __name__ == "__main__":
    username = "StadiaFan" # the twitter handle of an account to scrub the timeline of
    api = Utils.get_api()
    user = Utils.get_user(api, username)
    print(user)
