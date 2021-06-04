__title__ = "Add Coordinate Values"

try:
    import System
    import os
    import math
    import clr
    clr.AddReference('RevitAPI')
    clr.AddReference('RevitAPIUI')
    from Autodesk.Revit.DB import *
    from Autodesk.Revit.DB.BuiltInCategory import *
    from Autodesk.Revit.UI import *

    from datetime import datetime
    
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    app = __revit__.Application
    
    sels = map(lambda x: doc.GetElement(x), uidoc.Selection.GetElementIds())                                        # Get current selected elements
    
    piles_list = list(filter(lambda x: x.Category.Name == "Structural Foundations", sels))                          # Filter to get Structural Foundations
    
    project_base_point = FilteredElementCollector(doc).OfCategory(OST_ProjectBasePoint).ToElements()[0]             # Get Project Base Point
    a0 = -1*project_base_point.GetParameters("Angle to True North")[0].AsDouble()                                   # Recalculate Angle to True North
    
    shared_base_point = FilteredElementCollector(doc).OfCategory(OST_SharedBasePoint).ToElements()[0]               # Get Survey Base Point
    y_survey_global = shared_base_point.GetParameters("N/S")[0].AsDouble()                                          # Get N/S Component
    x_survey_global = shared_base_point.GetParameters("E/W")[0].AsDouble()                                          # Get E/W Component
    vec_survey_global = XYZ(x_survey_global, y_survey_global, 0)                                                    # Create vector pointing to global origin
    survey_vec_negate = shared_base_point.Position.Negate()                                                         # Then negative it

    vec_pile_local = []
    for i in piles_list:
        location = i.Location                                                                                       # Get location of every pile in selection
        if type(location) == LocationCurve:                                                                         ## if location is a curve
            if location.Curve.Direction.Z > 0:                                                                      # If direction is up
                vec_pile_local.append(location.Curve.GetEndPoint(1))                                                # Get end point
            if location.Curve.Direction.Z < 0:                                                                      # If direction is down
                vec_pile_local.append(location.Curve.GetEndPoint(0))                                                # Get start point
        elif type(location) == LocationPoint:                                                                       ## If location is point
            top_level = i.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM).AsDouble() + i.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM).AsDouble()    # Get pile cap elevation                                               
            vec_pile_local.append(location.Point.Add(XYZ(0,0,top_level)))

    vec_pile_global = []
    for i in vec_pile_local:
        vec_StoP = i.Add(survey_vec_negate)
        x_StoP = vec_StoP.X
        y_StoP = vec_StoP.Y
        new_X = x_StoP * math.cos(a0) - y_StoP * math.sin(a0)
        new_Y = x_StoP * math.sin(a0) + y_StoP * math.cos(a0)
        rotated_vec_StoP = XYZ(new_X, new_Y, 0)
        vec = rotated_vec_StoP.Add(vec_survey_global)
        vec_pile_global.append(vec)    
    
    x_guid = System.Guid("1178c195-a383-4a83-9df8-6a9c1707cb34")
    y_guid = System.Guid("34ad2963-e925-414a-89ba-e4320709a63a")
    lastEdited_guid = System.Guid("ca4b78ef-f317-469f-947b-ae5b9c5d3237")
    
    x_param_list = map(lambda e: e.get_Parameter(x_guid), piles_list)
    y_param_list = map(lambda e: e.get_Parameter(y_guid), piles_list)
    lastEdited_param_list = map(lambda e: e.get_Parameter(lastEdited_guid), piles_list)
    
    trans = Transaction(doc, "Set X Value")
    trans.Start()
    px_error_list = []
    py_error_list = []
    lastEdited_error_list = []
    
    for px, py, lastEdited, vec in zip(x_param_list, y_param_list, lastEdited_param_list, vec_pile_global):
        pxOk = px.Set(vec.Y)
        pyOk = py.Set(vec.X)
        lastEditedOk = lastEdited.Set(str(datetime.now().strftime("%c")))
        if not pxOk:
            px_error_list.append(px)
        if not pyOk:
            py_error_list.append(py)
        if not lastEditedOk:
            lastEdited_error_list.append(lastEditedOk)
    trans.Commit()
    if not px_error_list or not py_error_list:
        TaskDialog.Show("Succeed","Mission's completed!")
except Exception as error:
    TaskDialog.Show("Error",str(error))