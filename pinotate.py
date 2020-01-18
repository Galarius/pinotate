#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Galarius'
__copyright__ = 'Copyright 2020, Galarius'

import os
import sys
import argparse

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
        worker.export(args.title, args.out)
    else:
        worker.export_all(args.out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Export iBooks highlights", epilog="Run `pinotate.py` to export all highlights to the current directory")
    ap.add_argument('-o', '--out', default='./', help='output directory')
    ap.add_argument('-l', '--list', action="store_true", help='print books titles')
    ap.add_argument('only', metavar='title', nargs='?', help="export only this book's highlights")
    args = ap.parse_args()
    main(args)
