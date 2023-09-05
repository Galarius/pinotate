#!/usr/bin/env python3

__author__ = 'Galarius'
__copyright__ = 'Copyright 2020, Galarius'

import os
import sys
import argparse
import platform

from core import IBooksWorker

def main(args):
    
    worker = IBooksWorker()
    
    # print titles
    if args.list:
        titles = worker.titles()
        print('\n'.join(titles))
        sys.exit(0)
        
    # export
    if not (os.path.exists(args.out) and os.path.isdir(args.out)):
        os.makedirs(args.out)
    if args.title:
        worker.export(args)
    else:
        worker.export_all(args)

if __name__ == "__main__":
    if platform.python_version().startswith("2."):
        print('Python3 is required')
        sys.exit(1)

    ap = argparse.ArgumentParser(description="Export iBooks highlights", epilog="Run `pinotate.py` to export all highlights to the current directory")
    ap.add_argument('-o', '--out', default='./', help='output directory')
    ap.add_argument('-l', '--list', action="store_true", help='print books titles')
    ap.add_argument('--headings', default=False, action="store_true", help='add headings to markdown')
    ap.add_argument('-s', '--sort', default=False, action="store_true", help='sort by location instead of time')
    ap.add_argument('title', metavar='title', nargs='?', help="export only this book's highlights")
    args = ap.parse_args()
    main(args)
