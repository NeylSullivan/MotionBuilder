from pyfbsdk import *
from libHazardMoBuFunctions import *
import libHazardMoBuFunctions
reload(libHazardMoBuFunctions)


currentCharacter = FBApplication().CurrentCharacter

if currentCharacter:
    for nodeID in FBBodyNodeId.values.values():
        model = currentCharacter.GetModel(nodeID)
        if model:
            rigModelName = currentCharacter.GetCtrlRigModel(nodeID).Name
            propertyName = rigModelName + "Link"
            property = currentCharacter.PropertyList.Find(propertyName)
            if property:
                # print str(int(nodeID))
                print "'%s' : '%s'," % (rigModelName, model.Name)
