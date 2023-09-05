# -*- coding: utf-8 -*-

"""
Pinotate core module
"""

__author__ = 'Galarius'
__copyright__ = 'Copyright 2020, Galarius'

from .highlight import Highlight

import tempfile
import sqlite3
import shutil
import json
import sys
import os

class IBooksDispatcher(object):
    """
    Class to perform operations on iBooks database
    """
    def __init__(self):
        """
        Initialize application, create config file: 
        """
        self.home = os.path.expanduser("~")
        pref_folder = './'
        if not os.path.exists(pref_folder):
            os.mkdir(pref_folder)
        self.config_file = os.path.join(pref_folder, 'config.json')
        self.ibooks_doc_root = 'Library/Containers/com.apple.iBooksX/Data/Documents/'
        self.library_folder = 'BKLibrary'
        self.annotation_folder = 'AEAnnotation'
        self.tmp_dir = tempfile.TemporaryDirectory().name
        if not os.path.exists(self.config_file):
            self.__write_config()
        self.__read_config()

    def __write_config(self):
        """
        Save application configuration file
        """
        with open(self.config_file, 'w') as data_file:
            config = {"ibooks_doc_root":self.ibooks_doc_root,
            "library_folder":self.library_folder,
            "annotation_folder":self.annotation_folder,
            "tmp_dir":self.tmp_dir
            } 
            data = json.dumps(config, ensure_ascii=False)
            data_file.write(data)            

    def __read_config(self):
        """
        Read application configuration file
        """
        with open(self.config_file, 'r') as data_file:
            dict = json.load(data_file)
            self.ibooks_doc_root = dict["ibooks_doc_root"]
            self.library_folder  = dict["library_folder"]
            self.annotation_folder = dict["annotation_folder"]
            self.tmp_dir = dict["tmp_dir"]
       
    def __get_db(self, folder):
        """
        Copy iBooks database into temp folder
        @return database path
        """
        db_dir = os.path.join(self.home, self.ibooks_doc_root, folder)
        db_fullname = None

        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        for dfile in os.listdir(db_dir):
            src = os.path.join(db_dir, dfile)
            dst = os.path.join(self.tmp_dir, dfile)
            shutil.copy(src, dst)
            if dfile.endswith(".sqlite"):
                db_fullname = dst
        
        return db_fullname

    def find_library_db(self):
        """
        @return library db path
        """
        return self.__get_db(self.library_folder)

    def find_annotation_db(self):
        """
        @return annotation db path
        """
        return self.__get_db(self.annotation_folder)

    def get_book_titles(self, lib_db):
        """
        List all book titles from library db
        """
        titles = []
        conn = sqlite3.connect(lib_db)
        c = conn.cursor()
        for row in c.execute("SELECT ZTITLE FROM ZBKLIBRARYASSET WHERE ZTITLE <> '' AND ZTITLE <> 'none'"):
            titles.append(row[0])
        conn.close()
        return titles

    def get_book_asset_id(self, lib_db, book_title, enc=sys.stdin.encoding):
        """
        Find asset id by book title
        @return assets id or null
        """
        conn = sqlite3.connect(lib_db)
        cur = conn.cursor()
        cur.execute("SELECT ZASSETID FROM ZBKLIBRARYASSET WHERE ZTITLE=?", (book_title,))
        result = cur.fetchone()
        asset_id = result[0] if result else None
        conn.close()
        return asset_id

    def get_highlights(self, ann_db, asset_id):
        """
        Get highlights from annotation id by book's asset_id
        """
        if not asset_id:
            return None

        highlights = []
        try:
            with sqlite3.connect(ann_db) as conn:
                cur = conn.cursor()
                a_id = (asset_id,)
                for row, heading, created, location in cur.execute(
                    """SELECT ZANNOTATIONSELECTEDTEXT, 
                            ZFUTUREPROOFING5, 
                            ZANNOTATIONCREATIONDATE, 
                            ZANNOTATIONLOCATION 
                        FROM ZAEANNOTATION 
                        WHERE ZANNOTATIONASSETID=? 
                        AND ZANNOTATIONSELECTEDTEXT <> '' 
                        AND ZANNOTATIONDELETED=0
                    """, a_id):
                    chapter = 0
                    ref_in_chapter = 0
                    if location:
                        try:
                            chapter = int(location.split('[')[0].split('/')[2].replace(',', ''))
                            ref_in_chapter = int(location.split('!')[1].split('/')[2].replace(',', ''))
                        except:
                            pass
                    highligt = Highlight(row, heading, float(created), chapter, ref_in_chapter)
                    highlights.append(highligt)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

        return highlights

    def clear(self):
        """
        Remove temp directory
        """
        shutil.rmtree(self.tmp_dir)
