#-*- coding: utf-8 -*-

import re
import logging
import time

from konlpy.tag import Twitter
from konlpy.utils import csvread

import school.types as types
import school.util as util
import school.dictionary as dictionary


class Parser(object):

    def __init__(self, **kwargs):
        diff = set(['csvpath', 'texts']) - set(kwargs.keys())
        if len(diff) == 2:
            raise Exception('csvpath or texts keyword parameter must be set.')

        if 'csvpath' in kwargs:
            csvfile = open(kwargs['csvpath'], 'rb')
            iterator = iter([x[0] for x in csvread(csvfile)])
            iterator.next()

        if 'texts' in kwargs:
            texts = kwargs['texts']
            if not isinstance(texts, list):
                raise Exception('texts keyword parameter must be list type.')
            iterator = iter(texts)

        self.iterator = iterator
        self.nlp = Twitter()
        self.result = {}

    def __iter__(self):
        return self

    def next(self):
        row = self.iterator.next()

        for school in self.parse(row):
            if school not in self.result:
                self.result[school] = 0

            self.result[school] += 1

        return self.result

    def parse(self, row):
        time_checker = util.TimeChecker()
        logging.debug('--start--')

        locations = util.get_locations_from_comments(row)

        logging.debug(time_checker.check_and_format('location'))

        logging.debug('--input--')
        logging.debug(util.pretty_str(row))

        pos_data = self.nlp.pos(row, norm=True)
        pos_data = util.filter_pos(pos_data)

        logging.debug(time_checker.check_and_format('nlp'))

        words = [util.remove_non_korean(x[0]) for x in pos_data]
        used_index = 0

        time_checker.check()
        logging.debug('--output--')
        for current_index, word in enumerate(words):
            level = util.get_school_level(word)
            if level is types.UNKNOWN_SCHOOL_LEVEL:
                continue

            # 학교로 끝나는 단어를 찾을 경우, 앞에 5글자까지 검색 할 대상으로 정한다.
            # ex) target_data = [u'하양', u'여', u'중']
            target_data = words[max(used_index, current_index-4):current_index+1]

            # 뒤에서부터 한 단어씩 추가해서 유효 값인지  사전에서 검색한다.
            # ex) raw_data = [u'중'] > [u'여중'] > [u'하양여중']
            for i in range(1, len(target_data)+1):
                raw_data = target_data[max(-len(target_data), -i):]

                token = Token(raw_data, locations)
                if token.is_skip():
                    continue

                school = dictionary.find_school(token)
                if school is None:
                    continue

                logging.debug(str(token))
                logging.debug(school)

                used_index = current_index

                yield school

                break

        logging.debug(time_checker.check_and_format('find_school'))
        logging.debug('--end--')


class Token(object):

    def __init__(self, raw_data, locations=None):
        self.raw_data = raw_data
        self.locations = locations
        if locations:
            self._location_pattern = re.compile('|'.join(locations))

        joined_text = ''.join(raw_data)
        self.level = util.get_school_level(joined_text)
        self.kinds = util.get_school_kinds(joined_text)
        self.text = util.remove_keywords(joined_text)


    def __str__(self):
        return 'level: %s, kinds: %s, locations: %s text: %s' % (self.level, self.kinds, util.pretty_list(self.locations), util.pretty_str(self.text))

    def has_location_in(self, text):
        if not self.locations:
            return False

        return self._location_pattern.search(text) is not None

    def is_skip(self):
        return len(self.text) < 2

    def is_girl_kind(self):
        return types.GIRL_SCHOOL_KIND in self.kinds

    def is_special_kind(self):
        return types.SPECIAL_SCHOOL_KIND in self.kinds

    def is_normal_kind(self):
        return types.NORMAL_SCHOOL_KIND is self.kinds


def new_parser_from_csv(csvpath):
    return Parser(csvpath=csvpath)


def new_parser_from_texts(texts):
    return Parser(texts=texts)
