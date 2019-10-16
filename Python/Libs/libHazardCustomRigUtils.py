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

def CreateRelaionConstraint(name):
    constraintsToDeleteList = []
    for constraint in FBSystem().Scene.Constraints:
        if constraint.Name.startswith(name):
            constraintsToDeleteList.append(constraint)

    for constraint in constraintsToDeleteList:
        constraint.FBDelete()

    newConstraint = FBConstraintRelation(name)
    return newConstraint

def FindAnimationNode(pParent, pName):
    lResult = None
    for lNode in pParent.Nodes:
        if lNode.Name == pName:
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
            dstNode.WriteData([pData[0], pData[1], pData[2],])
        else:
            dstNode.WriteData([pData])

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

def CreateFuncBox(relationConstraint, pGroup, pName, posX, posY, newBoxNameSuffix=None):
    funcBox = relationConstraint.CreateFunctionBox(pGroup, pName)
    relationConstraint.SetBoxPosition(funcBox, posX, posY)
    if newBoxNameSuffix:
        funcBox.Name = '{}'.format(newBoxNameSuffix)
    return funcBox

def CreateRootRelaionConstraint(rigCtrlModel, oRootCtrlMarker, hipsCtrlModel, oRootCtrlArrow, oRootArrow):# Relation constraint for root motion
    RC_Root = CreateRelaionConstraint('RC_Root')

    srcBoxRigCtrl = CreateSrcBox(RC_Root, rigCtrlModel, True, 0, 300)
    srcBoxCtrlMarker = CreateSrcBox(RC_Root, oRootCtrlMarker, True, 1100, 400)
    srcBoxRigHips = CreateSrcBox(RC_Root, hipsCtrlModel, True, 0, 900)

    # Process reference pos
    funcBoxSplitReferencePos = CreateFuncBox(RC_Root, 'Converters', 'Vector to Number', 600, 600, 'Split reference pos')
    ConnectNodes(srcBoxRigCtrl, 'Translation', funcBoxSplitReferencePos, 'V')

    funcBoxCombineReferenceGroundedPos = CreateFuncBox(RC_Root, 'Converters', 'Number to Vector', 900, 600, 'Combine reference grounded pos')
    ConnectNodes(funcBoxSplitReferencePos, 'X', funcBoxCombineReferenceGroundedPos, 'X')
    SetInputValue(funcBoxCombineReferenceGroundedPos, 'Y', 0.0)
    ConnectNodes(funcBoxSplitReferencePos, 'Z', funcBoxCombineReferenceGroundedPos, 'Z')

    # Process hips pos

    funcBoxSplitHipsPos = CreateFuncBox(RC_Root, 'Converters', 'Vector to Number', 300, 900, 'Split hips pos')
    ConnectNodes(srcBoxRigHips, 'Translation', funcBoxSplitHipsPos, 'V')

    funcBoxRootUseSide = CreateFuncBox(RC_Root, 'Number', 'IF Cond Then A Else B', 600, 850, 'If root use side (X)')
    SetInputValue(funcBoxRootUseSide, 'b', 0.0)
    ConnectNodes(funcBoxSplitHipsPos, 'X', funcBoxRootUseSide, 'a')
    ConnectNodes(srcBoxRigCtrl, 'Root use side', funcBoxRootUseSide, 'Cond')

    funcBoxRootUseForward = CreateFuncBox(RC_Root, 'Number', 'IF Cond Then A Else B', 600, 944, 'If root use forward (Z)')
    SetInputValue(funcBoxRootUseForward, 'b', 0.0)
    ConnectNodes(funcBoxSplitHipsPos, 'Z', funcBoxRootUseForward, 'a')
    ConnectNodes(srcBoxRigCtrl, 'Root use forward', funcBoxRootUseForward, 'Cond')

    funcBoxCombineHipsGroundedPos = CreateFuncBox(RC_Root, 'Converters', 'Number to Vector', 950, 900, 'Combine hips grounded pos')
    ConnectNodes(funcBoxRootUseSide, 'Result', funcBoxCombineHipsGroundedPos, 'X')
    SetInputValue(funcBoxCombineHipsGroundedPos, 'Y', 0.0)
    ConnectNodes(funcBoxRootUseForward, 'Result', funcBoxCombineHipsGroundedPos, 'Z')

    # Check modes (switch like)
    funcBoxIsZeroMode = CreateFuncBox(RC_Root, 'Number', 'Is Identical (a == b)', 600, 0, 'Is Zero Mode')
    ConnectNodes(srcBoxRigCtrl, 'Root Mode', funcBoxIsZeroMode, 'a')
    SetInputValue(funcBoxIsZeroMode, 'b', 0)

    funcBoxIsHipsGroundedMode = CreateFuncBox(RC_Root, 'Number', 'Is Identical (a == b)', 600, 100, 'Is Hips XZ Mode')
    ConnectNodes(srcBoxRigCtrl, 'Root Mode', funcBoxIsHipsGroundedMode, 'a')
    SetInputValue(funcBoxIsHipsGroundedMode, 'b', 1)

    funcBoxIsReferenceGroundedMode = CreateFuncBox(RC_Root, 'Number', 'Is Identical (a == b)', 600, 200, 'Is Reference XZ Mode')
    ConnectNodes(srcBoxRigCtrl, 'Root Mode', funcBoxIsReferenceGroundedMode, 'a')
    SetInputValue(funcBoxIsReferenceGroundedMode, 'b', 2)

    funcBoxIsReferenceFreeMode = CreateFuncBox(RC_Root, 'Number', 'Is Identical (a == b)', 600, 300, 'Is Reference XYZ Mode')
    ConnectNodes(srcBoxRigCtrl, 'Root Mode', funcBoxIsReferenceFreeMode, 'a')
    SetInputValue(funcBoxIsReferenceFreeMode, 'b', 3)

    funcBoxIsFreeMode = CreateFuncBox(RC_Root, 'Number', 'Is Identical (a == b)', 600, 400, 'Is Marker XYZ Mode')
    ConnectNodes(srcBoxRigCtrl, 'Root Mode', funcBoxIsFreeMode, 'a')
    SetInputValue(funcBoxIsFreeMode, 'b', 4)


    # Actual IF nodes
    funcBox_IF_ZeroMode = CreateFuncBox(RC_Root, 'Vector', 'IF Cond Then A Else B', 1500, 0, 'If zero')
    ConnectNodes(funcBoxIsZeroMode, 'Result', funcBox_IF_ZeroMode, 'Cond')
    SetInputValue(funcBox_IF_ZeroMode, 'a', FBVector3d(0, 0, 0))

    funcBox_IF_HipsGroundedMode = CreateFuncBox(RC_Root, 'Vector', 'IF Cond Then A Else B', 1500, 100, 'If Hips XZ')
    ConnectNodes(funcBoxCombineHipsGroundedPos, 'Result', funcBox_IF_HipsGroundedMode, 'a') #a input from funcBoxCombineHipsGroundedPos
    ConnectNodes(funcBoxIsHipsGroundedMode, 'Result', funcBox_IF_HipsGroundedMode, 'Cond')
    ConnectNodes(funcBox_IF_HipsGroundedMode, 'Result', funcBox_IF_ZeroMode, 'b') #connect this to previous

    funcBox_IF_ReferenceGroundedMode = CreateFuncBox(RC_Root, 'Vector', 'IF Cond Then A Else B', 1500, 200, 'If reference XZ')
    ConnectNodes(funcBoxCombineReferenceGroundedPos, 'Result', funcBox_IF_ReferenceGroundedMode, 'a') #a input from funcBoxCombineReferenceGroundedPos
    ConnectNodes(funcBoxIsReferenceGroundedMode, 'Result', funcBox_IF_ReferenceGroundedMode, 'Cond')
    ConnectNodes(funcBox_IF_ReferenceGroundedMode, 'Result', funcBox_IF_HipsGroundedMode, 'b') #connect this to previous

    funcBox_IF_ReferenceFreeMode = CreateFuncBox(RC_Root, 'Vector', 'IF Cond Then A Else B', 1500, 300, 'If reference XYZ')
    ConnectNodes(srcBoxRigCtrl, 'Translation', funcBox_IF_ReferenceFreeMode, 'a') #a input from srcBoxRigCtrl
    ConnectNodes(funcBoxIsReferenceFreeMode, 'Result', funcBox_IF_ReferenceFreeMode, 'Cond')
    ConnectNodes(funcBox_IF_ReferenceFreeMode, 'Result', funcBox_IF_ReferenceGroundedMode, 'b') #connect this to previous

    # No need for final func box for free mode, just connect marker position to 'b' pin of previous node
    ConnectNodes(srcBoxCtrlMarker, 'Translation', funcBox_IF_ReferenceFreeMode, 'b') #a input from srcBoxCtrlMarker

    # marker should be visible only in "Free" mode
    dstBoxCtrlMarker = CreateDstBox(RC_Root, oRootCtrlMarker, True, 900, 400)
    ConnectNodes(funcBoxIsFreeMode, 'Result', dstBoxCtrlMarker, 'Visibility')

    #
    # Root rotation
    #
    # We set it only if 'Root Mode' > 1 ('Reference Grounded', 'Reference Free', 'Free')
    # 'Zero' and 'Hips Grounded' should stay on zero rotation
    #
    funcBoxIsRootRotatingMode = CreateFuncBox(RC_Root, 'Number', 'Is Greater (a > b)', 600, 500, 'Is Root Rotating Mode (a>1)')
    ConnectNodes(srcBoxRigCtrl, 'Root Mode', funcBoxIsRootRotatingMode, 'a')
    SetInputValue(funcBoxIsRootRotatingMode, 'b', 1)

    funcBox_IF_RotFromMarker = CreateFuncBox(RC_Root, 'Vector', 'IF Cond Then A Else B', 1500, 550, 'If rotation from marker') #else from reference
    ConnectNodes(funcBoxIsFreeMode, 'Result', funcBox_IF_RotFromMarker, 'Cond')
    ConnectNodes(srcBoxCtrlMarker, 'Rotation', funcBox_IF_RotFromMarker, 'a')
    ConnectNodes(srcBoxRigCtrl, 'Rotation', funcBox_IF_RotFromMarker, 'b')

    funcBox_IF_UseCustomRotation = CreateFuncBox(RC_Root, 'Vector', 'IF Cond Then A Else B', 1800, 400, 'If use custom rotation')
    ConnectNodes(funcBoxIsRootRotatingMode, 'Result', funcBox_IF_UseCustomRotation, 'Cond')
    ConnectNodes(funcBox_IF_RotFromMarker, 'Result', funcBox_IF_UseCustomRotation, 'a')
    SetInputValue(funcBox_IF_UseCustomRotation, 'b', FBVector3d(0, 0, 0))


    # Final controlled objects
    dstBoxRootBone = CreateDstBox(RC_Root, FBFindModelByLabelName('Root'), True, 2200, 0)
    ConnectNodes(funcBox_IF_ZeroMode, 'Result', dstBoxRootBone, 'Translation')
    ConnectNodes(funcBox_IF_UseCustomRotation, 'Result', dstBoxRootBone, 'Rotation')

    dstBoxRootCtrlArrow = CreateDstBox(RC_Root, oRootCtrlArrow, True, 2200, 150)
    ConnectNodes(funcBox_IF_ZeroMode, 'Result', dstBoxRootCtrlArrow, 'Translation')
    ConnectNodes(funcBox_IF_UseCustomRotation, 'Result', dstBoxRootCtrlArrow, 'Rotation')

    # Arrow constrained to root bone for visual reference
    srcBoxRootBone = CreateSrcBox(RC_Root, FBFindModelByLabelName('Root'), True, 1500, 900)
    dstBoxRootArrow = CreateDstBox(RC_Root, oRootArrow, True, 1800, 900)

    ConnectNodes(srcBoxRootBone, 'Rotation', dstBoxRootArrow, 'Rotation')
    ConnectNodes(srcBoxRootBone, 'Translation', dstBoxRootArrow, 'Translation')

    RC_Root.Active = True
    return RC_Root

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


def CreateCustomRigSetup():
    MakeSkinnedMeshesUnpickable()

    FBApplication().CurrentCharacter.GoToStancePose()

    rigCtrlModel = FBApplication().CurrentCharacter.GetCtrlRigModel(FBBodyNodeId.kFBReferenceNodeId)
    hipsCtrlModel = FBApplication().CurrentCharacter.GetCtrlRigModel(FBBodyNodeId.kFBHipsNodeId)

    AddEnumProperty(rigCtrlModel, 'Root Mode', True, ['Zero', 'Hips XZ', 'Reference XZ', 'Reference XYZ', 'Marker XYZ'])
    AddBoolProperty(rigCtrlModel, 'Root use forward', True, bDefaultValue=True)
    AddBoolProperty(rigCtrlModel, 'Root use side', True, bDefaultValue=False)

    oRootArrow = CreateCircleWithArrow('RootArrow', 50)
    oRootArrow.Pickable = False
    oRootCtrlArrow = CreateCompass('RootCtrlArrow', 60)
    oRootCtrlArrow.Pickable = False

    oRootCtrlMarker = CreateControlMarker('RootCtrlMarker', 10000.0)
    # Enable rotation DOF
    oRootCtrlMarker.RotationActive = True
    oRootCtrlMarker.RotationMinX = True
    oRootCtrlMarker.RotationMaxX = True
    oRootCtrlMarker.RotationMinZ = True
    oRootCtrlMarker.RotationMaxZ = True
    oRootCtrlMarker.RotationOrder = FBModelRotationOrder.kFBSphericXYZ

    oRootCtrlMarker.PropertyList.Find('Visibility').SetAnimated(True) # For relation constraint, marker visible when 'Root Mode' == 'Marker'

    RC_Root = CreateRootRelaionConstraint(rigCtrlModel, oRootCtrlMarker, hipsCtrlModel, oRootCtrlArrow, oRootArrow) # pylint: disable=unused-variable
    RC_IKBones = CreateIKBonesRelaionConstraint() # pylint: disable=unused-variable


    RC_Root.HardSelect()

    #Create reference properties
    refProp = RC_Root.PropertyList.Find('Active')
    rigCtrlModel.PropertyCreate('RC_Root Active', FBPropertyType.kFBPT_Reference, '', True, True, refProp)
