# -*- coding: utf-8 -*-


# =============================================================================
# 
# =============================================================================


__title__ = "Visibility Manager"
__Author__ = "Nhan Truong"

org = "Portcoast Consultant Corporation"
na = "Nhan Truong"
em = "nhan.tnt@portcoast.com.vn"
mo = "+84 379197306"


# =============================================================================
# 
# =============================================================================

import os

import clr

clr.AddReference('RevitAPI')

import Autodesk

from Autodesk.Revit.DB import *

clr.AddReference('IronPython.Wpf')

import wpf

import pyrevit

from pyrevit import script

xamlfile = script.get_bundle_file('UI.xaml')

from System import Uri, UriKind

from System.Windows import Application, Window, Media, Controls

# =============================================================================
# 
# =============================================================================

dir_name = os.path.dirname(__file__)

uiapp = __revit__
uidoc = uiapp.ActiveUIDocument
doc = uidoc.Document

def getCategoriesInActiveView():
    doc = __revit__.ActiveUIDocument.Document
    viewId = doc.ActiveView.Id
    elements = FilteredElementCollector(doc, viewId).WhereElementIsNotElementType().ToElements()
    categories = map(lambda e: e.Category, elements)
    for c in categories:
        if c == None:
            categories.remove(c)
    category_names = map(lambda c: c.Name, categories)
    category_name = []
    for c in category_names:
        if c not in category_name:
            category_name.append(c)
    return category_name
cbs = []
for c in getCategoriesInActiveView():
    cb = Controls.CheckBox()
    cb.Content = c
    cbs.append(cb)
class MyWindow(Window):

    def __init__(self):

        wpf.LoadComponent(self, xamlfile)

        self.Icon = Media.Imaging.BitmapImage(Uri(dir_name + "\portcoast.ico", UriKind.Relative))

        self.lbCategories.ItemsSource = cbs

MyWindow().ShowDialog()
