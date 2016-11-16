#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ilya Shoshin (Galarius)'
__copyright__ = 'Copyright 2016, Ilya Shoshin (Galarius)'

import sys
from pinotate import *

def print_usage():
    print """
          pinotate.py <book title>
          """

def main(argv):

    argv.append(argv)
    if not len(argv):
        print_usage()
        sys.exit(1)

    dispatcher = IBooksDispatcher()
    lib_db = dispatcher.find_library_db()
    ann_db = dispatcher.find_annotation_db()

    if not lib_db:
        print "failed to find iBooks library database"
        sys.exit(2)

    if not ann_db:
        print "failed to find iBooks annotation database"
        sys.exit(3)

    book_title = argv[0]

    # Библиотека
    print "looking book for `{}` in library database `{}`".format(book_title, lib_db)
    asset_id = dispatcher.get_book_asset_id(lib_db, book_title)
    # Аннотации
    print "looking highlights for `{}` in annotation database `{}`".format(asset_id, ann_db)
    highlights = dispatcher.get_highlights(ann_db, asset_id)

    if len(highlights):
        print highlights

    dispatcher.clear()

if __name__ == "__main__":
    main(sys.argv[1:])