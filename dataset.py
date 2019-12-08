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

    def load_csv(self, filename, numUsers, verbose=False):
        with open(filename) as csvfile:
            api = Utils.get_api()
            reader = list(csv.reader(csvfile, delimiter='\t'))
            print(reader)

            if numUsers is not None:
                limit = numUsers
            else:
                limit = sum([1 for row in csvfile])

            count = 0
            for row in reader:
                print('AccountID %s' % row[0])
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
                count += 1
                if count >= limit:
                    break
            csvfile.close()

    def save(self, filename, verbose=False):
        with open(filename, 'w') as f:
            f.write(self.toJSON(pretty=False))
            if verbose:
                print('Wrote %s human, %s bot, and %s unknown accounts' % (len(self.humans), len(self.bots), len(self.unknown)))
            f.close()

    def load(self, filename, verbose=False):
        with open(filename, 'r') as f:
            file_json = json.loads(f.read())
            self.humans = file_json['humans']
            self.bots = file_json['bots']
            self.unknown = file_json['unknown']
            if verbose:
                print('Loaded %s human, %s bot, and %s unknown accounts' % (len(self.humans), len(self.bots), len(self.unknown)))
            f.close()
