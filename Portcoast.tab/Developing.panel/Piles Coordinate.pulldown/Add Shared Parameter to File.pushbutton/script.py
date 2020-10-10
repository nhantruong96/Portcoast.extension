# -*- coding: utf-8 -*-

__tilte__ = "Add Shared Parameter to File (Alpha)"
import os
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

uiapp = __revit__
app = uiapp.Application

# Add Parameter

# Get File Name
dir_path = os.path.dirname(os.path.realpath(__file__))

# Assign Share File to Application
app.SharedParametersFilename = dir_path + "\SharedParameterFile.txt"

# Open Shared Parameter File
definition_File = app.OpenSharedParameterFile()

if definition_File:

    groups = definition_File.Groups
    
    for i in groups:

        externalDefinitions = i.Definitions

    sharedParams = []
    
    lastEdited = ExternalDefinitionCreationOptions("Last Edited", ParameterType.Text)
    lastEdited.UserModifiable = False
    sharedParams.append(lastEdited)
    
    X = ExternalDefinitionCreationOptions("X", ParameterType.Length)
    X.UserModifiable = False
    sharedParams.append(X)
    
    Y = ExternalDefinitionCreationOptions("Y", ParameterType.Length)
    Y.UserModifiable = False
    sharedParams.append(Y)
    
    for i in sharedParams:
        externalDefinitions.Create(i)