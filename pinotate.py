#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ilya Shoshin (Galarius)'
__copyright__ = 'Copyright 2016, Ilya Shoshin (Galarius)'

import sys

from pinotate import IBooksDispatcher

def print_usage():
    print("""
          `pinotate.py --list` to print all book titles
          `pinotate.py "book title"` to print all highlights from the selected book
          """)

def print_titles(dispatcher, lib_db):
    books = dispatcher.get_book_titles(lib_db)
    books_list_text = '\n---------------\n'.join(books)
    if len(books):
        print(books_list_text)
    else:
        print("There are no books in library.")

def print_highlights(book_title, dispatcher, lib_db, ann_db):
    # Library database
    print("looking book for `{}` in library database `{}`".format(book_title, lib_db))
    asset_id = dispatcher.get_book_asset_id(lib_db, book_title)
    if asset_id:
        # Annotation database
        print("looking highlights for `{}` in annotation database `{}`".format(asset_id, ann_db))
        highlights = dispatcher.get_highlights(ann_db, asset_id)
        if len(highlights):
            print("Found highlights: {}".format(len(highlights)))
        else:
            print("No highlights were found!")
        highlights_list_text = '\n---------------\n'.join(highlights)
        print(highlights_list_text)
    else:
        print("There is no book `{}` in library.".format(book_title))

def main(argv):

    if not len(argv):
        print_usage()
        sys.exit(1)

    dispatcher = IBooksDispatcher()
    lib_db = dispatcher.find_library_db()
    ann_db = dispatcher.find_annotation_db()

    if not lib_db:
        print("failed to find iBooks library database")
        sys.exit(2)

    if not ann_db:
        print("failed to find iBooks annotation database")
        sys.exit(3)

    if argv[0] == '--list':
        print_titles(dispatcher, lib_db)
    else:
        print_highlights(argv[0], dispatcher, lib_db, ann_db)

    dispatcher.clear()

if __name__ == "__main__":
    main(sys.argv[1:])