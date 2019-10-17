from pyfbsdk import *

rootCtrlArrow = FBFindModelByLabelName("RootCtrlArrow")
rootCtrlArrowTranslation = FBVector3d()
rootCtrlArrow.GetVector(rootCtrlArrowTranslation, FBModelTransformationType.kModelTranslation, True)


rigSettings = FBFindModelByLabelName("HazardCharacter_Ctrl:RigSettings")
rigSettings.PropertyList.Find('RootOffset').Data = rootCtrlArrowTranslation
