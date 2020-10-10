#! python3
import sys

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

# Get Revit active UI document
uidoc = __revit__.ActiveUIDocument

# Get Revit current document
doc = uidoc.Document

# Get Revit application
app = __revit__.Application

framingCollector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()
framingList = []
for i in framingCollector:
    if not i.IsHidden(doc.ActiveView):
        framingList.append(i)
startPt = map(lambda x: x.Location.Curve.GetEndPoint(0), framingList)
endtPt = map(lambda x: x.Location.Curve.GetEndPoint(1), framingList)

floorCollector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()
for i in floorCollector:
    print(i.Location)