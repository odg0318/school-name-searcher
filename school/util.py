#-*- coding: utf-8 -*-

import re
import time
import json

import school.types as types


def get_school_level(text):
    elementary_school_level_pattern = re.compile(u'(초등학교|초)$')
    middle_school_level_pattern = re.compile(u'(중학교|중)$')
    high_school_level_pattern = re.compile(u'(고등학교|고)$')
    other_school_level_pattern = re.compile(u'학교$')

    if elementary_school_level_pattern.search(text):
        return types.ELEMENTARY_SCHOOL_LEVEL

    if middle_school_level_pattern.search(text):
        return types.MIDDLE_SCHOOL_LEVEL

    if high_school_level_pattern.search(text):
        return types.HIGH_SCHOOL_LEVEL

    if other_school_level_pattern.search(text):
        return types.OTHER_SCHOOL_LEVEL

    return types.UNKNOWN_SCHOOL_LEVEL


def get_school_kinds(text):
    normal_school_pattern = re.compile(u'((초|중|고)|(초등|중|고등)학교)$')
    girl_school_pattern = re.compile(u'((여|여자)[가-힇]*(중|고)|여자[가-힇]*(중|고등)학교)$')
    open_school_pattern = re.compile(u'((방송|방통|방송통신)(여|여자)?(중|고)|방송통신(여|여자)?(중|고등)학교)$')
    special_school_pattern = re.compile(u'((과|과학|외|외국어|예|예술|방송|방통|방송통신|상|상업|공|공업)(여|여자)?(중|고)|(과학|외국어|예술|방송통신|상업|공업)(여자)?(중|고등)학교)$')
    attached_school_pattern = re.compile(u'((교대부|사대부|부|부설|부속)(여|여자)?(초|중|고)|(교육대학|사범대학)(부|부속|부설)(여자)?(초등|중|고등)학교)$')
    branch_school_pattern = re.compile(u'분교(장)?$')
    other_school_pattern = re.compile(u'학교$')

    special_science_school_pattern = re.compile(u'((과|과학)(여|여자)?(중|고)|과학(여|여자)?(중|고등)학교)$')
    special_foreign_school_pattern = re.compile(u'((외|외국어)(여|여자)?(중|고)|외국어(여|여자)?(중|고등)학교)$')
    special_art_school_pattern = re.compile(u'((예|예술)(여|여자)?(중|고)|예술(여|여자)?(중|고등)학교)$')
    special_commercial_school_pattern = re.compile(u'((상|상업)(여|여자)?(중|고)|상업(여|여자)?(중|고등)학교)$')
    special_technical_school_pattern = re.compile(u'((공|공업)(여|여자)?(중|고)|공업(여|여자)?(중|고등)학교)$')

    kinds = []
    if girl_school_pattern.search(text):
        kinds.append(types.GIRL_SCHOOL_KIND)

    if open_school_pattern.search(text):
        kinds.append(types.OPEN_SCHOOL_KIND)

    if special_school_pattern.search(text):
        kinds.append(types.SPECIAL_SCHOOL_KIND)

        if special_science_school_pattern.search(text):
            kinds.append(types.SPECIAL_SCIENCE_SCHOOL_KIND)

        if special_foreign_school_pattern.search(text):
            kinds.append(types.SPECIAL_FOREIGN_SCHOOL_KIND)

        if special_art_school_pattern.search(text):
            kinds.append(types.SPECIAL_ART_SCHOOL_KIND)

        if special_commercial_school_pattern.search(text):
            kinds.append(types.SPECIAL_COMMERCIAL_SCHOOL_KIND)

        if special_technical_school_pattern.search(text):
            kinds.append(types.SPECIAL_TECHNICAL_SCHOOL_KIND)

    if attached_school_pattern.search(text):
        kinds.append(types.ATTACHED_SCHOOL_KIND)

    if branch_school_pattern.search(text):
        kinds.append(types.BRANCH_SCHOOL_KIND)

    if len(kinds) > 0:
        return kinds

    if normal_school_pattern.search(text):
        kinds.append(types.NORMAL_SCHOOL_KIND)
        return kinds

    if other_school_pattern.search(text):
        kinds.append(types.OTHER_SCHOOL_LEVEL)
        return kinds

    kinds.append(types.UNKNOWN_SCHOOL_LEVEL)
    return kinds


# Removes useless types from Twitter NLP parser.
def filter_pos(data):
    filtered_list = ['Adjective', 'Conjunction', 'Punctuation', 'Foreign', 'KoreanParticle']
    return [x for x in data if x[1] not in filtered_list]


# Removes non-korean characters including garbage values.
def remove_non_korean(text):
    return re.sub(ur'[^가-힇\s]*', u'', text)


def remove_keywords(text):
    text = re.sub(u'여(중|고)$', u'여자\1', text)
    text = re.sub(u'과(중|고)$', u'과학\1', text)
    text = re.sub(u'외(중|고)$', u'외국어\1', text)
    text = re.sub(u'예(중|고)$', u'예술\1', text)
    text = re.sub(u'(방송|방통)(중|고)$', u'방송통신\1', text)
    text = re.sub(u'상(중|고)$', u'상업\1', text)
    text = re.sub(u'공(중|고)$', u'공업\1', text)
    text = re.sub(u'고$', u'고등학교', text)
    text = re.sub(u'중$', u'중학교', text)
    text = re.sub(u'초$', u'초등학교', text)

    keywords = [u'초등학교', u'중학교', u'고등학교', u'학교', u'분교장', u'분교', u'여자', u'과학', u'외국어', u'예술', u'방송통신', u'상업', u'공업', u'병설', u'부설']
    text = re.sub('|'.join(keywords), '', text)
    text = remove_non_korean(text)

    return text

def get_pattern_from_level(level):
    if level == types.ELEMENTARY_SCHOOL_LEVEL:
        return u'초등학교'

    if level == types.MIDDLE_SCHOOL_LEVEL:
        return u'중학교'

    if level == types.HIGH_SCHOOL_LEVEL:
        return u'고등학교'

    return u'학교'


def get_pattern_from_kinds(kinds):
    patterns = []

    if types.GIRL_SCHOOL_KIND in kinds:
        patterns += [u'여자']

    if types.OPEN_SCHOOL_KIND in kinds:
        patterns += [u'방송통신']

    if types.SPECIAL_SCHOOL_KIND in kinds:
        if types.SPECIAL_SCIENCE_SCHOOL_KIND in kinds:
            patterns += [u'과학']

        if types.SPECIAL_FOREIGN_SCHOOL_KIND in kinds:
            patterns += [u'외국어']

        if types.SPECIAL_ART_SCHOOL_KIND in kinds:
            patterns += [u'예술']

        if types.SPECIAL_COMMERCIAL_SCHOOL_KIND in kinds:
            patterns += [u'상업']

        if types.SPECIAL_TECHNICAL_SCHOOL_KIND in kinds:
            patterns += [u'공업']

    if types.ATTACHED_SCHOOL_KIND in kinds:
        patterns += [u'사범대학', u'부속', u'부설']

    if types.BRANCH_SCHOOL_KIND in kinds:
        patterns += [u'분교']

    return patterns


def get_locations_from_text(text):
    locations = []

    locations += re.findall(u'경기|강원|충청북도|충청남도|전라북도|전라남도|경상북도|경상남도|제주', text)
    locations += re.findall(u'서울|부산|대구|인천|광주|대전|울산|세종', text)
    locations += re.findall(u'성남|수원|안양|안산|용인|광명|평택|과천|오산|시흥|군포|의왕|하남|이천|안성|김포|화성|광주|여주|부천', text)
    locations += re.findall(u'고양|의정부|동두천|구리|남양주|파주|양주|포천', text)
    locations += re.findall(u'춘천|원주|강릉|동해|태백|속초|삼척', text)

    if u'충북' in text:
        locations.append(u'충청북도')

    if u'충남' in text:
        locations.append(u'충청남도')

    if u'전북' in text:
        locations.append(u'전라북도')

    if u'전남' in text:
        locations.append(u'전라남도')

    if u'경북' in text:
        locations.append(u'경상북도')

    if u'경남' in text:
        locations.append(u'경상남도')

    return locations


def pretty_str(s):
    return s.encode('utf-8')


def pretty_list(l):
    return '[' + pretty_str(','.join(l)) + ']'


def pretty_result_print(result):
    sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    return '\n'.join(['%s\t%d' % (pretty_str(x[0]), x[1]) for x in sorted_result])


class TimeChecker(object):

    def __init__(self):
        self.now = time.time()

    def check(self):
        new_now = time.time()
        diff = new_now - self.now
        self.now = new_now
        return diff

    def check_and_format(self, name):
        diff = self.check()

        return '[time checker] %s uses %fs' % (name, diff)

