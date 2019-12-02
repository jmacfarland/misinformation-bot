import timeline
import re

def get_keywords(username):
    # returns (usernames, hashtags)
    statuses = timeline.get_statuses(username)
    usernames = []
    hashtags = []

    for status in statuses:
        usernames.append(re.findall(r"@(\w+)", status))
        hashtags.append(re.findall(r"\#(\w+)", status))

    return usernames, hashtags

usernames, hashtags = get_keywords("StadiaFan")

print(usernames)
print("\n\n")
print(hashtags)
