#-*- coding: utf-8 -*-

import xlrd

COL_NAME = 4
COL_TYPE = 9 # 단설, 병설, 부속
COL_MIXED_GENDER = 25 # 남, 녀, 남녀공학

workbook = xlrd.open_workbook('data/schools.xlsx')
sheet = workbook.sheet_by_index(0)

def find(text):
    global sheet

    schools = sheet.col_values(COL_NAME, 1)

    try:
        (x for x in schools if x.endswith(word)).next()
        pprint(word)
    except:
        pass
