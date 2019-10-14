from pyfbsdk import *

#   for reference only

#   MotoinBuilder 2017

#   Aim Constraint 0
#   Expression Constraint 1
#   Multi Referential Constraint 2
#   Parent/Child Constraint 3
#   Path Constraint 4
#   Position Constraint 5
#   Range Constraint 6
#   Relation Constraint 7
#   Rigid Body Constraint 8
#   3 Points Constraint 9
#   Rotation Constraint 10
#   Scale Constraint 11
#   Mapping Constraint 12
#   Chain IK Constraint 13
#   Spline IK Constraint 14


##
## Scene Refresh Bug Work Around
##
## http://www.vicdebaie.com/blog/motionbuilder-python-library-aka-my-fav-functions/
##
def SceneRefresh():
    FBPlayerControl().GotoNextKey()
    FBSystem().Scene.Evaluate()
    FBPlayerControl().GotoPreviousKey()
    FBSystem().Scene.Evaluate()

def GetConstraintPrefix(CONSTRAINT_TYPE):
    lConsPrefix = "ParentChildCons_"
    if CONSTRAINT_TYPE == 5:
        lConsPrefix = "PositionCons_"
    if CONSTRAINT_TYPE == 10:
        lConsPrefix = "RotationCons_"
    return lConsPrefix


def SetConstraint(CONSTRAINT_TYPE, child, parent, _Weight=100, SNAP=False):

    lConsPrefix = GetConstraintPrefix(CONSTRAINT_TYPE)

    lMyCons = FBConstraintManager().TypeCreateConstraint(CONSTRAINT_TYPE)

    lMyCons.Name = lConsPrefix + child.Name

    #adding elements to the constraint slots
    lMyCons.ReferenceAdd(0, child)
    lMyCons.ReferenceAdd(1, parent)

    #setting up the snap option, so the elements will keep their position
    if SNAP is False:
        lMyCons.Snap()
    #weight of the constraint
    lMyCons.Weight = 100
    lMyCons.Active = False
    lMyCons.Snap()

    return lMyCons

def FindConstraintByName(constraintName):
    lConstraints = FBSystem().Scene.Constraints
    for constraint in lConstraints:
        if constraint.Name == constraintName:
            return constraint
    return None

def DeleteConstraintIfExist(constraintName):
    lConstraints = FBSystem().Scene.Constraints
    constraintsToDeleteList = []

    for constraint in lConstraints:
        if constraint.Name.startswith(constraintName):
            constraintsToDeleteList.append(constraint)

    for constraint in constraintsToDeleteList:
        print constraint.Name + " already exist. Deleting."
        constraint.FBDelete()

def SetConstraintForJoints(childName, parentName, SNAP, CONSTRAINT_TYPE=3):
    child = FBFindModelByLabelName(childName)
    parent = FBFindModelByLabelName(parentName)
    DeleteConstraintIfExist(GetConstraintPrefix(CONSTRAINT_TYPE) + child.Name)
    return SetConstraint(CONSTRAINT_TYPE, child, parent, 100, SNAP)

def SetJointRotation(jointName, rotX, rotY, rotZ):
    myJoint = FBFindModelByLabelName(jointName)
    if myJoint:
        myJoint.SetVector(FBVector3d(rotX, rotY, rotZ), FBModelTransformationType.kModelRotation, True)

def SelectBranch(topModel):
    '''
    Selects the given model and all of its descendants. Note that this
    function does not clear the current selection -- that's the caller's
    responsibility, if desired.
    '''
    for childModel in topModel.Children:
        SelectBranch(childModel)

    topModel.Selected = True


def SelectBranchWithoutFaceRig(topModel):
    '''
    Selects the given model and all of its descendants. Note that this
    function does not clear the current selection -- that's the caller's
    responsibility, if desired.
    '''
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

        SelectBranchWithoutFaceRig(childModel)

    topModel.Selected = True

def FindGroupByName(groupName):
    groups = FBSystem().Scene.Groups
    for group in groups:
        if group.Name == groupName:
            return group


def DeleteGroupIfExist(groupName):
    group = FindGroupByName(groupName)
    if group:
        print group.Name + " already exist. Deleting."
        group.FBDelete()


def DeselectAll():
    for comp in FBSystem().Scene.Components:
        comp.Selected = False

def SetSelectedModels(modelList):
    for model in modelList:
        model.Selected = True


def GetLastSelectedModel():
    '''
    Returns the most recently selected model in the scene, or
    None if no models are selected.
    '''
    selectedModels = FBModelList()
    FBGetSelectedModels(selectedModels, None, True, True)
    return selectedModels[-1] if selectedModels else None


def FindCharacterByName(charName):
    lCharacters = FBSystem().Scene.Characters
    for character in lCharacters:
        if character.Name == charName:
            return character
    return None

def ClearAnim(pNode):

    # The FCurve property will not be null on a terminal node.
    # i.e. the 'Lcl Translation' node will not have any animation on it
    # directly... only the sub-nodes 'X', 'Y' or 'Z' may have animation.
    if pNode.FCurve:

        # Ah! there is a FCurve! Let's remove all the keys.
        pNode.FCurve.EditClear()
    else:
        # Then we are dealing with a parent node. Let's look at it
        # children nodes.
        for lNode in pNode.Nodes:
            # Recursively call ourselves to deal with sub-nodes.
            ClearAnim(lNode)

            # Cleanup
            del lNode

# This recursive function finds the first and last keyframe of an
# animation node.
def FindLimits(pNode, pLLimit=None, pRLimit=None):
    # First let's see if the node has any keys
    if pNode.FCurve:
        # Got thru the list, updating the first and last frame if necessary.
        # Limits are initialised on first comparaison attempt.
        for lKey in pNode.FCurve.Keys:

            if pLLimit:
                if lKey.Time.Get() < pLLimit.Get():
                    pLLimit.Set(lKey.Time.Get())
            else:
                pLLimit = FBTime()
                pLLimit.Set(lKey.Time.Get())
            if pRLimit:
                if lKey.Time.Get() > pRLimit.Get():
                    pRLimit.Set(lKey.Time.Get())
            else:
                pRLimit = FBTime()
                pRLimit.Set(lKey.Time.Get())

    # If the node has any children nodes, we navigate those.
    if pNode.Nodes:
        for lNode in pNode.Nodes:
            (pLLimit, pRLimit) = FindLimits(lNode, pLLimit, pRLimit)

    return (pLLimit, pRLimit)


# Find the animation node recurvesive by name.
def FindAnimationNode(pName, pNode):
    lResult = None
    lName = pName.split('/')
    for lNode in pNode.Nodes:
        if lNode.Name == lName[0]:
            if len(lName) > 1:
                lResult = FindAnimationNode(pName.replace('%s/' % lName[0], ''), lNode)
            else:
                lResult = lNode
    return lResult

##Get Length Of Time Line / Get Time Line Frame Count
def GetTimeSpan():
    return FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame() - FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()

##Set Time Line Length ie. SetTimeSpan(150, 200) Will Set The Time Line To Start At Frame 150 And End At Frame 200
def SetTimeSpan(start, end):
    FBSystem().CurrentTake.LocalTimeSpan = FBTimeSpan(FBTime(0, 0, 0, start, 0), FBTime(0, 0, 0, end, 0))

##Plot Clip
def PlotStoryClip():
    if FBApplication().CurrentCharacter is None:
        print 'None character to plot story clip'
        return

    oldCurrentFrame = FBSystem().LocalTime.GetFrame(FBTimeMode.kFBTimeModeDefault)
    FBPlayerControl().Stop()
    FBPlayerControl().GotoStart()

    ##Deal With The User's Story Mode Activity
    FBStory().Mute = False
    SceneRefresh()

    ##Plot Options
    lPlotClipOptions = FBPlotOptions()
    lPlotClipOptions.ConstantKeyReducerKeepOneKey = False
    lPlotClipOptions.PlotAllTakes = False
    lPlotClipOptions.PlotOnFrame = True
    lPlotClipOptions.PlotPeriod = FBTime(0, 0, 0, 1)
    lPlotClipOptions.PlotTranslationOnRootOnly = False
    lPlotClipOptions.PreciseTimeDiscontinuities = False
    lPlotClipOptions.RotationFilterToApply = FBRotationFilter.kFBRotationFilterUnroll
    lPlotClipOptions.UseConstantKeyReducer = False
    ##Plot Story Clip On Current Character
    lChar = FBApplication().CurrentCharacter
    lChar.PlotAnimation(FBCharacterPlotWhere.kFBCharacterPlotOnControlRig, lPlotClipOptions)

    SceneRefresh()
    FBPlayerControl().Goto(FBTime(0, 0, 0, oldCurrentFrame, 0))
    SceneRefresh()


##Go Through The Story And Delete The Track Created By This Script
def CleanStoryTrack():
    iTracks = len(FBStory().RootFolder.Tracks)
    while iTracks > 0:
        FBStory().RootFolder.Tracks[0].FBDelete()
        iTracks = len(FBStory().RootFolder.Tracks)
