import csv
import tweepy
import time
import json
import datetime
from models import Object, User, UserType
from utils import Utils

class Dataset(Object):
    def __init__(self):
        self.humans = []
        self.bots = []
        self.unknown = []

    def load_csv(self, filename, numUsers=-1):
        with open(filename) as csvfile:
            api = Utils.get_api()
            reader = list(csv.reader(csvfile, delimiter='\t'))

            if numUsers > 0:
                limit = numUsers
            else:
                limit = sum(1 for row in csvfile)

            for row in reader[0:limit]:
                type = Utils.parse_type(row[1])
                user = None
                try:
                    user = Utils.get_user(api, id=row[0])
                except tweepy.RateLimitError:
                    print(datetime.datetime.now() + 'Rate limit hit! Waiting 15 minutes...')
                    time.sleep(900)
                    user = Utils.get_user(api, id=row[0])

                if type == UserType.HUMAN:
                    self.humans.append(user)
                elif type == UserType.BOT:
                    self.bots.append(user)
                else:
                    self.unknown.append(user)
            close(csvfile)

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(self.toJSON(pretty=False))
            f.close()

    def load(self, filename):
        with open(filename, 'r') as f:
            file_json = json.loads(f.read())
