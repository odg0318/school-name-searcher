#-*- coding: utf-8 -*-

import unittest

import school.util as util


class SchoolTestCase(unittest.TestCase):

    def test_check_full_name_school(self):
        r = util.regex_school_prefix(u'서초고등학교')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'고등학교')

        r = util.regex_school_prefix(u'서초중학교')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'중학교')

        r = util.regex_school_prefix(u'서초초등학교')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'초등학교')


    def test_check_shorten_normal_school(self):
        r = util.regex_school_prefix(u'서초고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'고')

        r = util.regex_school_prefix(u'서초중')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'중')

        r = util.regex_school_prefix(u'서초초')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'초')


    def test_check_girl_school(self):
        r = util.regex_school_prefix(u'숙명여자고등학교')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'고등학교')

        r = util.regex_school_prefix(u'숙명여자고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'여자고')

        r = util.regex_school_prefix(u'숙명여고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'여고')

        r = util.regex_school_prefix(u'숙명여자중학교')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'중학교')

        r = util.regex_school_prefix(u'숙명여자중')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'여자중')

        r = util.regex_school_prefix(u'숙명여중')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'여중')


    def test_check_shorten_special_school(self):
        r = util.regex_school_prefix(u'서울과고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'과고')

        r = util.regex_school_prefix(u'대원외고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'외고')

        r = util.regex_school_prefix(u'선화예고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'예고')

        r = util.regex_school_prefix(u'서울방송고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'방송고')

        r = util.regex_school_prefix(u'서울방통고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'방통고')

        r = util.regex_school_prefix(u'서울상고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'상고')

        r = util.regex_school_prefix(u'서울공고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'공고')


    def test_check_attached_school(self):
        r = util.regex_school_prefix(u'서울사대부고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'사대부고')

        r = util.regex_school_prefix(u'교대부설고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'부설고')

        r = util.regex_school_prefix(u'교대부고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'부고')

        r = util.regex_school_prefix(u'교대부고')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'부고')


    def test_check_branch_school(self):
        r = util.regex_school_prefix(u'서울분교')

        self.assertTrue(r is not None)
        self.assertEqual(r.group(0), u'분교')


if __name__ == '__main__':
    unittest.main()
