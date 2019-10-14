# Copyright 2009 Autodesk, Inc.  All rights reserved.
# Use of this software is subject to the terms of the Autodesk license agreement 
# provided at the time of installation or download, or which otherwise accompanies
# this software in either electronic or hard copy form.
#
# Topic: FBConstraintManager, FBPlug
#

from pyfbsdk import *

FBApplication().FileNew()

# We create new constraints with thr constaint manager.
lMgr = FBConstraintManager()
lScene = FBSystem().Scene
# We want to create one constraint of each types that exists.
for lIdx in range( lMgr.TypeGetCount() ):

    # We create the constraint, which will be automatically added to the scene.
    lCnst = lMgr.TypeCreateConstraint( lIdx )

    # User feedback, if the python console is up.
    print lMgr.TypeGetName( lIdx ) + " Constraint " + str(lIdx)
    
    # Cleanup.
    del( lCnst )

# Cleanup.
del( lMgr, lIdx, FBConstraintManager )
