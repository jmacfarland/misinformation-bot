import os
import csv
import tweepy
import time
import json
import datetime
import logging
from models import Object, User, UserType
from utils import Utils

class Dataset(Object):
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.FileHandler('%s.log'%str(datetime.datetime.now()).replace(' ','_')))
        self.humans = []
        self.bots = []
        self.unknown = []

    def load_csv(self, filename, numUsers, skip, verbose=False):
        with open(filename) as csvfile:
            api = Utils.get_api()
            reader = list(csv.reader(csvfile, delimiter='\t'))

            if numUsers is not None:
                limit = numUsers - 1
            else:
                limit = sum([1 for row in csvfile]) - 1

            directory = filename.split('.')[0]
            line = skip - 1

            for row in list(reader)[skip:skip+limit]:
                line = line + 1
                self.log.info('AccountID %s, line %s' % (row[0], line))
                print('AccountID %s, line %s' % (row[0], line))
                type = Utils.parse_type(row[1])
                try:
                    user = Utils.get_user(api, id=row[0])
                except tweepy.TweepError as e:
                    self.log.error(e)
                    continue

                self.save_user(directory, '_%s.dat'%str(line), user, verbose)

                if type == UserType.HUMAN:
                    self.humans.append(user)
                elif type == UserType.BOT:
                    self.bots.append(user)
                else:
                    self.unknown.append(user)
            csvfile.close()

    def remove_user_type(self, directory, num):
        for i in range(num):
            obj = None
            filename = directory+'/_%s.dat'%i
            try:
                with open(filename, 'r') as f:
                    data = f.read()
                    obj = json.loads(data.replace('"type": UserType.UNKNOWN,', ''))
            except:
                print('%s not found'%filename)

            open(filename, 'w').close() #clear the file
            with open(filename, 'w') as f:
                f.write(json.dumps(obj, default=lambda o: o.__dict__).strip("'<>()").replace('\'', '\"'))
                f.close()


    def categorize_files(self, directory, manifest):
        map = {}
        num_accounts = 0

        # Load mapping of AccountID -> (human | bot)
        with open(manifest, 'r') as m:
            reader = list(csv.reader(m, delimiter='\t'))
            lr = list(reader)
            count = len(lr)
            for row in lr:
                map[row[0]] = row[1]
            m.close()

        # load and categorize all files in dir
        #for i in range(count):
        i = 1
        obj = None
        filename = directory+'/_%s.dat'%i
        print(filename)
        with open(filename) as f:
            obj = json.loads(f.read())
            type = map[obj['id']]
            obj['type'] = type
            print('%s: %s'%(filename,type))

    def save_user(self, directory, filename, user, verbose=False):
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory+'/'+filename, 'w') as f:
            f.write(user.toJSON(pretty=False))
            if verbose:
                self.log.info('Wrote %s to %s/%s' % (user.screen_name, directory, filename))
            f.close()

    def save(self, filename, verbose=False):
        with open(filename, 'w') as f:
            f.write(self.toJSON(pretty=False))
            if verbose:
                self.log.info('Wrote %s human, %s bot, and %s unknown accounts' % (len(self.humans), len(self.bots), len(self.unknown)))
            f.close()

    def load(self, filename, verbose=False):
        with open(filename, 'r') as f:
            file_json = json.loads(f.read())
            self.humans = file_json['humans']
            self.bots = file_json['bots']
            self.unknown = file_json['unknown']
            if verbose:
                self.log.info('Loaded %s human, %s bot, and %s unknown accounts' % (len(self.humans), len(self.bots), len(self.unknown)))
            f.close()
