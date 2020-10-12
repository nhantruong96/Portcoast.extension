# -*- coding: utf-8 -*-

__title__ = "Get Current Time"

import os
import sys
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
app = __revit__.Application

itemsSelected = uidoc.Selection
idsSelected = itemsSelected.GetElementId()
