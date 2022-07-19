#! /bin/env python

"""
Please refer to the documentation provided in the README.md,
which can be found at https://github.com/Wasta-Geek/Lovecraft-scrapper/blob/master/README.md
"""

import argparse
import sys
from lovecraft_scrapper.lovecraft_page import LovecraftPage, LovecraftPageUnavailable


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


def lovecraft_scrapper_main() -> None:
    """
    Scrap a Lovecraft webpage and display some statistics about it
    """
    args = parse_arguments()
    lovecraft_page = LovecraftPage(args.url)
    try:
        lovecraft_page.open_webpage()
    except LovecraftPageUnavailable:
        print(f"Cannot retrieve webpage content, please verify the target URL '{args.url}'"
              " and your internet connection")
        sys.exit(1)


if __name__ == "__main__":
    lovecraft_scrapper_main()
