#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ilya Shoshin (Galarius)'
__copyright__ = 'Copyright 2016, Ilya Shoshin (Galarius)'

import sqlite3
import shutil
import json
import sys
import os

class IBooksDispatcher(object):
    def __init__(self):
        self.home = os.path.expanduser("~")
        pref_folder = os.path.join(self.home,'Library/Containers/com.galarius.pinotate/')
        if not os.path.exists(pref_folder):
            os.mkdir(pref_folder)
        self.config_file = os.path.join(pref_folder,'config.json')
        self.ibooks_doc_root = 'Library/Containers/com.apple.iBooksX/Data/Documents/'
        self.library_folder = 'BKLibrary'
        self.annotation_folder = 'AEAnnotation'
        self.tmp_dir = './tmp'
        if not os.path.exists(self.config_file):
            self.__write_config()
        self.__read_config()

    def __write_config(self):
        with open(self.config_file, 'w') as data_file:
            dict = {"ibooks_doc_root":self.ibooks_doc_root,
            "library_folder":self.library_folder,
            "annotation_folder":self.annotation_folder,
            "tmp_dir":self.tmp_dir
            } 
            data = json.dumps(dict, ensure_ascii=False)
            data_file.write(data)            

    def __read_config(self):
        with open(self.config_file, 'r') as data_file:
            dict = json.load(data_file)
            self.ibooks_doc_root = dict["ibooks_doc_root"]
            self.library_folder  = dict["library_folder"]
            self.annotation_folder = dict["annotation_folder"]
            self.tmp_dir = dict["tmp_dir"]
       
    def __get_db(self, folder):
        db_dir = os.path.join(self.home, self.ibooks_doc_root, folder)
        db_name = None
        for file in os.listdir(db_dir):
            if file.endswith(".sqlite"):
                db_name = file
                break 
        
        if not db_name:
            return None

        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        # make a copy in tmp dir
        src = os.path.join(db_dir, db_name)
        dst = os.path.join(self.tmp_dir, db_name)
        shutil.copy(src, dst)
        return dst

    def find_library_db(self):
        return self.__get_db(self.library_folder)

    def find_annotation_db(self):
        return self.__get_db(self.annotation_folder)

    def get_book_titles(self, lib_db):
        titles = []
        conn = sqlite3.connect(lib_db)
        c = conn.cursor()
        for row in c.execute("SELECT ZTITLE FROM ZBKLIBRARYASSET WHERE ZTITLE <> '' AND ZTITLE <> 'none'"):
            titles.append(row[0])
        conn.close()
        return titles

    def get_book_asset_id(self, lib_db, book_title, enc=sys.stdin.encoding):
        conn = sqlite3.connect(lib_db)
        c = conn.cursor()
        t = ( (book_title.decode(enc) if enc else book_title), )
        c.execute("SELECT ZASSETID FROM ZBKLIBRARYASSET WHERE ZTITLE=?", t)
        result = c.fetchone()
        asset_id = result[0] if result else None
        conn.close()
        return asset_id

    def get_highlights(self, ann_db, asset_id):
        if not asset_id:
            return None

        conn = sqlite3.connect(ann_db)
        c = conn.cursor()
        t = (asset_id,)
        highlights = []
        for row in c.execute("SELECT ZANNOTATIONSELECTEDTEXT FROM ZAEANNOTATION WHERE ZANNOTATIONASSETID=? AND ZANNOTATIONSELECTEDTEXT <> ''", t):
            highlights.append(row[0])
        conn.close()
        return highlights

    def clear(self):
        shutil.rmtree(self.tmp_dir)