#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Galarius'
__copyright__ = 'Copyright 2020, Galarius'

import os
import re
import sys
import argparse

from pinotate import IBooksDispatcher

# source: https://github.com/django/django/blob/master/django/utils/text.py
def valid_filename(s):
    return re.sub(r'(?u)[^-\w.]', '', str(s).strip().replace(' ', '_'))        

class IBooksWorker (object):
    def __init__(self):
        self.dispatcher = IBooksDispatcher()
        self.lib_db = self.dispatcher.find_library_db()
        self.ann_db = self.dispatcher.find_annotation_db()
        self.__assert_db()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.dispatcher.clear()

    def __assert_db(self):
        if not self.lib_db:
            print("Failed to find iBooks library database.")
            sys.exit(2)
        if not self.ann_db:
            print("Failed to find iBooks annotation database.")
            sys.exit(3)

    def titles(self):
        return self.dispatcher.get_book_titles(self.lib_db)

    def export(self, book, out_dir):
        if book:
            self.__export(book, out_dir)
            return

        for title in self.titles():    
            self.__export(title, out_dir)

    def __export(self, title, out_dir):
        asset_id = self.__asset_id(title)    
        if not asset_id:
            print("There is no book `{}` in library.".format(title))
            return
        highlights = self.__highlights(asset_id)    
        if not len(highlights):
            print("No highlights were found in book `{}`.".format(title))
            return
        self.__save(title, highlights, out_dir)
    
    def __asset_id(self, title):
        return self.dispatcher.get_book_asset_id(self.lib_db, title)

    def __highlights(self, asset_id):
        return self.dispatcher.get_highlights(self.ann_db, asset_id)

    def __save(self, title, highlights, out_dir):
        filename = os.path.join(out_dir, "{}.md".format(valid_filename(title)))
        with open(filename, 'w') as md_file:
            md_file.write("# {}\n\n".format(title))
            for highlight in highlights:
                md_file.write("> {}\n\n".format(highlight))
        print('Created file "{}"'.format(filename))

def main(args):
    # print titles
    if args.list:
        with IBooksWorker() as worker:
            titles = worker.titles()
            print('\n'.join(titles))
        return
    # create output dir if needed
    if not (os.path.exists(args.out) and os.path.isdir(args.out)):
        os.makedirs(args.out)
    # export
    with IBooksWorker() as worker:
        worker.export(args.title, args.out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Export iBooks highlights")
    ap.add_argument('-o', '--out', default='./', help='output directory')
    ap.add_argument('-l', '--list', action="store_true", help='print books titles')
    ap.add_argument('title', metavar='title', nargs='?', help='export highlights of a specific book only (optional)')
    args = ap.parse_args()
    main(args)
