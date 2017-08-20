#-*- coding: utf-8 -*-

import sqlite3
import re
import os

import school.types as types
import school.util as util

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/schools.db')
conn = sqlite3.connect(db_path)


def find_school(token, matched_patterns=None, unmatched_patterns=None):
    if matched_patterns is None:
        matched_patterns = []

    if unmatched_patterns is None:
        unmatched_patterns = []

    level_pattern = util.get_pattern_from_level(token.level)
    kind_patterns = util.get_pattern_from_kinds(token.kinds)

    if len(kind_patterns) > 0:
        matched_patterns.append(re.compile(u'(%s)+.*%s$' % ('|'.join(kind_patterns), level_pattern)))

    if token.is_normal_kind():
        unmatched_patterns.append(util.non_normal_school_pattern)

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM schools WHERE name LIKE ? AND name LIKE ?', ('%'+token.text+'%', '%'+level_pattern))
    rows = cursor.fetchall()

    schools_with_score = []
    for row in rows:
        location, name, prop, gender = row
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
