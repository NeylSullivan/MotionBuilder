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

def CreateArrow(name, color=FBColor(1.0, 1.0, 0.0)):
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
    curve = CreateCircle(name, radius, 20, color)

    for i in [0, 20]:
        pos = curve.PathKeyGet(i)
        pos *= 1.4
        curve.PathKeySet(i, pos, True)
    for i in [0, 1, 19, 20]:
        vKeyPos = curve.PathKeyGet(i)
        curve.PathKeySetLeftTangent(i, vKeyPos)
        curve.PathKeySetRightTangent(i, vKeyPos)

def CreateCircleWithArrow(name, radius):
    curve = FBModelPath3D(name)
    curve.Show = True
    curve.Visible = True
    #curve.Color = color

    points = [FBVector4d(0, 0, 1, 1),
              FBVector4d(0.309017, 0, 0.951057, 1),
              FBVector4d(0.587785, 0, 0.809017, 1),
              FBVector4d(0.809017, 0, 0.587785, 1),
              FBVector4d(0.951057, 0, 0.309017, 1),
              FBVector4d(1, 0, 0, 1),
              FBVector4d(0.951057, 0, -0.309017, 1),
              FBVector4d(0.809017, 0, -0.587785, 1),
              FBVector4d(0.587785, 0, -0.809017, 1),
              FBVector4d(0.2, 0, -1, 1),    #9
              FBVector4d(0.2, 0, 0.0, 1),   #10
              FBVector4d(0.6, 0, 0.0, 1),   #11
              FBVector4d(0, 0, 0.9, 1),     #12
              FBVector4d(-0.6, 0, 0.0, 1),  #13
              FBVector4d(-0.2, 0, 0.0, 1),  #14
              FBVector4d(-0.2, 0, -1, 1),   #15
              FBVector4d(-0.587785, 0, -0.809017, 1),
              FBVector4d(-0.809017, 0, -0.587785, 1),
              FBVector4d(-0.951057, 0, -0.309017, 1),
              FBVector4d(-1, 0, 0, 1),
              FBVector4d(-0.951057, 0, 0.309017, 1),
              FBVector4d(-0.809017, 0, 0.587785, 1),
              FBVector4d(-0.587785, 0, 0.809017, 1),
              FBVector4d(-0.309017, 0, 0.951057, 1),
              FBVector4d(0, 0, 1, 1)]

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

def CreateCustomRigSetup():
    model = FBApplication().CurrentCharacter.GetCtrlRigModel(FBBodyNodeId.kFBReferenceNodeId)
    #model.PropertyCreate( pName, pType, pDataType, pAnimatable, pIsUser, pReferenceSource )
    AddEnumProperty(model, 'Root Motion Mode', True, ['Zero', 'Hips Grounded', 'Reference Grounded', 'Reference Free', 'Free'])

    CreateCircleWithArrow('RootArow', 50)
    CreateCompass('RootCtrlArrow', 60)
