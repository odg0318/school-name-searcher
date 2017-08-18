#-*- coding: utf-8 -*-

import sys
import logging
import json

from school.parser import new_parser_from_csv
from school.util import pretty_dict


def main():
    logging.basicConfig(level=logging.INFO)

    parser = new_parser_from_csv('data/comments.csv')

    for result in parser:
        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        print json.dumps(sorted_result[:5], ensure_ascii=False)


if __name__ == '__main__':
    main()
