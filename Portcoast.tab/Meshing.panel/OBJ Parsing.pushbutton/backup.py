import time

import sys
import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('System.Windows.Forms')
import System
from System.Windows.Forms import OpenFileDialog, DialogResult
from System.Collections.Generic import List
# Define function

vertices = list()
textures = list()
indices = list()

objectName = "Sample"

def main():
    doc = __revit__.ActiveUIDocument.Document
    app = __revit__.Application
    
    # Get input obj
    fileDialog = OpenFileDialog()
    fileDialog.Filter = "OBJ Geometry Format (*.obj)|*.obj|All files (*.*)|*.*"
    if fileDialog.ShowDialog() == DialogResult.OK:
        fileName = fileDialog.FileName
    else:
        sys.exit()

    # Start counting runtime
    start = time.time()
    
    # Open obj file
    scene = open(fileName, 'r')
    
    for line in scene:
        split = line.split()
        
        # If line is blank
        if not len(split):
            continue
        
        # Get geometry vertices
        if split[0] == "v":
            vertex = map(lambda x: float(x), split[1:])
            vertices.append(XYZ(vertex[0], vertex[2], vertex[1]))
            
        # Get texture vertices
        elif split[0] == "vt":
            
            textures.append(split[1:])
        
        # Get index of vertex
        elif split[0] == "f":
            index = list()

            if 2 < len(split[1:]) < 5:
                
                for i in split[1:]:

                    # If face contain texture infomation
                    if "/" in i:
                        
                        index.append(int(i.split("/")[0]))
                        
                    # If face does not contain texture infomation
                    else:
                        
                        index.append(int(i))
                
                indices.append(index)

    # Close obj file            
    scene.close()
    
    # Build Tessellated Shape Proxy
    graphicStyle = FilteredElementCollector(doc).OfClass(GraphicsStyle).ToElements()

    defaultMaterial = ElementId(23)
    
    graphicStyle = ElementId(132)
    
    builder = TessellatedShapeBuilder()

    builder.OpenConnectedFaceSet(False)
    
    for index in indices:
        
        loopVertices = List[XYZ](4)
        
        for i in index:
            
            loopVertices.Add(vertices[i-1])
            
        tessellatedFace = TessellatedFace(loopVertices, defaultMaterial)
        
        builder.AddFace(tessellatedFace)
        
        builder.DoesFaceHaveEnoughLoopsAndVertices(tessellatedFace)
        
    builder.CloseConnectedFaceSet()
    
    builder.Target = TessellatedShapeBuilderTarget.AnyGeometry
    
    builder.Fallback = TessellatedShapeBuilderFallback.Mesh
    
    builder.GraphicsStyleId = graphicStyle
    
    builder.Build()
        
    result = builder.GetBuildResult()
    print(type(result))
    
    # Create Direct Shape
    trans = Transaction(doc, 'DirectShape')
    trans.Start()
    try:
        directShape = DirectShape.CreateElement(doc, ElementId(BuiltInCategory.OST_GenericModel))
        
        directShape.ApplicationId = str(app.ActiveAddInId)
        
        directShape.SetName(objectName)
        
        directShape.SetShape(result.GetGeometricalObjects())
        
        trans.Commit()
    except Exception as error:
        print(error)
        trans.RollBack()
    # End counting runtime
    time.sleep(1)
    end = time.time()
    print("Runtime of program is {}".format(end-start))

if __name__=="__main__":
    main()
