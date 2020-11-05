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

clr.AddReference('IronPython.Wpf')

import wpf

import pyrevit

from pyrevit import script

xamlfile = script.get_bundle_file('UI.xaml')

from System import Uri, UriKind

from System.Windows import Application, Window, Media

# =============================================================================
# 
# =============================================================================

dir_name = os.path.dirname(__file__)

class MyWindow(Window):

    def __init__(self):

        wpf.LoadComponent(self, xamlfile)

        self.Icon = Media.Imaging.BitmapImage(Uri(dir_name + "\\portcoast.ico", UriKind.Relative))
    
MyWindow().ShowDialog()
