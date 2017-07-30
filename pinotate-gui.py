#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ilya Shoshin (Galarius)'
__copyright__ = 'Copyright 2016, Ilya Shoshin (Galarius)'

from pinotate import *
import sys
import wx
import os

wxID_FRAME_LISTBOX_TITLES = wx.NewId()
wxID_FRAME_BUTTON_EXPORT = wx.NewId()


dispatcher = IBooksDispatcher()
lib_db = dispatcher.find_library_db()
ann_db = dispatcher.find_annotation_db()

if not lib_db:
    print "failed to find iBooks library database"
    sys.exit(2)

if not ann_db:
    print "failed to find iBooks annotation database"
    sys.exit(3)

titles = dispatcher.get_book_titles(lib_db)

class Window(wx.Frame):
    def __init__(self, parent, title):
        super(Window, self).__init__(parent, title = title, size = (640,480))      
        self.InitUI() 
        self.CreateStatusBar()
        self.Centre() 
        self.Show()
        self.SetAutoLayout(True)
        self.Layout()
        self.highlights = []

    def InitUI(self): 
        vbox = wx.BoxSizer(wx.VERTICAL)

        lblTitle = wx.TextCtrl(self, style=wx.TE_READONLY)
        lblTitle.SetValue("iBooks Library")
        vbox.Add(lblTitle, 0, wx.LEFT) 

        self.listBoxTitles = wx.ListBox(choices=titles, 
            id=wxID_FRAME_LISTBOX_TITLES,
            name='listBoxTitles', parent=self)
        self.listBoxTitles.Bind(wx.EVT_LISTBOX, self.OnListBoxListbox, id=wxID_FRAME_LISTBOX_TITLES)
        vbox.Add(self.listBoxTitles, 0, wx.EXPAND)

        self.textBoxHighlights = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.textBoxHighlights.SetBackgroundColour(wx.Colour(255, 255, 128))
        vbox.Add(self.textBoxHighlights, 1, wx.EXPAND)

        self.SetSizer(vbox)

        menu = wx.Menu()
        exportTxt = menu.Append(wx.ID_ANY,"Export as text...", "Export highlights as text.")
        exportCSV = menu.Append(wx.ID_ANY,"Export as csv...", "Export highlights as csv.")
        aboutItem = menu.Append(wx.ID_ABOUT,"About", "Push the button to get an information about Pinotate.")
        exitItem = menu.Append(wx.ID_EXIT,"Exit", "Push the button to leave Pinotate.")
        self.Bind(wx.EVT_MENU, self.OnExportTxt, exportTxt)
        self.Bind(wx.EVT_MENU, self.OnExportCSV, exportCSV)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        bar = wx.MenuBar()
        bar.Append(menu, "File")
        self.SetMenuBar(bar)

    def OnListBoxListbox(self, event):
        '''
        click list item and display the selected string in frame's title
        '''
        book_title = self.listBoxTitles.GetStringSelection()

        self.SetStatusText("Selected: {}".format(book_title.encode('utf-8')))

        # Library database
        asset_id = dispatcher.get_book_asset_id(lib_db, book_title, enc=None)
        
        # Annotation database
        self.highlights = dispatcher.get_highlights(ann_db, asset_id)
        highlights_text = '\n---------------\n'.join(self.highlights)
        self.textBoxHighlights.SetValue(highlights_text)

    def OnExportTxt(self, event):
        wildcard = "Text files (*.txt)|*.txt|" 
        "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            filepath = dialog.GetPath()
            with open(filepath, 'w') as f:
                f.write(self.textBoxHighlights.Value.encode('utf-8'))
        dialog.Destroy()

    def OnExportCSV(self, event):

        data = []
        separator = ';'.encode('utf-8')
        data.append("{0}{1}{2}".format("key", separator, "value"))
        for highlight in self.highlights:
            data.append("{0}{1}{2}".format(highlight.encode('utf-8'), separator, ""))
        highlights_text = '\n'.join(data)

        wildcard = "CSV files (*.csv)|*.csv|" 
        "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            filepath = dialog.GetPath()
            with open(filepath, 'w') as f:
                f.write(highlights_text)
        dialog.Destroy()

    def OnAbout(self, e):
        aboutDlg = wx.MessageDialog(self, "pinotate","About Pinotate", wx.OK)
        aboutDlg.ShowModal()
        
    def OnExit(self, e):
        self.control.SetValue("Close me, please! :(")
        dispatcher.clear()

app = wx.App()
wnd = Window(None, "Pinotate")
app.MainLoop()