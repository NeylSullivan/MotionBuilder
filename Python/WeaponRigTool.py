import os
from pyfbsdk import *
from pyfbsdk_additions import *

import libHazardMoBuFunctions
reload(libHazardMoBuFunctions)
from libHazardMoBuFunctions import *

def CreateMarkerForJoint(joint):
    jointName = joint.Name
    markerName = "CTRL_" + jointName
    
    marker = FBModelMarker(markerName)
    marker.Show = True
    marker.Size = 200
    if jointName == "WPN_Safetyswitch" or jointName == "WPN_Trigger":
        marker.PropertyList.Find('LookUI').Data = FBMarkerLook.kFBMarkerLookHardCross
    else:
        marker.PropertyList.Find('LookUI').Data = FBMarkerLook.kFBMarkerLookCube
    
    marker.ShadingMode = FBModelShadingMode.kFBModelShadingWire
    
    lTranslation = FBVector3d()
    joint.GetVector(lTranslation, FBModelTransformationType.kModelTranslation, True)
    marker.Translation = lTranslation
    lRotation = FBVector3d()
    joint.GetVector(lRotation, FBModelTransformationType.kModelRotation, True)
    marker.Rotation = lRotation
    
def MakeMarkers(topModel):
    CreateMarkerForJoint(topModel)    
    
    for childModel in topModel.Children:
        MakeMarkers(childModel)


def BtnCallback_MakeMarkers(control, event):
    DeselectAll()
    
    topModel = FBFindModelByLabelName("WPN_Root")
    MakeMarkers(topModel)
    DeselectAll()
    
def SetParentForCorrespondingMarkerChilds(topJoint):
    parentMarker = FBFindModelByLabelName("CTRL_" + topJoint.Name)

    for childModel in topJoint.Children:
        if childModel.Name.startswith("WPN_"):
            childMarker = FBFindModelByLabelName("CTRL_" + childModel.Name)
            
            if(parentMarker and childMarker):
                childMarker.Parent = parentMarker
                SetConstraintForJoints (childModel.Name, "CTRL_" + childModel.Name, True)
                SetParentForCorrespondingMarkerChilds(childModel)
                
def FindParentForJointMarker(joint):
    marker = FBFindModelByLabelName("CTRL_" + joint.Name)
    if (marker == None):
        return #joint without marker
        
    while (joint.Parent):
        parentMarker = FBFindModelByLabelName("CTRL_" + joint.Parent.Name)
        if(parentMarker):
            marker.Parent = parentMarker
            break
        joint = joint.Parent
        
                
def SetParentForMarkers(topModel):
    FindParentForJointMarker(topModel)
    
    for childModel in topModel.Children:
        SetParentForMarkers(childModel)    
        
def SetConstraintsForJointsAndMarkers(topModel):
    #FindParentForJointMarker(topModel)
    marker = FBFindModelByLabelName("CTRL_" + topModel.Name)
    if(marker):
        SetConstraintForJoints (topModel.Name, "CTRL_" + topModel.Name, True)
    
    for childModel in topModel.Children:
        SetConstraintsForJointsAndMarkers(childModel)    
    
    
def BtnCallback_ReorganizeAndConstraint(control, event):
    DeselectAll()
    
    topJoint = FBFindModelByLabelName("WPN_Root")
    SetParentForMarkers(topJoint)
    SetConstraintsForJointsAndMarkers(topJoint)
        
    DeselectAll()

def PopulateLayout(mainLyt):
    x = FBAddRegionParam(5,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(5,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(-5,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(-5,FBAttachType.kFBAttachBottom,"")
    main = FBVBoxLayout(FBAttachType.kFBAttachTop)
    mainLyt.AddRegion("main","main", x, y, w, h)
    mainLyt.SetControl("main",main)
    
    b = FBButton()
    b.Caption = "Make Markers"
    # b.Justify = FBTextJustify.kFBTextJustifyLeft
    main.Add(b,30)
    b.OnClick.Add(BtnCallback_MakeMarkers)
    
    b = FBButton()
    b.Caption = "Reorganize and Constraint"
    # b.Justify = FBTextJustify.kFBTextJustifyLeft
    main.Add(b,30)
    b.OnClick.Add(BtnCallback_ReorganizeAndConstraint)
    
    
    
   
def CreateTool():
    # Tool creation will serve as the hub for all other controls
    t = FBCreateUniqueTool("Weapon Rig Tool")
    t.StartSizeX = 200
    t.StartSizeY = 260
    PopulateLayout(t)
    ShowTool(t)
    

CreateTool()