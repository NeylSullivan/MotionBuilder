from pyfbsdk import *
from pyfbsdk_additions import *
from libHazardMoBuFunctions import *
import libHazardMoBuFunctions
import libHazardCustomRigUtils as hazCustomRig
import libHazardBoneMapUtils as hazBoneMap
import libHazardUIExtension
from libHazardUIExtension import *
reload(libHazardMoBuFunctions)
reload(hazCustomRig)
reload(hazBoneMap)
reload(libHazardUIExtension)



def BtnCallback_SetTPose(_control, _event):
    lScene = FBSystem().Scene

    lScene.Evaluate()
    SetJointRotation("Arm_L", 90, 0, 0)
    lScene.Evaluate()
    SetJointRotation("ForeArm_L", 90, 0, 0)
    lScene.Evaluate()
    SetJointRotation("Hand_L", 90, 0, 0)
    lScene.Evaluate()
    SetJointRotation("Arm_R", 90, 0, 180)
    lScene.Evaluate()
    SetJointRotation("ForeArm_R", 90, 0, 180)
    lScene.Evaluate()
    SetJointRotation("Hand_R", 90, 0, 180)
    lScene.Evaluate()

    #experimental
    SetJointRotation("UpLeg_L", 90, 0, -90)
    lScene.Evaluate()
    SetJointRotation("UpLeg_R", 90, 0, -90)
    lScene.Evaluate()
    SetJointRotation("Leg_L", 90, 0, -90)
    lScene.Evaluate()
    SetJointRotation("Leg_R", 90, 0, -90)
    lScene.Evaluate()
    SetJointRotation("Foot_L", 90, 4, -90)
    lScene.Evaluate()
    SetJointRotation("Foot_R", 90, 4, -90)
    lScene.Evaluate()


def BtnCallback_ClearUnusedProperties(_control, _event):
    for topLevelModel in FBSystem().Scene.RootModel.Children:
        # Huge optimization
        ClearUserPropertiesRecursive(topLevelModel)

def AddJointToCharacter(characterObject, slot, jointName):
    myJoint = FBFindModelByLabelName(jointName)
    if myJoint:
        prop = characterObject.PropertyList.Find(slot + "Link") # Should return empty array
        if prop is not None: # so check it for 'if prop is not None:', not just a regular 'if prop:'
            prop.append(myJoint)
        else:
            print 'WARNING: Cannot find slot {} for adding to character {}'.format(slot, characterObject.Name)
    else:
        print 'WARNING: Cannot find joint {} for addingto character {}'.format(jointName, characterObject.Name)



def BtnCallback_DefineSkeleton(_control, _event):
    myCharacterName = "HazardCharacter"

    #myCharacter = FindCharacterByName(myCharacterName)

    myCharacter = FBCharacter(myCharacterName)
    FBApplication().CurrentCharacter = myCharacter

    fbp = FBProgress() # Create a FBProgress object and set default values for the caption and text.
    fbp.Caption = ""
    fbp.Text = " -----------------------------------   Creating Hazard Character"
    progress = 0.0
    #progresssteps = len(boneMap)

    boneMap = hazBoneMap.GetBoneMap()

    for pslot, pjointName in boneMap.iteritems(): # assign Biped to Character Mapping.
        AddJointToCharacter(myCharacter, pslot, pjointName)
        progress += 1
        val = progress / len(boneMap)  * 100
        fbp.Percent = int(val)

    FBSystem().Scene.Evaluate()
    myCharacter.SetCharacterizeOn(True)
    FBSystem().Scene.Evaluate()
    myCharacter.SetCharacterizeOff()
    FBSystem().Scene.Evaluate()

    print "Character mapping created for " + (myCharacter.LongName)

    fbp.FBDelete() # We must call FBDelete when the FBProgress object is no longer needed.


def BtnCallback_CreateControlRig(_control, _event):
    myCharacter = FBApplication().CurrentCharacter
    if myCharacter:
        if not myCharacter.GetCharacterize():
            myCharacter.SetCharacterizeOn(True)

        myCharacter.CreateControlRig(True)

        myCharacter.InputType = FBCharacterInputType.kFBCharacterInputMarkerSet
        myCharacter.ActiveInput = True

def BtnCallback_DestroyExistingRig(_control, _event):
    if FBApplication().CurrentCharacter:
        FBApplication().CurrentCharacter.GoToStancePose()



    myList = []
    for node in FBSystem().Scene.Characters:
        myList.append(node)
    SafeDeleteObjects(myList)
    del myList[:]

    for node in FBSystem().Scene.Constraints:
        myList.append(node)
    SafeDeleteObjects(myList)
    del myList[:]

    for node in FBSystem().Scene.CharacterExtensions:
        myList.append(node)
    SafeDeleteObjects(myList)
    del myList[:]

    for node in FBSystem().Scene.ControlSets:
        myList.append(node)
    SafeDeleteObjects(myList)
    del myList[:]

    for node in FBSystem().Scene.Handles:
        myList.append(node)
    SafeDeleteObjects(myList)
    del myList[:]

    for node in FBSystem().Scene.Devices:
        myList.append(node)
    SafeDeleteObjects(myList)
    del myList[:]

    for topLevelModel in FBSystem().Scene.RootModel.Children:
        if isinstance(topLevelModel, (FBModelPath3D, FBModelMarker)):
            myList.append(topLevelModel)

    map(FBComponent.FBDelete, myList)

    del myList[:]

    hudsToDelete = []
    elementsToDelete = []
    for hud in FBSystem().Scene.HUDs:
        for element in hud.Elements:
            elementsToDelete.append(element)
        hudsToDelete.append(hud)

    SafeDeleteObjects(elementsToDelete)

    for hud in hudsToDelete:
        for cam in FBSystem().Scene.Cameras:
            cam.DisconnectSrc(hud)
        FBSystem().Scene.DisconnectSrc(hud)
        hud.FBDelete()


    for node in FBSystem().Scene.Namespaces:
        myList.append(node)
    SafeDeleteObjects(myList)
    del myList[:]

    FBSystem().Scene.NamespaceCleanup()

def BtnCallback_CreateCustomRigSetup(_control, _event):
    reload(hazCustomRig)
    hazCustomRig.CreateCustomRigSetup()

def BtnCallback_AutorigAll(_control, _event):
    FBSystem().Scene.Evaluate()
    BtnCallback_DestroyExistingRig(None, None)
    FBSystem().Scene.Evaluate()
    BtnCallback_SetTPose(None, None)
    FBSystem().Scene.Evaluate()
    BtnCallback_ClearUnusedProperties(None, None)
    FBSystem().Scene.Evaluate()
    BtnCallback_DefineSkeleton(None, None)
    FBSystem().Scene.Evaluate()
    BtnCallback_CreateControlRig(None, None)
    FBSystem().Scene.Evaluate()
    BtnCallback_CreateCustomRigSetup(None, None)
    FBSystem().Scene.Evaluate()

def PopulateLayout(mainLyt):
    x = FBAddRegionParam(5, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(5, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(-5, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(-5, FBAttachType.kFBAttachBottom, "")
    main = FBVBoxLayout(FBAttachType.kFBAttachTop)
    mainLyt.AddRegion("main", "main", x, y, w, h)
    mainLyt.SetControl("main", main)

    with BorderedVertBoxLayout(mainLyt, 120, 'Autorig Tasks') as vert:
        LayoutButton(vert, 50, "AUTORIG ALL", BtnCallback_AutorigAll, Look=FBButtonLook.kFBLookColorChange, State0Color=FBColor(0.7, 0.3, 0), State1Color=FBColor(0, 1, 0))


    with BorderedVertBoxLayout(mainLyt, 215, 'Manual Tasks') as vert:
        LayoutButton(vert, 30, "Destroy Existing Rig", BtnCallback_DestroyExistingRig)
        LayoutButton(vert, 30, "Set T Pose", BtnCallback_SetTPose)
        LayoutButton(vert, 30, "Clear Unused Properties", BtnCallback_ClearUnusedProperties)
        LayoutButton(vert, 30, "Define Skeleton", BtnCallback_DefineSkeleton)
        LayoutButton(vert, 30, "Create Control Rig", BtnCallback_CreateControlRig)
        LayoutButton(vert, 30, "Create Custom Rig Setup", BtnCallback_CreateCustomRigSetup)


def CreateTool():
    t = FBCreateUniqueTool("Autorig Tool")
    t.StartSizeX = 200
    t.StartSizeY = 400
    PopulateLayout(t)
    ShowTool(t) #@UndefinedVariable

CreateTool()
