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
            vertices.append(XYZ(vertex[0], vertex[1], vertex[2]))
            
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
                        
            if len(index) == 4:

                tri_Index1 = [index[0], index[1], index[2]]
                
                tri_Index2 = [index[1], index[2], index[3]]
                
                indices.append(tri_Index1)
                
                indices.append(tri_Index2)

    # Close obj file            
    
    scene.close()
    
    defaultMaterial = ElementId(23)
    
    builder = TessellatedShapeBuilder()

    builder.OpenConnectedFaceSet(False)
    
    for index in indices:
        loopVertices = List[XYZ](map(lambda i: vertices[i-1], index))
        builder.AddFace(TessellatedFace(loopVertices, defaultMaterial))
        
    builder.CloseConnectedFaceSet()
    
    builder.Target = TessellatedShapeBuilderTarget.AnyGeometry
    
    builder.Fallback = TessellatedShapeBuilderFallback.Abort
    
    builder.Build()
    
    result = builder.GetBuildResult()
    
    # End counting runtime
    time.sleep(1)
    end = time.time()
    print("Runtime of program is {}".format(end-start))

if __name__=="__main__":
    main()
