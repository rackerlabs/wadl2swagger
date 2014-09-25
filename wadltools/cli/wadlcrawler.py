# -*- coding: utf-8 -*-

import os, errno
import argparse
import logging

import wadltools
from wadltools import WADLCrawler

def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

def main():
    parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--wadl-dir', type=str, default='wadls/', help='the directory to store the fetched WADLs')
    parser.add_argument('url', nargs='+', metavar='URL', help="URLs to fetch (will fetch individual HTML or crawl HTML links)")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    wadl_dir = args.wadl_dir
    mkdir_p(wadl_dir)
    crawler = WADLCrawler()
    for url in args.url:
        wadl_files = crawler.crawl(url)
        for wadl_file in wadl_files:
            target_file = os.path.join(wadl_dir, os.path.basename(wadl_file))
            logging.info("Downloading %s to %s", url, target_file)
            crawler.download(wadl_file, target_file)

if __name__ == '__main__':
    main()
