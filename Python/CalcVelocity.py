from pyfbsdk import *
import math

def GetPointsDistance(start, end):
    root = (end[0] - start[0])*(end[0] - start[0]) + (end[1] - start[1])*(end[1] - start[1]) + (end[2] - start[2])*(end[2] - start[2])
    return math.sqrt(root)

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


    #print startPos
    #print endPos

    distance = GetPointsDistance(startPos, endPos)
    #print distance # distance
    time = GetTimeSpan()
    #print time # time
    velocity = distance / time
    #print velocity

    lStartFrame = FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()
    lEndFrame = FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()

    lMessage = "Selected model: {}\n\n".format(model.Name)
    lMessage += "Start Frame: {}, Pos: ({:.1f}, {:.1f}, {:.1f})\n".format(lStartFrame, startPos[0], startPos[1], startPos[2])
    lMessage += "End Frame: {}, Pos: ({:.1f}, {:.1f}, {:.1f})\n\n\n".format(lEndFrame, endPos[0], endPos[1], endPos[2])
    lMessage += "Time: {:.2f}\n".format(time)
    lMessage += "Distance: {:.1f}\n".format(distance)
    lMessage += "Velocity: {:.1f}\n\n\n".format(velocity)
    lMessage += "*** GUESSED TIME WARPING VALUES ***\n\n"


    for i in range(1, 9):
        guessedSpeed = 100.0 * i
        scaleFactor = velocity / guessedSpeed
        guessedTime = time * scaleFactor
        guessedFrames = int((lEndFrame-lStartFrame) * scaleFactor)

        lMessage += 'Speed: {}, Time: {:.2f} Frames: {:03d}\n '.format(guessedSpeed, guessedTime, guessedFrames)

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
