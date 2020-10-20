# -*- coding: utf-8 -*-

__title__ = "Ple Clash Detection"

import os
import sys
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *



def cal_MinDist(vectors, points):
    "Calculate min distance between 2 vectors"
    vec1 = vectors[0]
    vec2 = vectors[1]
    pt1 = points[0]
    pt2 = points[1]
    
    n = vec1.CrossProduct(vec2)
    d = pt1.Add(pt2.Negate()).DotProduct(n) / n.GetLength()
    return d

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
app = __revit__.Application

itemsSelected = uidoc.Selection
idsSelected = itemsSelected.GetElementIds()


directionVectorList = []
firstPointList = []

for id in idsSelected:
    
    # Get FamilyInstance
    element = doc.GetElement(id)
    
    # if selected elements are Structural Foundation
    if element.Category.Name == "Structural Foundations":
    
        # Get location (vector) of Element
        
        # If element is super-component
        if element.SuperComponent:
            
            print(element, "/n is SuperComponent")
            
            print(element.Location.Point)
            
            print("Coming Soon!")
        
        # if element is not super-component
        else:
            
            # Get location (vector) of Sub-Component
            subComponentVectorsList = map(lambda x: doc.GetElement(x).Location.Point, element.GetSubComponentIds())
            
            # Get list of z value of vector
            zValueList = map(lambda x: x.Z,subComponentVectorsList)
            
            # Get index of min/ max z component value
            indexOfMinZValue = zValueList.index(min(zValueList))
            
            indexOfMaxZValue = zValueList.index(max(zValueList))
            
            # Get vector which has the min/ max z component
            minZVector = subComponentVectorsList[indexOfMinZValue]
            
            maxZVector = subComponentVectorsList[indexOfMaxZValue]
            
            directionVectorList.append(maxZVector.Negate().Add(minZVector))
            
            firstPointList.append(maxZVector)
            
    # if selected elements are Structural Column
    elif element.Category.Name == "Structural Columns":
        print("Coming Soon!")
        pass
print("Distance:")
seq = min(len(directionVectorList), len(firstPointList))
for i in range(seq-1):
    for j in range(i, seq)
        vectors = [directionVectorList[i], directionVectorList[j]]
        pointss = [firstPointList[i], firstPointList[j]]
            for k in range(0, 1, .1)
                pt1 = points[0].Add(vectors[0].Multiply(k))
                
    if not n.IsZeroLength():
        
        d = pointList[0].Add(pointList[1].Negate()).DotProduct(n) / n.GetLength()
        print(d)
    else:
        
        d = firstPointList[0].DistanceTo(firstPointList[1])
        print(d)

    
