from pyfbsdk import *
from pyfbsdk_additions import *

import libHazardMoBuFunctions
reload(libHazardMoBuFunctions)
from libHazardMoBuFunctions import *

strictModeCheckBox = FBButton()


def MakeTempMarker(reference):
    markerName = "Temp_" + reference.Name + "_Marker"
    
    oldMarker = FBFindModelByLabelName(markerName)
    
    if oldMarker:
        print (markerName + " already exist. Deleting.")
        oldMarker.FBDelete()

    marker = FBModelMarker(markerName)
    marker.Look = FBMarkerLook.kFBMarkerLookSquare
    marker.Size = 4000
    marker.Color = FBColor(0,0,1)

    marker.Show = True

    lTranslation = FBVector3d()
    reference.GetVector(lTranslation, FBModelTransformationType.kModelTranslation, True)
    marker.Translation = lTranslation
    lRotation = FBVector3d()
    # reference.GetVector(lRotation, FBModelTransformationType.kModelRotation, True)
    # marker.Rotation = lRotation

    return marker

    
def SetTranslationDOF(marker, x, y, z):
    marker.PropertyList.Find( 'TranslationActive' ).Data = True
    marker.PropertyList.Find( 'TranslationMinX' ).Data = x
    marker.PropertyList.Find( 'TranslationMaxX' ).Data = x
    marker.PropertyList.Find( 'TranslationMinY' ).Data = y
    marker.PropertyList.Find( 'TranslationMaxY' ).Data = y
    marker.PropertyList.Find( 'TranslationMinZ' ).Data = z
    marker.PropertyList.Find( 'TranslationMaxZ' ).Data = z
    
def SetRotationDOF(marker, x, y, z):
    marker.PropertyList.Find( 'RotationActive' ).Data = True
    marker.PropertyList.Find( 'RotationMinX' ).Data = x
    marker.PropertyList.Find( 'RotationMaxX' ).Data = x
    marker.PropertyList.Find( 'RotationMinY' ).Data = y
    marker.PropertyList.Find( 'RotationMaxY' ).Data = y
    marker.PropertyList.Find( 'RotationMinZ' ).Data = z
    marker.PropertyList.Find( 'RotationMaxZ' ).Data = z

def GetRootName(): return "Root"
        
def GetHipsName(): return "Hips"
    
def ClearAnimOnSkeleton():
    ClearAnim(FBFindModelByLabelName(GetRootName()).AnimationNode)
    ClearAnim(FBFindModelByLabelName(GetRootName()).AnimationNode)

def BtnCallback_CreateMarkers(control, event):
    lRootMarker = MakeTempMarker(FBFindModelByLabelName(GetRootName()))
    lRootPositionConstraint = SetConstraintForJoints (lRootMarker.Name, GetHipsName(), True, 5)
    lRootRotationConstraint = SetConstraintForJoints (lRootMarker.Name, GetHipsName(), True, 10)
    
    SetTranslationDOF(lRootMarker, strictModeCheckBox.State, True, False)
    SetRotationDOF(lRootMarker, True, strictModeCheckBox.State, True)

    lHipsMarker = MakeTempMarker(FBFindModelByLabelName(GetHipsName()))
    lHipsConstraint = SetConstraintForJoints (lHipsMarker.Name, GetHipsName(), True)
    
def CheckboxCallback_StrictMode(control, event):
    lRootMarker = FBFindModelByLabelName("Temp_" + GetRootName() + "_Marker")
    if (lRootMarker):
        SetTranslationDOF(lRootMarker, strictModeCheckBox.State, True, False)
        SetRotationDOF(lRootMarker, True, strictModeCheckBox.State, True)
    
def BtnCallback_PlotToMarkers(control, event):
    lRootMarker = FBFindModelByLabelName("Temp_" + GetRootName() + "_Marker")
    lHipsMarker = FBFindModelByLabelName("Temp_" + GetHipsName() + "_Marker")
    
    DeselectAll()
    lRootMarker.Selected = True
    lHipsMarker.Selected = True
    
    FBSystem().CurrentTake.PlotTakeOnSelected(FBTime(0,0,0,1)) 
    
    DeselectAll()
    
def BtnCallback_DeleteConstraints(control, event):
    DeleteConstraintIfExist("PositionCons_Temp_" + GetRootName() + "_Marker")
    DeleteConstraintIfExist("RotationCons_Temp_" + GetRootName() + "_Marker")
    DeleteConstraintIfExist("ParentChildCons_Temp_" + GetHipsName() + "_Marker")
    
def BtnCallback_ConstraintSkeletonToMarkers(control, event):
    lHipsMarker = FBFindModelByLabelName("Temp_" + GetHipsName() + "_Marker")
    lHipsConstraint = SetConstraintForJoints (GetHipsName(), lHipsMarker.Name, True)
    
    lRootMarker = FBFindModelByLabelName("Temp_" + GetRootName() + "_Marker")
    lRootConstraint = SetConstraintForJoints (GetRootName(), lRootMarker.Name, True)
    
def BtnCallback_PlotToSkeleton(control, event):
    lRoot = FBFindModelByLabelName(GetRootName())
    lHips = FBFindModelByLabelName(GetHipsName())
    
    DeselectAll()
    lRoot.Selected = True
    lHips.Selected = True
    
    FBSystem().CurrentTake.PlotTakeOnSelected(FBTime(0,0,0,1)) 
    
    DeselectAll()

def BtnCallback_DeleteMarkers(control, event):
    lRootMarker = FBFindModelByLabelName("Temp_" + GetRootName() + "_Marker")
    lRootMarker.FBDelete()
    lHipsMarker = FBFindModelByLabelName("Temp_" + GetHipsName() + "_Marker")
    lHipsMarker.FBDelete()
    
    DeleteConstraintIfExist("ParentChildCons_" + GetRootName())
    DeleteConstraintIfExist("ParentChildCons_" + GetRootName())
    

def BtnCallback(control, event):
    print control.Caption, " has been clicked!"

def PopulateLayout(mainLyt):
    x = FBAddRegionParam(5,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(5,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(-5,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(-5,FBAttachType.kFBAttachBottom,"")
    main = FBVBoxLayout(FBAttachType.kFBAttachTop)
    mainLyt.AddRegion("main","main", x, y, w, h)
    mainLyt.SetControl("main",main)
    
    b = FBButton()
    b.Caption = "Create Markers"
    # b.Justify = FBTextJustify.kFBTextJustifyLeft
    main.Add(b,30)
    b.OnClick.Add(BtnCallback_CreateMarkers)
    
    
    strictModeCheckBox.Caption = "Strict Mode"
    strictModeCheckBox.Hint = "For linear movement lock root DOF, allow only Z axis movement"
    strictModeCheckBox.Style = FBButtonStyle.kFBCheckbox 
    strictModeCheckBox.Justify = FBTextJustify.kFBTextJustifyLeft
    # b.State = True
    main.Add(strictModeCheckBox,20)
    strictModeCheckBox.OnClick.Add(CheckboxCallback_StrictMode)
    
    b = FBButton()
    b.Caption = "Plot Skeleton to Markers"
    main.Add(b,30)
    b.OnClick.Add(BtnCallback_PlotToMarkers)
    
    b = FBButton()
    b.Caption = "Delete Constraints"
    main.Add(b,30)
    b.OnClick.Add(BtnCallback_DeleteConstraints)
    
    b = FBButton()
    b.Caption = "Constraint Skeleton To Markers"
    main.Add(b,30)
    b.OnClick.Add(BtnCallback_ConstraintSkeletonToMarkers)
    
    b = FBButton()
    b.Caption = "Plot Markers to Skeleton"
    main.Add(b,30)
    b.OnClick.Add(BtnCallback_PlotToSkeleton)
    
    b = FBButton()
    b.Caption = "Delete Markers"
    main.Add(b,30)
    b.OnClick.Add(BtnCallback_DeleteMarkers)


def CreateTool():
    # Tool creation will serve as the hub for all other controls
    t = FBCreateUniqueTool("Plot Root Motion")
    t.StartSizeX = 200
    t.StartSizeY = 280
    PopulateLayout(t)
    ShowTool(t)
    
    strictModeCheckBox.State = True
    

CreateTool()