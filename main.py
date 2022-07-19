#! /bin/env python

"""
Please refer to the documentation provided in the README.md,
which can be found at https://github.com/Wasta-Geek/Lovecraft-scrapper/blob/master/README.md
"""

import argparse


def parse_arguments() -> argparse.Namespace:
    """
    Parse arguments given by script input args

    :return: args object
    """
    parser = argparse.ArgumentParser(description='Scrap a HPL URL and print some data.')
    parser.add_argument('url', nargs="?", type=str,
                        default='https://www.hplovecraft.com/writings/texts/fiction/mm.aspx',
                        help='the target URL to scrap')
    args = parser.parse_args()
    return args


def lovecraft_scrapper() -> None:
    """

    :param args: arguments object
    """
    args = parse_arguments()
    print(args.url)


if __name__ == "__main__":
    lovecraft_scrapper()
