import twitter
import json

def load_credentials():
    with open("credentials.txt") as creds_file:
        return json.load(creds_file)

def main():
    creds = load_credentials()
    api = twitter.Api(
        consumer_key=creds['key'],
        consumer_secret=creds['key_secret'],
        access_token_key=creds['token'],
        access_token_secret=creds['token_secret']
    )

    friends = api.GetFriends(creds['account_id'])
    print(friends)

main()
