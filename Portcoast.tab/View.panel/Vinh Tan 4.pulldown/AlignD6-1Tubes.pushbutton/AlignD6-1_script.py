# -*- coding: utf-8 -*-
# =============================================================================
# 
# =============================================================================


__title__ = "Tranfer"
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

import System

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# =============================================================================
# Functions
# =============================================================================

def get_ViewType(document):
    view_class_collector = DB.FilteredElementCollector(document).OfCategory(OST_Views)
    list_ViewType = list()
    for i in view_class_collector:
        if i.GetType() not in list_ViewType:
            list_ViewType.append(i.GetType())
    return list_ViewType

  
# =============================================================================
# End Get View Type
# =============================================================================

dir_name = os.path.dirname(__file__)
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# =============================================================================
#Declare some Dialogs
# =============================================================================


# =============================================================================
# 
# =============================================================================

def execute():

    ref1 = None
    ref2 = None

    sel1 = uidoc.Selection
    sel2 = uidoc.Selection

    ref1 = sel1.PickObjects(Selection.ObjectType.Element, "Select Tubes")
    ref2 = sel2.PickObjects(Selection.ObjectType.Element, "Select Nodes")

    
if "__main__" == __name__:
    execute()