from pyfbsdk import *

import libHazardMoBuFunctions
from libHazardMoBuFunctions import *
reload(libHazardMoBuFunctions)


object = GetLastSelectedModel()

if object:
    propList = object.PropertyList
    for _property in propList:
        if _property.GetName():
            print _property.GetPropertyTypeName() +" " + _property.GetName()
