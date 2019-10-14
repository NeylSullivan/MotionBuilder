from pyfbsdk import *

rigSettings = FBFindModelByLabelName("HazardCharacter_Ctrl:RigSettings")
rigSettings.PropertyList.Find('RootOffset').Data = FBVector3d()