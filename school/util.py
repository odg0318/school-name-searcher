#-*- coding: utf-8 -*-

import re

normal_school_pattern = re.compile(u'(초등|중|고등)학교$')
shorten_normal_school_pattern = re.compile(u'(초|중|고)$')
shorten_girl_school_pattern = re.compile(u'(여|여자)(초|중|고)$')
shorten_special_school_pattern = re.compile(u'(과|외|예|방송|방통|상|공)(초|중|고)$')
shorten_attached_school_pattern = re.compile(u'(사대부|부|부설|부속)(초|중|고)$')
branch_school_pattern = re.compile(u'분교(장)?$')


# An order of regular expression is very important.
# All shorten pattern should be matched before normal shorten one.
def regex_school_prefix(text):
    r = shorten_girl_school_pattern.search(text)
    if r is not None:
        return r

    r = shorten_special_school_pattern.search(text)
    if r is not None:
        return r

    r = shorten_attached_school_pattern.search(text)
    if r is not None:
        return r

    r = shorten_normal_school_pattern.search(text)
    if r is not None:
        return r

    r = normal_school_pattern.search(text)
    if r is not None:
        return r

    r = branch_school_pattern.search(text)
    if r is not None:
        return r

    return None


# Removes useless types from Twitter NLP parser.
def filter_pos(data):
    filtered_list = ['Adjective', 'Verb', 'Conjunction', 'Punctuation', 'Foreign', 'KoreanParticle']
    return [x for x in data if x[1] not in filtered_list]


def replace_shorten_to_full(text):
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

    return text


def is_enough_length(text):
    for prefix in [u'고등학교', u'중학교', u'초등학교']:
        if len(word.replace(prefix, u'')) > 2:
            return True

    return False


# Combine string to find school one by one from backward which is prefix of schools.
def combine_school_text(sample):
    pass
