
__title__ = "Import OBJ"

import time

start = time.time()

import sys
import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

clr.AddReference('System.Windows.Forms')
import System
from System.Windows.Forms import OpenFileDialog, DialogResult
from System.Collections.Generic import List

objIndices = []
objNames = []
obj = []
vertices = []
# Get file path
filePath = "C:\\Users\\nhant\\AppData\\Roaming\\pyRevit-Master\\extensions\\portcoast.extension\\Portcoast.tab\\Meshing.panel\\obj-final.pushbutton\\eRTG.obj"

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

#Create Tessellated Shape Builder
builder = TessellatedShapeBuilder()

#Get inputted obj
with open(filePath, 'r') as scene:

    #Get object info
    for n, line in enumerate(scene):
        obj.append(line)
        split = line.split()

        if not len(split):
            continue
        
        if split[0] == "o":
            objIndices.append(int(n))
            objNames.append(split[1:][0])
        
        if split[0] == "v":
            vertex = map(lambda i: float(i)*1000, split[1:])
            vertices.append(XYZ(vertex[0], vertex[2], vertex[1]))

    n = int(0)    
#    while n < (len(objNames) - 1):
    while n < 2:
        
        print("Step: {}".format(n))
        
        #Build Tessellated Shape Proxy
        builder.Clear()
        builder.OpenConnectedFaceSet(False)
        
        for line in obj[objIndices[n]:objIndices[n+1]]:
            
            #But need to think about GraphicStyle
            graphicStyle = FilteredElementCollector(doc).OfClass(GraphicsStyle).FirstElementId()
            
            #But need to construct material from .mtl file
            materialCollector = FilteredElementCollector(doc).OfClass(Material).ToElements()
            for i in materialCollector:
                if i.Name == "Default":
                    defaultMaterial = i.Id
        
            #Get vertices of faces
            split = line.split()
            indices = []
            
            if "f" == split[0]:
                if 2 < len(split[1:]) < 5:
                    if "//" in ''.join(split[1:]):
                        indices = map(lambda x: int(x.split("//")[0]) ,split[1:])
                    elif "/" in ''.join(split[1:]):
                        indices = map(lambda x: int(x.split("/")[0]) ,split[1:])       
                loopVertices = List[XYZ](4)
                for index in indices:

                    loopVertices.Add(vertices[index-1])
                    
                tessellatedFace = TessellatedFace(loopVertices, defaultMaterial)
                    
                if builder.DoesFaceHaveEnoughLoopsAndVertices(tessellatedFace):
                    builder.AddFace(tessellatedFace)
            
        builder.CloseConnectedFaceSet()
                
        builder.Target = TessellatedShapeBuilderTarget.Mesh
        builder.Fallback = TessellatedShapeBuilderFallback.Abort
        
        builder.Build()
        
        result = builder.GetBuildResult()
            
        # Create Direct Shape
        trans = Transaction(doc, 'CreateDirectShape')
        trans.Start()
        try:
            directShape = DirectShape.CreateElement(doc, ElementId(BuiltInCategory.OST_GenericModel))
            directShape.ApplicationId = str(app.ActiveAddInId)
            directShape.SetName(objNames[n])
            directShape.SetShape(result.GetGeometricalObjects())
        
            trans.Commit()
        except Exception as error:
            TaskDialog.show("Exception", error)
            trans.RollBack()
            break
        n += 1
        
time.sleep(1)
end = time.time()
print("Runtime of software is {}".format(end - start))