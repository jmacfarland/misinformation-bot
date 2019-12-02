import sys
import tweepy
#import twitter
import re

# emoji unicode causes the program to crash, attempted this solution:
# https://stackoverflow.com/questions/47436649/trying-to-extract-tweets-with-tweepy-but-emojis-make-it-crash
# but it didnt' work, instead went with outright removing the emojis as shown here:
# https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
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

#print(remove_emoji("TEST \U0001F44D"))

def get_statuses(username):
    auth = tweepy.OAuthHandler("B64NvUxL6HsTc4mzHgAOf8RZW", "9oQhr3GV7KNcZ6vgmDcvh57YfRtc7UNE25QRNFiHaf6oc9s7jf")
    auth.set_access_token("1147175528492933122-BCBWkaxBANeQSqBWXBMUvKcaXBXgL2", "xhltiEyDaJ6DGKXhxKMKi81cVhAjdsG1P0m3cgIxLM9w4")
    api = tweepy.API(auth)

    # Our original method did not provide the full timeline, found a solution at this link:
    #  https://stackoverflow.com/questions/42225364/getting-whole-user-timeline-of-a-twitter-user
    all_statuses = tweepy.Cursor(api.user_timeline, screen_name='StadiaFan', tweet_mode="extended").items()
    return [remove_emoji(str(status.full_text)) for status in all_statuses]

username = "StadiaFan" # the twitter handle of an account to scrub the timeline of
print("THE TIMELINE OF: " + username + "\n________________")
all_statuses = get_statuses(username)
for status in all_statuses:
    print(status)
print("___________\nEND OF TIMELINE")
