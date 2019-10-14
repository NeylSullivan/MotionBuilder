from pyfbsdk import *

import libHazardMoBuFunctions
from libHazardMoBuFunctions import *
reload(libHazardMoBuFunctions)


curve = GetLastSelectedModel()

if curve:
    print curve.Name
    for i in range(curve.PathKeyGetCount()):
        vKeyPos = curve.PathKeyGet(i)
        print vKeyPos
