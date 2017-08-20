#-*- coding: utf-8 -*-

import sys
import logging
import json
import argparse

from school.parser import new_parser_from_csv


def main():
    argparser = argparse.ArgumentParser(description='A program to parse schools from comments.')
    argparser.add_argument('--verbose', action='store_true', help='Show all logs.')
    argparser.add_argument('--no-skip', action='store_true', help='Show all logs.')
    args = argparser.parse_args()

    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=logging_level, format='%(asctime)s [%(levelname)s] %(message)s')

    parser = new_parser_from_csv('data/comments.csv')

    for result in parser:
        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        logging.info('--result--')
        logging.info(json.dumps(sorted_result[:5], ensure_ascii=False))

        if args.no_skip:
            sys.stdin.readline()


if __name__ == '__main__':
    main()
