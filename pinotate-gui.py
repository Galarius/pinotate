#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Galarius'
__copyright__ = 'Copyright 2020, Galarius'

import platform
import sys

if platform.python_version().startswith("2."):
    print('Python3 is required')
    sys.exit(1)

import wx
import wx.html2 
import os
from markdown import markdown

from core import generate_md, valid_filename
from core import IBooksWorker

wxID_FRAME_LISTBOX_TITLES = wx.NewIdRef(count=1)
wxID_FRAME_BUTTON_EXPORT = wx.NewIdRef(count=1)

class Window(wx.Frame):
    def __init__(self, parent, title):
        super(Window, self).__init__(parent, title = title, size = (640,480))      
        self.worker = IBooksWorker()
        self.InitUI() 
        self.CreateStatusBar()
        self.Centre() 
        self.Show()
        self.SetAutoLayout(True)
        self.Layout()

    def InitUI(self): 
        titles = self.worker.titles()

        wxVbox = wx.BoxSizer(wx.VERTICAL)
        
        wxText = wx.TextCtrl(self, style=wx.TE_READONLY)
        wxText.SetValue("iBooks Library")
        wxVbox.Add(wxText, 0, wx.EXPAND) 
        
        self.wxListBox = wx.ListBox(choices=titles, id=wxID_FRAME_LISTBOX_TITLES, parent=self)
        self.wxListBox.Bind(wx.EVT_LISTBOX, self.OnRowSelected, id=wxID_FRAME_LISTBOX_TITLES)
        wxVbox.Add(self.wxListBox, 0, wx.EXPAND)
        
        self.browser = wx.html2.WebView.New(self) 
        wxVbox.Add(self.browser, 1, wx.EXPAND)
        
        self.SetSizer(wxVbox)

        menu = wx.Menu()
        exportMd = menu.Append(wx.ID_ANY,"Export...", "Export highlights.")
        aboutItem = menu.Append(wx.ID_ABOUT,"About...", "About Pinotate.")
        self.Bind(wx.EVT_MENU, self.OnExportMd, exportMd)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        bar = wx.MenuBar()
        bar.Append(menu, "File")
        self.SetMenuBar(bar)

    def OnRowSelected(self, event):
        self.content = ""
        self.title = self.wxListBox.GetStringSelection()
        self.SetStatusText("{}".format(self.title))
        asset_id = self.worker.asset_id(self.title)
        highlights = self.worker.highlights(asset_id)
        if highlights:
            self.content = generate_md(self.title, highlights)
        self.browser.SetPage(markdown(self.content), "")

    def OnExportMd(self, event):
        if len(self.content) == 0:
            return
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), valid_filename(self.title), "Markdown files (*.md)|*.md|", wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            filepath = dialog.GetPath()
            with open(filepath, 'w') as f:
                f.write(self.content)
        dialog.Destroy()

    def OnAbout(self, e):
        aboutDlg = wx.MessageDialog(self, "Export iBooks highlights","About Pinotate", wx.OK)
        aboutDlg.ShowModal()

app = wx.App()
wnd = Window(None, "Pinotate")
app.MainLoop()