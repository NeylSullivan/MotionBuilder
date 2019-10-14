from pyfbsdk import *
from math import *

def GetPointsDistance(start, end):
    root = (end[0] - start[0])*(end[0] - start[0]) + (end[1] - start[1])*(end[1] - start[1]) + (end[2] - start[2])*(end[2] - start[2])
    return sqrt(root)

def SceneRefresh():
    FBPlayerControl().GotoNextKey()
    FBSystem().Scene.Evaluate()
    FBPlayerControl().GotoPreviousKey()
    FBSystem().Scene.Evaluate()

def GetTimeSpan():
    return FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetSecondDouble() - FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetSecondDouble()


def ProcessData(model):

    FBPlayerControl().GotoStart()
    FBSystem().Scene.Evaluate()
    startPos = FBVector3d()
    model.GetVector(startPos, FBModelTransformationType.kModelTranslation, True)

    FBPlayerControl().GotoEnd()
    FBSystem().Scene.Evaluate()
    endPos = FBVector3d()
    model.GetVector(endPos, FBModelTransformationType.kModelTranslation, True)

    #return to start
    FBPlayerControl().GotoStart()
    FBSystem().Scene.Evaluate()


    print startPos
    print endPos

    distance = GetPointsDistance(startPos, endPos)
    print distance # distance
    time = GetTimeSpan()
    print time # time
    velocity = distance / time
    print velocity

    lMessage = "Selected model: " + model.Name
    lMessage += "\n"
    lMessage += "\n" + "Start Frame: " + str(FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame())
    lMessage += ", Pos: (" + str(startPos[0]) + " ," + str(startPos[1]) + " ," + str(startPos[2]) + ")"
    lMessage += "\n" + "End Frame: " + str(FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame())
    lMessage += ", Pos: (" + str(endPos[0]) + " ," + str(endPos[1]) + " ," + str(endPos[2]) + ")"
    lMessage += "\n"
    lMessage += "\n" + "Time: " + str(time)
    lMessage += "\n" + "Distance: " + str(distance)
    lMessage += "\n"
    lMessage += "\n" + "Velocity: " + str(velocity)

    FBMessageBox(model.Name, lMessage, "OK", None, None)
    del lMessage

#Init
Scene = FBSystem().Scene
System = FBSystem()
Application = FBApplication()

selectedModels = FBModelList()
FBGetSelectedModels(selectedModels, None, True, True)
lastSelectedModel = selectedModels[-1] if selectedModels else None

if lastSelectedModel is None:
    lRoot = FBFindModelByLabelName("Root") #For new skeleton
    if lRoot is None:
        lRoot = FBFindModelByLabelName("root") #For original UE4 skeleton
    if lRoot is None: #still None? Abort
        FBMessageBox("Message", "Nothing selected and cann't find 'Root' or 'root' joint", "OK", None, None)
    else:
        ProcessData(lRoot)
else:
    ProcessData(lastSelectedModel)
