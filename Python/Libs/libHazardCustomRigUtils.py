import math
from pyfbsdk import *

def DeletePropertyIfExist(model, propName):
    lProp = model.PropertyList.Find(propName)
    if lProp:
        model.PropertyRemove(lProp)

def AddEnumProperty(model, propName, pAnimatable, stringList):
    DeletePropertyIfExist(model, propName)
    lProp = model.PropertyCreate(propName, FBPropertyType.kFBPT_enum, 'Enum', pAnimatable, True, None)
    lEnumList = lProp.GetEnumStringList(True) #Get Enum StringList and add new item.
    for s in stringList:
        lEnumList.Add(s)
    lProp.NotifyEnumStringListChanged() #Notify change, to let it take effect.
    lProp.SetAnimated(pAnimatable) # To make sure

def AddBoolProperty(model, propName, pAnimatable, bDefaultValue):
    DeletePropertyIfExist(model, propName)
    lProp = model.PropertyCreate(propName, FBPropertyType.kFBPT_bool, 'Bool', pAnimatable, True, None)
    lProp.Data = bDefaultValue
    lProp.SetAnimated(pAnimatable)

def DeleteModelIfExist(name):
    cl = FBComponentList()
    FBFindObjectsByName(name, cl, False, True) # First search by exact name
    if cl:
        for o in cl:
            o.FBDelete()
    cl = FBComponentList() #reinit
    FBFindObjectsByName(name + ' *', cl, False, True) #next by wildcard with space between name and (probably) number
    if cl:
        for o in cl:
            o.FBDelete()

def CreateArrow(name, color=FBColor(1.0, 1.0, 0.0)):
    DeleteModelIfExist(name)
    curve = FBModelPath3D(name)
    curve.Show = True
    curve.Visible = True
    curve.Color = color

    curve.PathKeyEndAdd(FBVector4d(0, 0, 60, 1))
    curve.PathKeyEndAdd(FBVector4d(-20, 0, 40, 1))
    curve.PathKeyEndAdd(FBVector4d(-10, 0, 40, 1))
    curve.PathKeyEndAdd(FBVector4d(-10, 0, -40, 1))
    curve.PathKeyEndAdd(FBVector4d(10, 0, -40, 1))
    curve.PathKeyEndAdd(FBVector4d(10, 0, 40, 1))
    curve.PathKeyEndAdd(FBVector4d(20, 0, 40, 1))
    curve.PathKeyEndAdd(FBVector4d(0, 0, 60, 1))

    #PATCH: Remove the two first point, they are unnecessary
    curve.PathKeyRemove(0)
    curve.PathKeyRemove(0)

    # tangents
    for i in range(0, curve.PathKeyGetCount()):
        vKeyPos = curve.PathKeyGet(i)
        curve.PathKeySetLeftTangent(i, vKeyPos)
        curve.PathKeySetRightTangent(i, vKeyPos)

    return curve

def CreateCircle(name, radius, steps=16, color=FBColor(1.0, 0.0, 1.0)):
    DeleteModelIfExist(name)
    curve = FBModelPath3D(name)
    curve.Show = True
    curve.Visible = True
    curve.Color = color

    angleStepRad = math.radians(360.0 / steps)

    for i in range(steps+1):
        x = radius * math.sin(i * angleStepRad)
        z = radius * math.cos(i * angleStepRad)
        curve.PathKeyEndAdd(FBVector4d(x, 0, z, 1))

    #Remove the two first point, they are unnecessary
    curve.PathKeyRemove(0)
    curve.PathKeyRemove(0)

    iLastIdx = curve.PathKeyGetCount()-1

    #fix end tangents
    startRightTangent = curve.PathKeyGetRightTangent(0)
    startRightTangent[2] = radius
    curve.PathKeySetRightTangent(0, startRightTangent)

    endLeftTangent = curve.PathKeyGetLeftTangent(iLastIdx)
    endLeftTangent[2] = radius
    curve.PathKeySetLeftTangent(iLastIdx, endLeftTangent)

    return curve

def CreateCompass(name, radius, color=FBColor(1.0, 0.0, 1.0)):
    # DeleteModelIfExist will be called from CreateCircle() function
    curve = CreateCircle(name, radius, 20, color)

    for i in [0, 20]:
        pos = curve.PathKeyGet(i)
        pos *= 1.4
        curve.PathKeySet(i, pos, True)
    for i in [0, 1, 19, 20]:
        vKeyPos = curve.PathKeyGet(i)
        curve.PathKeySetLeftTangent(i, vKeyPos)
        curve.PathKeySetRightTangent(i, vKeyPos)
    return curve

def CreateCircleWithArrow(name, radius, color=FBColor(1.0, 1.0, 0.0)):
    DeleteModelIfExist(name)
    curve = FBModelPath3D(name)
    curve.Show = True
    curve.Visible = True
    curve.Color = color

    points = [FBVector4d(0.000000, 0, 1.000000, 1),
              FBVector4d(0.309017, 0, 0.951057, 1),
              FBVector4d(0.587785, 0, 0.809017, 1),
              FBVector4d(0.809017, 0, 0.587785, 1),
              FBVector4d(0.951057, 0, 0.309017, 1),
              FBVector4d(1.000000, 0, 0.000000, 1),
              FBVector4d(0.951057, 0, -0.309017, 1),
              FBVector4d(0.809017, 0, -0.587785, 1),
              FBVector4d(0.587785, 0, -0.809017, 1),
              FBVector4d(0.200000, 0, -1.000000, 1),        # Arrow - 9
              FBVector4d(0.200000, 0, 0.000000, 1),         # Arrow - 10
              FBVector4d(0.600000, 0, 0.000000, 1),         # Arrow - 11
              FBVector4d(0.000000, 0, 0.900000, 1),         # Arrow - 12
              FBVector4d(-0.600000, 0, 0.00000, 1),         # Arrow - 13
              FBVector4d(-0.200000, 0, 0.00000, 1),         # Arrow - 14
              FBVector4d(-0.200000, 0, -1.000000, 1),       # Arrow - 15
              FBVector4d(-0.587785, 0, -0.809017, 1),
              FBVector4d(-0.809017, 0, -0.587785, 1),
              FBVector4d(-0.951057, 0, -0.309017, 1),
              FBVector4d(-1.000000, 0, 0.000000, 1),
              FBVector4d(-0.951057, 0, 0.309017, 1),
              FBVector4d(-0.809017, 0, 0.587785, 1),
              FBVector4d(-0.587785, 0, 0.809017, 1),
              FBVector4d(-0.309017, 0, 0.951057, 1),
              FBVector4d(0.000000, 0, 1.000000, 1)]

    for p in points:
        curve.PathKeyEndAdd(p * radius)

    #Remove the two first point, they are unnecessary
    curve.PathKeyRemove(0)
    curve.PathKeyRemove(0)

    # tangents
    for i in range(9, 16):
        vKeyPos = curve.PathKeyGet(i)
        curve.PathKeySetLeftTangent(i, vKeyPos)
        curve.PathKeySetRightTangent(i, vKeyPos)

    return curve

def CreateControlMarker(name, size, color=FBColor(1.0, 0.5, 0.0), markerLook=FBMarkerLook.kFBMarkerLookSquare):
    DeleteModelIfExist(name)
    marker = FBModelMarker(name)
    marker.Show = True
    marker.Size = size
    marker.Look = markerLook
    marker.Color = color
    marker.ShadingMode = FBModelShadingMode.kFBModelShadingWire

    return marker

def DeleteConstraintByName(pName):
    constraintsToDeleteList = []
    for constraint in FBSystem().Scene.Constraints:
        if constraint.Name.startswith(pName):
            constraintsToDeleteList.append(constraint)

    for constraint in constraintsToDeleteList:
        constraint.FBDelete()


def CreateRelaionConstraint(pName):
    DeleteConstraintByName(pName)
    newConstraint = FBConstraintRelation(pName)
    return newConstraint

def FindAnimationNode(pParent, pName):
    lResult = None
    for lNode in pParent.Nodes:
        if lNode.Name == pName:
            lResult = lNode
            break
    #If not found, try by Label (important for MACRO relation constraints)
    if lResult is None:
        for lNode in pParent.Nodes:
            if lNode.Label == pName:
                lResult = lNode
                break
    return lResult

def ConnectNodes(srcBox, srcProperty, dstBox, dstProperty):
    srcNode = FindAnimationNode(srcBox.AnimationNodeOutGet(), srcProperty)
    dstNode = FindAnimationNode(dstBox.AnimationNodeInGet(), dstProperty)
    if srcNode and dstNode:
        FBConnect(srcNode, dstNode)

def SetInputValue(dstBox, dstProperty, pData):
    dstNode = FindAnimationNode(dstBox.AnimationNodeInGet(), dstProperty)
    if dstNode:
        print 'set "{}" -> "{}" -> "{}"'.format(dstBox.Name, dstNode.Name, pData)
        if isinstance(pData, FBVector3d):
            dstNode.WriteData([pData[0], pData[1], pData[2]])
        if isinstance(pData, FBTime):
            print 'ERROR!!! Direct setting time is not suported. Use "Seconds to Time" converter instead'
        else:
            dstNode.WriteData([pData])
    else:
        print 'NO DST NODE FOUND "{}" -> "{}" -> "{}"'.format(dstBox.Name, dstNode.Name, pData)

def FindSrcBoxByName(relationConstraint, pName):
    for box in relationConstraint.Boxes:
        if box.Name == pName:
            return box
    return None

def CreateSrcBox(relationConstraint, model, useGlobalTransforms, posX, posY):
    srcBox = relationConstraint.SetAsSource(model)
    srcBox.UseGlobalTransforms = useGlobalTransforms
    relationConstraint.SetBoxPosition(srcBox, posX, posY)
    return srcBox

def CreateDstBox(relationConstraint, model, useGlobalTransforms, posX, posY):
    dstBox = relationConstraint.ConstrainObject(model)
    dstBox.UseGlobalTransforms = useGlobalTransforms
    relationConstraint.SetBoxPosition(dstBox, posX, posY)
    return dstBox

def CreateFuncBox(relationConstraint, pGroup, pName, posX, posY, newBoxName=None):
    funcBox = relationConstraint.CreateFunctionBox(pGroup, pName)
    relationConstraint.SetBoxPosition(funcBox, posX, posY)
    if newBoxName:
        funcBox.Name = newBoxName
    return funcBox

def CreateRootRelaionConstraint(rigCtrlModel, oRootCtrlMarker, hipsCtrlModel, oRootCtrlArrow, oRootArrow):# Relation constraint for root motion
    RC_Root = CreateRelaionConstraint('RC_Root')

    srcBoxRigCtrl = CreateSrcBox(RC_Root, rigCtrlModel, True, 100, 200)
    srcBoxCtrlMarker = CreateSrcBox(RC_Root, oRootCtrlMarker, True, 2400, 400)
    srcBoxRigHips = CreateSrcBox(RC_Root, hipsCtrlModel, True, 100, 600)

    # Process reference pos
    funcBoxSplitReferencePos = CreateFuncBox(RC_Root, 'Converters', 'Vector to Number', 1650, 50, 'Split reference pos')
    ConnectNodes(srcBoxRigCtrl, 'Translation', funcBoxSplitReferencePos, 'V')

    funcBoxCombineReferenceGroundedPos = CreateFuncBox(RC_Root, 'Converters', 'Number to Vector', 1950, 50, 'Reference XZ pos')
    ConnectNodes(funcBoxSplitReferencePos, 'X', funcBoxCombineReferenceGroundedPos, 'X')
    SetInputValue(funcBoxCombineReferenceGroundedPos, 'Y', 0.0)
    ConnectNodes(funcBoxSplitReferencePos, 'Z', funcBoxCombineReferenceGroundedPos, 'Z')

    # Process hips pos

    funcBoxSplitHipsPos = CreateFuncBox(RC_Root, 'Converters', 'Vector to Number', 400, 700, 'Split hips pos')
    ConnectNodes(srcBoxRigHips, 'Translation', funcBoxSplitHipsPos, 'V')

    funcBoxCombineHipsGroundedPos = CreateFuncBox(RC_Root, 'Converters', 'Number to Vector', 700, 700, 'Hips XZ Pos') ####
    ConnectNodes(funcBoxSplitHipsPos, 'X', funcBoxCombineHipsGroundedPos, 'X')
    SetInputValue(funcBoxCombineHipsGroundedPos, 'Y', 0.0)
    ConnectNodes(funcBoxSplitHipsPos, 'Z', funcBoxCombineHipsGroundedPos, 'Z')

    #Add root ofset calculation from zero frame

    funcBoxLocalTime = CreateFuncBox(RC_Root, 'System', 'Local Time', 500, 430)

    funcBoxSecondsToTime = CreateFuncBox(RC_Root, 'Converters', 'Seconds to Time', 386, 482)
    SetInputValue(funcBoxSecondsToTime, 'Seconds', 0.0)

    funcBoxIsZeroFrame = CreateFuncBox(RC_Root, 'Time', 'Is Identical (T1 == T2)', 680, 460, 'Is zero frame')
    ConnectNodes(funcBoxLocalTime, 'Result', funcBoxIsZeroFrame, 'T1')
    ConnectNodes(funcBoxSecondsToTime, 'Result', funcBoxIsZeroFrame, 'T2')

    funcBoxMemoryHipsOffset = CreateFuncBox(RC_Root, 'Vector', 'Memory (V1 when REC)', 1000, 700, 'Memory hips offset')
    ConnectNodes(funcBoxIsZeroFrame, 'Result', funcBoxMemoryHipsOffset, 'REC')
    ConnectNodes(funcBoxCombineHipsGroundedPos, 'Result', funcBoxMemoryHipsOffset, 'V1')

    fb_applyHipsOffset = CreateFuncBox(RC_Root, 'Vector', 'IF Cond Then A Else B', 1300, 800, 'If apply hips offset')
    ConnectNodes(funcBoxMemoryHipsOffset, 'Result', fb_applyHipsOffset, 'a')
    SetInputValue(fb_applyHipsOffset, 'b', FBVector3d(0, 0, 0))
    ConnectNodes(srcBoxRigCtrl, 'Apply hips offset', fb_applyHipsOffset, 'Cond')


    funcBoxSubtractHipsOffset = CreateFuncBox(RC_Root, 'Vector', 'Subtract (V1 - V2)', 1250, 600)
    ConnectNodes(funcBoxCombineHipsGroundedPos, 'Result', funcBoxSubtractHipsOffset, 'V1')
    ConnectNodes(fb_applyHipsOffset, 'Result', funcBoxSubtractHipsOffset, 'V2')


    fb_SplitHipsXZPos = CreateFuncBox(RC_Root, 'Converters', 'Vector to Number', 1550, 600, 'Split hips XZ pos')
    ConnectNodes(funcBoxSubtractHipsOffset, 'Result', fb_SplitHipsXZPos, 'V')

    fb_CombineHipXPos = CreateFuncBox(RC_Root, 'Converters', 'Number to Vector', 2050, 700, 'Hips X Pos') ####
    ConnectNodes(fb_SplitHipsXZPos, 'X', fb_CombineHipXPos, 'X')
    SetInputValue(fb_CombineHipXPos, 'Y', 0.0)
    SetInputValue(fb_CombineHipXPos, 'Z', 0.0)

    fb_CombineHipZPos = CreateFuncBox(RC_Root, 'Converters', 'Number to Vector', 2050, 600, 'Hips Z Pos') ####
    SetInputValue(fb_CombineHipZPos, 'X', 0.0)
    SetInputValue(fb_CombineHipZPos, 'Y', 0.0)
    ConnectNodes(fb_SplitHipsXZPos, 'Z', fb_CombineHipZPos, 'Z')



    #######
    #######
    #######
    fb_switch_rot = CreateFuncBox(RC_Root, 'My Macros', 'MACRO_RC_SWITCH', 2800, 200, 'Switch Rot')
    ConnectNodes(srcBoxRigCtrl, 'Root Mode', fb_switch_rot, 'Index')
    SetInputValue(fb_switch_rot, 'Input 0', FBVector3d(0, 0, 0))
    SetInputValue(fb_switch_rot, 'Input 1', FBVector3d(0, 0, 0))
    SetInputValue(fb_switch_rot, 'Input 2', FBVector3d(0, 0, 0))
    ConnectNodes(srcBoxRigHips, 'Rotation', fb_switch_rot, 'Input 3') # Hips XZ mode
    ConnectNodes(srcBoxRigCtrl, 'Rotation', fb_switch_rot, 'Input 4') # Reference XZ mode
    ConnectNodes(srcBoxRigCtrl, 'Rotation', fb_switch_rot, 'Input 5') # Reference XYZ
    ConnectNodes(srcBoxCtrlMarker, 'Rotation', fb_switch_rot, 'Input 6') # Marker XYZ


    fb_switch_trs = CreateFuncBox(RC_Root, 'My Macros', 'MACRO_RC_SWITCH', 2800, 500, 'Switch Trs')
    ConnectNodes(srcBoxRigCtrl, 'Root Mode', fb_switch_trs, 'Index')

    SetInputValue(fb_switch_trs, 'Input 0', FBVector3d(0, 0, 0)) # Zero mode
    ConnectNodes(fb_CombineHipZPos, 'Result', fb_switch_trs, 'Input 1') # Hips Z mode
    ConnectNodes(fb_CombineHipXPos, 'Result', fb_switch_trs, 'Input 2') # Hips X mode
    ConnectNodes(funcBoxSubtractHipsOffset, 'Result', fb_switch_trs, 'Input 3') # Hips XZ mode
    ConnectNodes(funcBoxCombineReferenceGroundedPos, 'Result', fb_switch_trs, 'Input 4') # Reference XZ mode
    ConnectNodes(srcBoxRigCtrl, 'Translation', fb_switch_trs, 'Input 5') # Reference XYZ
    ConnectNodes(srcBoxCtrlMarker, 'Translation', fb_switch_trs, 'Input 6') # Marker XYZ



    # Final controlled objects
    dstBoxRootBone = CreateDstBox(RC_Root, FBFindModelByLabelName('Root'), True, 3500, 0)
    ConnectNodes(fb_switch_trs, 'Result', dstBoxRootBone, 'Translation')
    ConnectNodes(fb_switch_rot, 'Result', dstBoxRootBone, 'Rotation')

    dstBoxRootCtrlArrow = CreateDstBox(RC_Root, oRootCtrlArrow, True, 3500, 150)
    ConnectNodes(fb_switch_trs, 'Result', dstBoxRootCtrlArrow, 'Translation')
    ConnectNodes(fb_switch_rot, 'Result', dstBoxRootCtrlArrow, 'Rotation')

    # Make marker follow root when not in 'Marker XYZ' mode
    # funcBox_IF_MarkerNotFollowRootTrs = CreateFuncBox(RC_Root, 'Vector', 'IF Cond Then A Else B', 1500, 650, 'If marker NOT follow root (Trs)')
    # ConnectNodes(srcBoxCtrlMarker, 'Translation', funcBox_IF_MarkerNotFollowRootTrs, 'a') #use original marker translation
    # ConnectNodes(funcBox_IF_ZeroMode, 'Result', funcBox_IF_MarkerNotFollowRootTrs, 'b')
    # ConnectNodes(funcBoxIsFreeMode, 'Result', funcBox_IF_MarkerNotFollowRootTrs, 'Cond')

    # funcBox_IF_MarkerNotFollowRootRot = CreateFuncBox(RC_Root, 'Vector', 'IF Cond Then A Else B', 1500, 750, 'If marker NOT follow root (Rot)')
    # ConnectNodes(srcBoxCtrlMarker, 'Rotation', funcBox_IF_MarkerNotFollowRootRot, 'a') #use original marker rotation
    # ConnectNodes(srcBoxRigCtrl, 'Rotation', funcBox_IF_MarkerNotFollowRootRot, 'b')

    dstBoxCtrlMarker = CreateDstBox(RC_Root, oRootCtrlMarker, True, 3500, 300)
    # Translation and roation of marker will not be directly visible in viewport, but can be plotted to marker
    ConnectNodes(fb_switch_trs, 'Result', dstBoxCtrlMarker, 'Translation')
    ConnectNodes(fb_switch_rot, 'Result', dstBoxCtrlMarker, 'Rotation')
    ConnectNodes(fb_switch_trs, 'Is mode 6', dstBoxCtrlMarker, 'Visibility')# marker should be visible only in "Free" mode

    # Arrow constrained to root bone for visual reference
    srcBoxRootBone = CreateSrcBox(RC_Root, FBFindModelByLabelName('Root'), True, 3300, 550)
    dstBoxRootArrow = CreateDstBox(RC_Root, oRootArrow, True, 3600, 550)

    ConnectNodes(srcBoxRootBone, 'Rotation', dstBoxRootArrow, 'Rotation')
    ConnectNodes(srcBoxRootBone, 'Translation', dstBoxRootArrow, 'Translation')

    RC_Root.Active = True
    return RC_Root

def CreateMacroSwitchRelationConstraint():
    constraint = CreateRelaionConstraint('MACRO_RC_SWITCH')

    OUTPUTS_NUM = 7

    fb_IN_Mode = CreateFuncBox(constraint, 'Macro Tools', 'Macro Input Number', 10, 10, 'Index')
    FindAnimationNode(fb_IN_Mode.AnimationNodeOutGet(), 'Input').Label = 'Index'

    trsInputs = []

    for i in range(OUTPUTS_NUM):
        fb_IN_trs = CreateFuncBox(constraint, 'Macro Tools', 'Macro Input Vector', 800, 10 + (i*100), 'Input {}'.format(i))
        FindAnimationNode(fb_IN_trs.AnimationNodeOutGet(), 'Input').Label = 'Input {}'.format(i)
        trsInputs.append(fb_IN_trs)
        fb_IN_trs = None

    fb_OUT_Trs = CreateFuncBox(constraint, 'Macro Tools', 'Macro Output Vector', 1300, 10, 'Result')
    FindAnimationNode(fb_OUT_Trs.AnimationNodeInGet(), 'Output').Label = 'Result'

    prev_IfTrsBox = None

    for i in range(OUTPUTS_NUM):

        fb_IsMode = CreateFuncBox(constraint, 'Number', 'Is Identical (a == b)', 300, 10 + (i*100), 'Is {}'.format(i))
        ConnectNodes(fb_IN_Mode, 'Input', fb_IsMode, 'a')
        SetInputValue(fb_IsMode, 'b', i)

        fb_OUT_Mode = CreateFuncBox(constraint, 'Macro Tools', 'Macro Output Bool', 600, 10 + (i*100), 'Out Mode {}'.format(i))
        FindAnimationNode(fb_OUT_Mode.AnimationNodeInGet(), 'Output').Label = 'Is mode {}'.format(i)
        ConnectNodes(fb_IsMode, 'Result', fb_OUT_Mode, 'Output')

        if i < OUTPUTS_NUM-1: # Dont create last 'IF' node
            fb_IF_Trs = CreateFuncBox(constraint, 'Vector', 'IF Cond Then A Else B', 1000, 10 + (i*100), 'If {} Vector'.format(i))
            ConnectNodes(fb_IsMode, 'Result', fb_IF_Trs, 'Cond')

        if i < OUTPUTS_NUM-1:
            ConnectNodes(trsInputs[i], 'Input', fb_IF_Trs, 'a')
        else: #connect to previous 'b' input
            ConnectNodes(trsInputs[i], 'Input', prev_IfTrsBox, 'b')


        if not prev_IfTrsBox: #Connct to main output
            ConnectNodes(fb_IF_Trs, 'Result', fb_OUT_Trs, 'Output')
        elif i < OUTPUTS_NUM-1: # Conncet to previous box 'b' input
            ConnectNodes(fb_IF_Trs, 'Result', prev_IfTrsBox, 'b')

        prev_IfTrsBox = fb_IF_Trs


    return constraint

def CreateIKBonesRelaionConstraint():
    constraint = CreateRelaionConstraint('RC_IKBones')

    # Correct order - dst, then src, cause multiple ik bones can be connected to single regular bone ('IK_Weapon_Root' and 'IK_Hand_R' to 'Hand_R')
    dstSrcMap = (('IK_Foot_L', 'Foot_L'),
                 ('IK_Foot_R', 'Foot_R'),
                 ('IK_Weapon_Root', 'Hand_R'),
                 ('IK_Hand_R', 'Hand_R'),
                 ('IK_Hand_L', 'Hand_L'),
                 ('IK_Hips', 'Hips'))

    vertPosOffset = 0
    for dstBone, srcBone in dstSrcMap:
        srcBox = FindSrcBoxByName(constraint, srcBone) # One src cand drive multiple dst
        if not srcBox:
            srcBox = CreateSrcBox(constraint, FBFindModelByLabelName(srcBone), True, 50, 50 + vertPosOffset)
        dstBox = CreateDstBox(constraint, FBFindModelByLabelName(dstBone), True, 500, 50 + vertPosOffset)

        ConnectNodes(srcBox, 'Rotation', dstBox, 'Rotation')
        ConnectNodes(srcBox, 'Translation', dstBox, 'Translation')

        vertPosOffset += 100

    constraint.Active = True
    return constraint

def MakeSkinnedMeshesUnpickable():
    for topLevelModel in FBSystem().Scene.RootModel.Children:
        if topLevelModel.IsDeformable:
            topLevelModel.Pickable = False

def SetModelRotationToOnlyVertical(pModel):
    pModel.QuaternionInterpolate = True
    pModel.RotationActive = True
    pModel.RotationMinX = True
    pModel.RotationMaxX = True
    pModel.RotationMinZ = True
    pModel.RotationMaxZ = True
    pModel.RotationOrder = FBModelRotationOrder.kFBSphericXYZ

def CreateCustomRigSetup():
    MakeSkinnedMeshesUnpickable()

    FBApplication().CurrentCharacter.GoToStancePose()

    rigCtrlModel = FBApplication().CurrentCharacter.GetCtrlRigModel(FBBodyNodeId.kFBReferenceNodeId)
    hipsCtrlModel = FBApplication().CurrentCharacter.GetCtrlRigModel(FBBodyNodeId.kFBHipsNodeId)

    AddEnumProperty(rigCtrlModel, 'Root Mode', True, ['Zero', 'Hips Z', 'Hips X', 'Hips XZ', 'Reference XZ', 'Reference XYZ', 'Marker XYZ'])
    AddBoolProperty(rigCtrlModel, 'Apply hips offset', True, bDefaultValue=True)

    oRootArrow = CreateCircleWithArrow('RootArrow', 50)
    # Set rotation limits to SKELETON BONE itself, not to 'RootArrow'!!! It will be constrained to bone anyway
    SetModelRotationToOnlyVertical(FBFindModelByLabelName('Root'))
    oRootArrow.Pickable = False
    oRootCtrlArrow = CreateCompass('RootCtrlArrow', 60)
    SetModelRotationToOnlyVertical(oRootCtrlArrow)
    oRootCtrlArrow.Pickable = False

    oRootCtrlMarker = CreateControlMarker('RootCtrlMarker', 10000.0)
    SetModelRotationToOnlyVertical(oRootCtrlMarker)
    # Enable rotation DOF


    oRootCtrlMarker.PropertyList.Find('Visibility').SetAnimated(True) # For relation constraint, marker visible when 'Root Mode' == 'Marker'

    DeleteConstraintByName('RC_Root') # HACK to prevent dialog popup about deleting used macro relation constraint

    CreateMacroSwitchRelationConstraint()
    RC_Root = CreateRootRelaionConstraint(rigCtrlModel, oRootCtrlMarker, hipsCtrlModel, oRootCtrlArrow, oRootArrow) # pylint: disable=unused-variable
    RC_IKBones = CreateIKBonesRelaionConstraint() # pylint: disable=unused-variable


    RC_Root.HardSelect()

    #Create reference properties
    refProp = RC_Root.PropertyList.Find('Active')
    rigCtrlModel.PropertyCreate('RC_Root Active', FBPropertyType.kFBPT_Reference, '', True, True, refProp)
