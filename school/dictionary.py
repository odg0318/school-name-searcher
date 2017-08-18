#-*- coding: utf-8 -*-

import xlrd
import re

from konlpy.utils import pprint

import school.types as types
import school.util as util

ROW_START = 1

COL_LOCATION = 2 # 주소
COL_NAME = 4
COL_PROPERTY = 7 # (일반|자율|특성화|특수목적)고등학교
COL_TYPE = 9 # 단설, 병설, 부속
COL_GENDER = 25 # 남, 녀, 남녀공학

workbook = xlrd.open_workbook('data/schools.xlsx')
sheet = workbook.sheet_by_index(0)

locations = sheet.col_values(COL_LOCATION, ROW_START)
names = sheet.col_values(COL_NAME, ROW_START)
properties = sheet.col_values(COL_PROPERTY, ROW_START)
genders  = sheet.col_values(COL_GENDER, ROW_START)

data = zip(locations, names, properties, genders)

def find_school(token, matched_patterns=None, unmatched_patterns=None):
    if matched_patterns is None:
        matched_patterns = []

    if unmatched_patterns is None:
        unmatched_patterns = []

    level_pattern = util.get_pattern_from_level(token.level)
    kind_patterns = util.get_pattern_from_kinds(token.kinds)

    matched_patterns.append(re.compile(u'(%s)+.*%s$' % ('|'.join(token.texts), level_pattern)))
    if len(kind_patterns) > 0:
        matched_patterns.append(re.compile(u'(%s)+.*%s$' % ('|'.join(kind_patterns), level_pattern)))

    if types.NORMAL_SCHOOL_KIND in token.kinds:
        non_normal = [u'여자', u'과학', u'외국어', u'예술', u'방송통신', u'상업', u'공업', u'병설', u'부설']
        unmatched_patterns.append(re.compile(u'(%s)' % '|'.join(non_normal)))

    schools_with_score = []
    for d in data:
        location, name, prop, gender = d
        score = 0

        if token.is_girl_kind() and gender == u'녀':
            score += 1

        if not token.is_girl_kind() and gender != u'녀':
            score += 1

        if token.is_special_kind() and prop in [u'특수목적고등학교', u'특성화고등학교']:
            score += 1

        if token.has_location_in(name):
            score += 1

        if token.has_location_in(location):
            score += 1

        matched = [True for x in matched_patterns if x.search(name)]
        unmatched = [True for x in unmatched_patterns if x.search(name)]

        if len(matched) != len(matched_patterns) or len(unmatched) > 0:
            continue

        schools_with_score.append((name, score))

    if len(schools_with_score) == 0:
        return None

    return [x[0] for x in sorted(schools_with_score, key=lambda s: (s[1], -len(s[0])), reverse=True)][0]
