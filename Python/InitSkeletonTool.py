from pyfbsdk import *
from pyfbsdk_additions import *
from libHazardMoBuFunctions import *
import libHazardMoBuFunctions
reload(libHazardMoBuFunctions)

boneMap = {'Reference' : 'Root',
           'Hips' : 'Hips',
           'LeftUpLeg' : 'UpLeg_L',
           'LeftUpLegRoll' : 'UpLegTwist_L',
           'LeftLeg' : 'Leg_L',
           'LeftFoot' : 'Foot_L',
           'LeftToeBase' : 'Toe_L',
           'RightUpLeg' : 'UpLeg_R',
           'RightUpLegRoll' : 'UpLegTwist_R',
           'RightLeg' : 'Leg_R',
           'RightFoot' : 'Foot_R',
           'RightToeBase' : 'Toe_R',
           'Spine' : 'Spine_1',
           'Spine1' : 'Spine_2',
           'Spine2' : 'Spine_3',
           'Spine3' : 'Spine_4',
           'Neck' : 'Neck_1',
           'Neck1' : 'Neck_2',
           'Head' : 'Head',
           'LeftShoulder' : 'Clavicle_L',
           'LeftArm' : 'Arm_L',
           'LeftForeArm' : 'ForeArm_L',
           'LeftHand' : 'Hand_L',
           'RightShoulder' : 'Clavicle_R',
           'RightArm' : 'Arm_R',
           'RightForeArm' : 'ForeArm_R',
           'RightHand' : 'Hand_R',
           'LeftHandThumb1' : 'HandThumb1_L',
           'LeftHandThumb2' : 'HandThumb2_L',
           'LeftHandThumb3' : 'HandThumb3_L',
           'LeftInHandIndex' : 'HandIndex0_L',
           'LeftHandIndex1' : 'HandIndex1_L',
           'LeftHandIndex2' : 'HandIndex2_L',
           'LeftHandIndex3' : 'HandIndex3_L',
           'LeftInHandMiddle' : 'HandMid0_L',
           'LeftHandMiddle1' : 'HandMid1_L',
           'LeftHandMiddle2' : 'HandMid2_L',
           'LeftHandMiddle3' : 'HandMid3_L',
           'LeftInHandRing' : 'HandRing0_L',
           'LeftHandRing1' : 'HandRing1_L',
           'LeftHandRing2' : 'HandRing2_L',
           'LeftHandRing3' : 'HandRing3_L',
           'LeftInHandPinky' : 'HandPinky0_L',
           'LeftHandPinky1' : 'HandPinky1_L',
           'LeftHandPinky2' : 'HandPinky2_L',
           'LeftHandPinky3' : 'HandPinky3_L',
           'RightHandThumb1' : 'HandThumb1_R',
           'RightHandThumb2' : 'HandThumb2_R',
           'RightHandThumb3' : 'HandThumb3_R',
           'RightInHandIndex' : 'HandIndex0_R',
           'RightHandIndex1' : 'HandIndex1_R',
           'RightHandIndex2' : 'HandIndex2_R',
           'RightHandIndex3' : 'HandIndex3_R',
           'RightInHandMiddle' : 'HandMid0_R',
           'RightHandMiddle1' : 'HandMid1_R',
           'RightHandMiddle2' : 'HandMid2_R',
           'RightHandMiddle3' : 'HandMid3_R',
           'RightInHandRing' : 'HandRing0_R',
           'RightHandRing1' : 'HandRing1_R',
           'RightHandRing2' : 'HandRing2_R',
           'RightHandRing3' : 'HandRing3_R',
           'RightInHandPinky' : 'HandPinky0_R',
           'RightHandPinky1' : 'HandPinky1_R',
           'RightHandPinky2' : 'HandPinky2_R',
           'RightHandPinky3' : 'HandPinky3_R',
           'LeftHandThumb4' : 'HandThumb3_L_END',
           'LeftHandIndex4' : 'HandIndex3_L_END',
           'LeftHandMiddle4' : 'HandMid3_L_END',
           'LeftHandRing4' : 'HandRing3_L_END',
           'LeftHandPinky4' : 'HandPinky3_L_END',
           'RightHandThumb4' : 'HandThumb3_R_END',
           'RightHandIndex4' : 'HandIndex3_R_END',
           'RightHandMiddle4' : 'HandMid3_R_END',
           'RightHandRing4' : 'HandRing3_R_END',
           'RightHandPinky4' : 'HandPinky3_R_END',
           'LeafLeftUpLegRoll1' : 'UpLeg_L_TWIST',
           'LeafRightUpLegRoll1' : 'UpLeg_R_TWIST',
           'LeafLeftArmRoll1' : 'Arm_L_TWIST',
           'LeafLeftForeArmRoll1' : 'ForeArm_L_TWIST',
           'LeafRightArmRoll1' : 'Arm_R_TWIST',
           'LeafRightForeArmRoll1' : 'ForeArm_R_TWIST'}

def BtnCallback_SetIKConstraints(_control, _event):
    SetConstraintForJoints("IK_Foot_L", "Foot_L", False)
    SetConstraintForJoints("IK_Foot_R", "Foot_R", False)

    SetConstraintForJoints("IK_Weapon_Root", "Hand_R", False)
    SetConstraintForJoints("IK_Hand_R", "Hand_R", False)
    SetConstraintForJoints("IK_Hand_L", "Hand_L", False)

    SetConstraintForJoints("IK_Hips", "Hips", False)
    SetConstraintForJoints("IK_CAMERA", "FK_CAMERA_SOCKET", False)

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
    DeselectAll()

    SelectBranch(FBFindModelByLabelName("Root"))

    selectedModels = FBModelList()
    FBGetSelectedModels(selectedModels)

    for model in selectedModels:
        propList = model.PropertyList

        propNameList = []

        for prop in propList:
            if  prop.Name.startswith("mr displacement"):
                propNameList.append(prop.Name)

            if  prop.Name == "MaxHandle":
                propNameList.append(prop.Name)

            if prop.Name == "lockInfluenceWeights":
                propNameList.append(prop.Name)

        for propName in propNameList:
            model.PropertyRemove(model.PropertyList.Find(propName))

    DeselectAll()

def BtnCallback_CreateGroups(_control, _event):
    DeselectAll()

    # Select skeleton nodes (without face)
    SelectBranchWithoutFaceRig(FBFindModelByLabelName("Root"))

    selectedModels = FBModelList()
    FBGetSelectedModels(selectedModels)


    DeleteGroupIfExist('Plot_Group')
    plotGroup = FBGroup('Plot_Group')

    for model in selectedModels:
        plotGroup.Items.append(model)


    DeleteGroupIfExist('Export_Group')
    exportGroup = FBGroup('Export_Group')

    for model in selectedModels:
        modelName = model.Name
        if modelName.endswith("_TWIST"):
            continue
        if modelName.endswith("_JIGGLE"):
            continue
        if modelName.endswith("_END"):
            continue
        if modelName.startswith("Nipple_"):
            continue

        exportGroup.Items.append(model)

    DeselectAll()

def AddJointToCharacter(characterObject, slot, jointName):
    myJoint = FBFindModelByLabelName(jointName)
    if myJoint:
        proplist = characterObject.PropertyList.Find(slot + "Link")
        print myJoint.Name
        proplist.append(myJoint)



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


def PopulateLayout(mainLyt):
    x = FBAddRegionParam(5, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(5, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(-5, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(-5, FBAttachType.kFBAttachBottom, "")
    main = FBVBoxLayout(FBAttachType.kFBAttachTop)
    mainLyt.AddRegion("main", "main", x, y, w, h)
    mainLyt.SetControl("main", main)

    b = FBButton()
    b.Caption = "Set IK Constraints"
    # b.Justify = FBTextJustify.kFBTextJustifyLeft
    main.Add(b, 30)
    b.OnClick.Add(BtnCallback_SetIKConstraints)

    b = FBButton()
    b.Caption = "Set T Pose"
    # b.Justify = FBTextJustify.kFBTextJustifyLeft
    main.Add(b, 30)
    b.OnClick.Add(BtnCallback_SetTPose)

    b = FBButton()
    b.Caption = "Clear Unused Properties"
    # b.Justify = FBTextJustify.kFBTextJustifyLeft
    main.Add(b, 30)
    b.OnClick.Add(BtnCallback_ClearUnusedProperties)

    b = FBButton()
    b.Caption = "Create Plot/Export Groups"
    # b.Justify = FBTextJustify.kFBTextJustifyLeft
    main.Add(b, 30)
    b.OnClick.Add(BtnCallback_CreateGroups)

    b = FBButton()
    b.Caption = "Define Skeleton"
    # b.Justify = FBTextJustify.kFBTextJustifyLeft
    main.Add(b, 30)
    b.OnClick.Add(BtnCallback_DefineSkeleton)

    b = FBButton()
    b.Caption = "Create Control Rig"
    # b.Justify = FBTextJustify.kFBTextJustifyLeft
    main.Add(b, 30)
    b.OnClick.Add(BtnCallback_CreateControlRig)


def CreateTool():
    # Tool creation will serve as the hub for all other controls
    t = FBCreateUniqueTool("Init Skeleton Tool")
    t.StartSizeX = 200
    t.StartSizeY = 260
    PopulateLayout(t)
    ShowTool(t) #@UndefinedVariable

CreateTool()
