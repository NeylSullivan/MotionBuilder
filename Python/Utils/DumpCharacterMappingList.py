from pyfbsdk import *

import libHazardMoBuFunctions
reload(libHazardMoBuFunctions)
from libHazardMoBuFunctions import *

currentCharacter = FBApplication().CurrentCharacter

if currentCharacter:
   for nodeID in FBBodyNodeId.values.values():
        model = currentCharacter.GetModel(nodeID)
        if (model):
            rigModelName = currentCharacter.GetCtrlRigModel(nodeID).Name
            propertyName = rigModelName + "Link"
            property = currentCharacter.PropertyList.Find(propertyName)
            if property :
                # print str(int(nodeID))
                print "'%s' : '%s'," % (rigModelName, model.Name)
            

'''
    propList = currentCharacter.PropertyList
    for _property in propList:
        #print _property.GetProperty
        if _property.GetName() and _property.GetName().endswith("Link"):
            print (_property.GetPropertyTypeName() +" " + _property.GetName() + " " + _property.Data.Name)
        '''