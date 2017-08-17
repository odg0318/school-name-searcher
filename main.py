#-*- coding: utf-8 -*-

import sys
import re

from konlpy.tag import Twitter
from konlpy.utils import pprint, csvread

import school.util as util
import school.dictionary as dictionary


def main():
    csvfile = open('data/comments.csv', 'rb')
    iterator = iter(csvread(csvfile))

    iterator.next()

    twitter = Twitter()

    for row in iterator:
        comment = row[0]

        data = twitter.pos(comment, norm=True)
        data = util.filter_pos(data)

        print('--text--')
        print(comment)
        print('--output--')

        for i, d in enumerate(data):
            r = util.regex_school_prefix(d[0])
            if r is None:
                continue

            sample = data[max(0, i-4):i+1]

            prefix = r.group(0)
            print(prefix)
            pprint(sample[max(-len(sample), -3):])


        sys.stdin.readline()


if __name__ == '__main__':
    main()
