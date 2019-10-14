import os
from pyfbsdk import *
from pyfbsdk_additions import *
from libHazardMoBuFunctions import *
import libHazardMoBuFunctions
reload(libHazardMoBuFunctions)


def SelectBranchWithoutUnrelevantBones(topModel):

    modelName = topModel.Name

    if modelName.endswith("_TWIST"):
        return
    if modelName.endswith("_BEND"):
        return
    if modelName.endswith("_END"):
        return
    if modelName.endswith("_JIGGLE"):
        return
    if modelName.startswith("Nipple"):
        return

    for childModel in topModel.Children:
        if topModel.Name == "Head":
            childModelName = childModel.Name
            if childModelName.startswith("Eye_"):
                continue
            if childModelName.startswith("Ear_"):
                continue
            if childModelName == "UpperTeeth":
                continue
            if childModelName == "LowerJaw":
                continue
            if childModelName == "UpperFaceRig":
                continue

        SelectBranchWithoutUnrelevantBones(childModel)

    topModel.Selected = True


def BtnCallback_PlotToSkeleton(_control, _event):

    oldSelectedModels = FBModelList()
    FBGetSelectedModels(oldSelectedModels) #save selection

    DeselectAll()

    SelectBranchWithoutUnrelevantBones(FBFindModelByLabelName("Root"))

    lOptions = FBPlotOptions()
    lOptions.ConstantKeyReducerKeepOneKey = True
    lOptions.PlotAllTakes = False
    lOptions.PlotOnFrame = False
    lOptions.PlotPeriod = FBTime(0, 0, 0, 1)
    lOptions.PlotTranslationOnRootOnly = False
    lOptions.PreciseTimeDiscontinuities = False
    #lOptions.RotationFilterToApply = FBRotationFilter.kFBRotationFilterGimbleKiller
    lOptions.UseConstantKeyReducer = True


    #FBSystem().CurrentTake.PlotTakeOnSelected(FBTime(0,0,0,1))
    FBSystem().CurrentTake.PlotTakeOnSelected(lOptions)
    DeselectAll()
    print "Plot done"

    SetSelectedModels(oldSelectedModels) #restore selection

    # # Dont disable character input right now
    # currentChar = FBApplication().CurrentCharacter
    # if currentChar and currentChar.ActiveInput == True:
        # currentChar.ActiveInput = False
        # print "Character ActiveInput disabled"


def ResetAnimCurveToValue(node, animNodeName, newValue):
    animNode = FindAnimationNode(animNodeName, node.AnimationNode)
    animNode.FCurve.EditClear()
    for i in range(FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame(), FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()):
        animNode.FCurve.KeyAdd(FBTime(0, 0, 0, i), newValue)

def BtnCallback_ResetCameraIKBonePosition(_control, _event):
    node = FBFindModelByLabelName('IK_FPCam')

    FBSystem().CurrentTake.SetCurrentLayer(0) # Select base animation layer
    FBSystem().Scene.Evaluate()

    ResetAnimCurveToValue(node, 'Lcl Translation/X', 0)
    ResetAnimCurveToValue(node, 'Lcl Translation/Y', 0)
    ResetAnimCurveToValue(node, 'Lcl Translation/Z', 168) #up down TEMP VALUE

    FBSystem().Scene.Evaluate()

def BtnCallback_ResetCameraIKBoneRotation(_control, _event):
    node = FBFindModelByLabelName('IK_FPCam')

    FBSystem().CurrentTake.SetCurrentLayer(0) # Select base animation layer
    FBSystem().Scene.Evaluate()

    ResetAnimCurveToValue(node, 'Lcl Rotation/X', 0)
    ResetAnimCurveToValue(node, 'Lcl Rotation/Y', 0)
    ResetAnimCurveToValue(node, 'Lcl Rotation/Z', -90)

    FBSystem().Scene.Evaluate()

animExportDir = r'd:\CONTENT_SRC\Characters\Female\Anim'

def BtnCallback_ExportCurrentTake(_control, _event):

    oldSelectedModels = FBModelList()
    FBGetSelectedModels(oldSelectedModels) #save selection

    DeselectAll()
    SelectBranchWithoutUnrelevantBones(FBFindModelByLabelName("Root"))

    currentTake = FBSystem().CurrentTake

    finalFileName = currentTake.Name + ".fbx"
    lFilePath = os.path.join(animExportDir, finalFileName)

    print "File name: " + lFilePath

    lOptions = FBFbxOptions(False)

    # skip not current takes
    pTakeIndex = 0
    for take in FBSystem().Scene.Takes:
        if not take.Name == currentTake.Name:
            lOptions.SetTakeSelect(pTakeIndex, False)
        pTakeIndex += 1

    # Save only the selected models, in ASCII format so we can have a look at the file.
    lOptions.SaveSelectedModelsOnly = True
    lOptions.UseASCIIFormat = False

    # Not saving system information; only focus on the selected models.
    lOptions.BaseCameras = False
    lOptions.CameraSwitcherSettings = False
    lOptions.CurrentCameraSettings = False
    lOptions.GlobalLightingSettings = False
    lOptions.TransportSettings = False

    if FBApplication().FileSave(lFilePath, lOptions):
        print "File successfully saved to %s" % lFilePath
    else:
        print "Failed to save file: %s" % lFilePath

    DeselectAll()

    SetSelectedModels(oldSelectedModels) #restore selection



def PopulateLayout(mainLyt):
    x = FBAddRegionParam(5, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(5, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(-5, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(-5, FBAttachType.kFBAttachBottom, "")
    main = FBVBoxLayout(FBAttachType.kFBAttachTop)
    mainLyt.AddRegion("main", "main", x, y, w, h)
    mainLyt.SetControl("main", main)

    b = FBButton()
    b.Caption = "Plot to Skeleton"
    # b.Justify = FBTextJustify.kFBTextJustifyLeft
    main.Add(b, 30)
    b.OnClick.Add(BtnCallback_PlotToSkeleton)

    b = FBButton()
    b.Caption = "Export Current Take"
    main.Add(b, 30)
    b.OnClick.Add(BtnCallback_ExportCurrentTake)


def CreateTool():
    # Tool creation will serve as the hub for all other controls
    t = FBCreateUniqueTool("Plot Skeleton Final")
    t.StartSizeX = 200
    t.StartSizeY = 160
    PopulateLayout(t)
    ShowTool(t)

CreateTool()
