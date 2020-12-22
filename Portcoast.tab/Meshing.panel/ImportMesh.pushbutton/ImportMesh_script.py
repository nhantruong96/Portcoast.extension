# -*- coding: utf-8 -*-


# =============================================================================
# 
# =============================================================================


__title__ = "OBJ Importer"
__Author__ = "Nhan Truong"

org = "Portcoast Consultant Corporation"
na = "Nhan Truong"
em = "nhan.tnt@portcoast.com.vn"
mo = "+84 379197306"


# =============================================================================
# 
# =============================================================================

import os

import sys

import io

import clr

clr.AddReference('RevitAPI')

import Autodesk

from Autodesk.Revit.DB import *

clr.AddReference('IronPython.Wpf')

import wpf

import pyrevit

from pyrevit import script

xamlfile = script.get_bundle_file('ui.xaml')

from System import Uri, UriKind

from System.Windows import Application, Window, Media, Controls, Forms

# =============================================================================
# 
# =============================================================================

dir_name = os.path.dirname(__file__)

uiapp = __revit__
uidoc = uiapp.ActiveUIDocument
doc = uidoc.Document

# Get input obj
def get_InputObj():
    fileDialog = Forms.OpenFileDialog()
    fileDialog.Filter = "OBJ Geometry Format (*.obj)|*.obj|All files (*.*)|*.*"
    if fileDialog.ShowDialog() == Forms.DialogResult.OK:
        objFileName = fileDialog.FileName
        materialFileName = objFileName.replace('.obj', '.mtl')
    else:
        sys.exit()
    return objFileName, materialFileName

class MyWindow(Window):

    def __init__(self):

        wpf.LoadComponent(self, xamlfile)

        self.Icon = Media.Imaging.BitmapImage(Uri(dir_name + "\portcoast.ico", UriKind.Relative))

    def btnInputObj_Click(self, sender, args):
        obj, mtl = get_InputObj()

        vertices = []
        with open(obj, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line[0] == 'v':
                    split_ = line.split()
                    vertices.append(split_[1:len(split_)])
        

# Show file dialog & Get Input Obj & Mtl file

# Run UI
MyWindow().ShowDialog()

