#!/usr/bin/env python

from utils import Utils
from dataset import Dataset
import argparse
import sys


def main(args):
    d = Dataset()
    if args.gather:
        if not args.outfile:
            print('Must specify --outfile')
            sys.exit(1)
        d.load_csv(args.infile, args.num_accounts, args.verbose)
        d.save(args.outfile, args.verbose)
    elif args.load:
        d.load(args.infile, args.verbose)
    else:
        print('--gather and --load are mutually exclusive options')
        sys.exit(1)

    print('Done!')
    sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gather', action='store_true', help='Gather relevant account data')
    parser.add_argument('-l', '--load', action='store_true', help='Load previously gathered data')
    parser.add_argument('-if', '--infile', help='CSV file to load accounts from')
    parser.add_argument('-of', '--outfile', help='File to store JSON output to')
    parser.add_argument('-n', '--num-accounts', type=int, help='How many accounts to process')
    parser.add_argument('-v', '--verbose', action='store_true', help='Display more information during process')

    args = parser.parse_args()
    main(args)
