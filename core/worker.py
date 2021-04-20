# -*- coding: utf-8 -*-

from .db import IBooksDispatcher
from .utils import valid_filename, generate_md

import os
import sys

__author__ = 'Galarius'
__copyright__ = 'Copyright 2020, Galarius'

class IBooksWorker (object):
    def __init__(self):
        self.dispatcher = IBooksDispatcher()
        self.lib_db = self.dispatcher.find_library_db()
        self.ann_db = self.dispatcher.find_annotation_db()
        self.__assert_db()

    def __del__(self):
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

    def asset_id(self, title):
        return self.dispatcher.get_book_asset_id(self.lib_db, title)

    def highlights(self, asset_id):
        return self.dispatcher.get_highlights(self.ann_db, asset_id)

    def export(self, args):
        self.__export(args.title, args.out, args.headings, args.sort)
    
    def export_all(self, args):
        for title in self.titles():    
            self.__export(title, args.out, args.headings, args.sort)

    def __export(self, title, out_dir, with_headings=True, normal_sorting=True):
        asset_id = self.asset_id(title)    
        if not asset_id:
            print("There is no book `{}` in library.".format(title))
            return
        highlights = self.highlights(asset_id)    
        if not len(highlights):
            print("No highlights were found in book `{}`.".format(title))
            return
        self.__save(title, highlights, out_dir, with_headings, normal_sorting)

    def __save(self, title, highlights, out_dir, with_headings=True, normal_sorting=True):
        filename = os.path.join(out_dir, "{}.md".format(valid_filename(title)))
        md = generate_md(title, highlights, with_headings, normal_sorting)
        with open(filename, 'w') as md_file:
            md_file.write(md)
        print('Created file "{}"'.format(filename))