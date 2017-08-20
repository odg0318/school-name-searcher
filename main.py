#-*- coding: utf-8 -*-

import sys
import logging
import argparse
import os

from school.parser import new_parser_from_csv
from school.util import pretty_result_print


def main():
    argparser = argparse.ArgumentParser(description='A program to parse schools from comments.')
    argparser.add_argument('--csvfile', required=True, help='CSV file to parse.')
    argparser.add_argument('--verbose', action='store_true', help='Show all logs.')
    argparser.add_argument('--no-skip', action='store_true', help='S')
    args = argparser.parse_args()

    if not os.path.exists(args.csvfile):
        print('%s file doesn\'t exist.' % args.csvfile)
        sys.exit(64)


    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=logging_level, format='%(asctime)s [%(levelname)s] %(message)s')

    parser = new_parser_from_csv(args.csvfile)

    for r in parser:
        if args.no_skip:
            parser.print_result()
            sys.stdin.readline()

    parser.print_result()



if __name__ == '__main__':
    main()
