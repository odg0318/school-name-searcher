#-*- coding: utf-8 -*-

import unittest

import school.parser as parser
import school.util as util
import school.types as types
import school.dictionary as dictionary


class SchoolParserTestCase(unittest.TestCase):

    def test_invalid_initialize(self):
        self.assertRaises(Exception, parser.Parser)


    def test_initialize_from_texts(self):
        texts = [u'서초중학교', u'서초고등학교', u'그리고',  u'쓰레기값', u'서초중']
        p = parser.new_parser_from_texts(texts)

        result = None
        for r in p:
            result = r

        self.assertTrue(result is not None)
        self.assertEqual(2, result[u'서초중학교'])
        self.assertEqual(1, result[u'서초고등학교'])


    def test_token_initializer(self):
        token = parser.Token([u'하양여중'])

        self.assertEqual(types.MIDDLE_SCHOOL_LEVEL, token.level)
        self.assertTrue(types.GIRL_SCHOOL_KIND in token.kinds)
        self.assertEqual(2, len(token.text))
        self.assertEqual(u'하양', token.text)
        self.assertFalse(token.is_skip())


class SchoolLevelTestCase(unittest.TestCase):

    def test_elementary_school(self):
        for text in [u'서초초등학교', u'서초초']:
            level = util.get_school_level(text)
            self.assertEqual(level, types.ELEMENTARY_SCHOOL_LEVEL)

    def test_middle_school(self):
        for text in [u'서초중학교', u'서초중']:
            level = util.get_school_level(text)
            self.assertEqual(level, types.MIDDLE_SCHOOL_LEVEL)

    def test_high_school(self):
        for text in [u'서초고등학교', u'서초고']:
            level = util.get_school_level(text)
            self.assertEqual(level, types.HIGH_SCHOOL_LEVEL)

    def test_other_school(self):
        for text in [u'대안학교']:
            level = util.get_school_level(text)
            self.assertEqual(level, types.OTHER_SCHOOL_LEVEL)


class SchoolKindTestCase(unittest.TestCase):

    def test_normal_school(self):
        for text in [u'서초초등학교', u'서초초']:
            kinds = util.get_school_kinds(text)
            self.assertTrue(types.NORMAL_SCHOOL_KIND in kinds)

        for text in [u'서초중학교', u'서초중']:
            kinds = util.get_school_kinds(text)
            self.assertTrue(types.NORMAL_SCHOOL_KIND in kinds)

        for text in [u'서초고등학교', u'서초고']:
            kinds = util.get_school_kinds(text)
            self.assertTrue(types.NORMAL_SCHOOL_KIND in kinds)

    def test_girl_school(self):
        for text in [u'숙명여자중학교', u'숙명여자중', u'숙명여중']:
            kinds = util.get_school_kinds(text)
            self.assertTrue(types.GIRL_SCHOOL_KIND in kinds)

        for text in [u'숙명여자고등학교', u'숙명여자고', u'숙명여고']:
            kinds = util.get_school_kinds(text)
            self.assertTrue(types.GIRL_SCHOOL_KIND in kinds)

    def test_special_school(self):
        for text in [u'서울과고', u'서울과학고', u'서울과학고등학교']:
            kinds = util.get_school_kinds(text)
            self.assertTrue(types.SPECIAL_SCHOOL_KIND in kinds)

        for text in [u'서울외고', u'서울외국어고', u'서울외국어고등학교']:
            kinds = util.get_school_kinds(text)
            self.assertTrue(types.SPECIAL_SCHOOL_KIND in kinds)

        for text in [u'서울예고', u'서울예술고', u'서울예술고등학교']:
            kinds = util.get_school_kinds(text)
            self.assertTrue(types.SPECIAL_SCHOOL_KIND in kinds)

        for text in [u'서울방송고', u'서울방통고', u'서울방송통신고', u'서울방송통신고등학교']:
            kinds = util.get_school_kinds(text)
            self.assertTrue(types.SPECIAL_SCHOOL_KIND in kinds)

        for text in [u'서울상고', u'서울상업고', u'서울상업고등학교']:
            kinds = util.get_school_kinds(text)
            self.assertTrue(types.SPECIAL_SCHOOL_KIND in kinds)

        for text in [u'서울공고', u'서울공업고', u'서울공업고등학교']:
            kinds = util.get_school_kinds(text)
            self.assertTrue(types.SPECIAL_SCHOOL_KIND in kinds)

    def test_attached_school(self):
        for text in [u'서울사대부고', u'서울사대부설고', u'서울사대부속고', u'서울사범대학부속고등학교', u'서울사범대학부설고등학교']:
            kinds = util.get_school_kinds(text)
            self.assertTrue(types.ATTACHED_SCHOOL_KIND in kinds)

    def test_branch_school(self):
        for text in [u'서울분교', u'서울분교장']:
            kinds = util.get_school_kinds(text)
            self.assertTrue(types.BRANCH_SCHOOL_KIND in kinds)

    def test_mixed_school(self):
        kinds = util.get_school_kinds(u'서울대학교사범대학부설여자중학교')
        self.assertTrue(types.ATTACHED_SCHOOL_KIND in kinds)
        self.assertTrue(types.GIRL_SCHOOL_KIND in kinds)

        kinds = util.get_school_kinds(u'동일여자상업고등학교')
        self.assertTrue(types.SPECIAL_SCHOOL_KIND in kinds)
        self.assertTrue(types.SPECIAL_COMMERCIAL_SCHOOL_KIND in kinds)
        self.assertTrue(types.GIRL_SCHOOL_KIND in kinds)

        kinds = util.get_school_kinds(u'대구여자상업고등학교')
        self.assertTrue(types.SPECIAL_SCHOOL_KIND in kinds)
        self.assertTrue(types.SPECIAL_COMMERCIAL_SCHOOL_KIND in kinds)
        self.assertTrue(types.GIRL_SCHOOL_KIND in kinds)


class SchoolDictionaryTestCase(unittest.TestCase):

    def test_hayang_girl_school(self):
        token = parser.Token([u'하양여중'])

        school = dictionary.find_school(token)
        self.assertEqual(u'하양여자중학교', school)


if __name__ == '__main__':
    unittest.main(verbosity=2)
