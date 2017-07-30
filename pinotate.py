#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ilya Shoshin (Galarius)'
__copyright__ = 'Copyright 2016, Ilya Shoshin (Galarius)'

import sys

from pinotate import IBooksDispatcher

def print_usage():
    print """
          `pinotate.py --list` to print all book titles
          `pinotate.py "book title"` to print all highlights from the selected book
          """

def print_titles(dispatcher, lib_db):
    books = dispatcher.get_book_titles(lib_db)
    for book in books:
        print book

def print_highlights(book_title, dispatcher, lib_db, ann_db):
    # Library database
    print "looking book for `{}` in library database `{}`".format(book_title, lib_db)
    asset_id = dispatcher.get_book_asset_id(lib_db, book_title)
    # Annotation database
    print "looking highlights for `{}` in annotation database `{}`".format(asset_id, ann_db)
    highlights = dispatcher.get_highlights(ann_db, asset_id)
    if not len(highlights):
        print "No highlights were found!"
    else:
        print "Found highlights: {}".format(len(highlights))
    for highlight in highlights:
        print highlight

def main(argv):

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

    if argv[0] == '--list':
        print_titles(dispatcher, lib_db)
    else:
        print_highlights(argv[0], dispatcher, lib_db, ann_db)

    #dispatcher.clear()

if __name__ == "__main__":
    main(sys.argv[1:])