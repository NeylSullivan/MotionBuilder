from pyfbsdk import *

for constraint in FBSystem().Scene.Constraints:
    if constraint.Is(FBConstraintRelation_TypeInfo()):# pylint: disable=undefined-variable
        for box in constraint.Boxes:
            if box.Selected:
                boxPos = constraint.GetBoxPosition(box) # Tupple, first is result of operation True/False
                print 'Constraint: "{}" Box: "{}" Position: ({}, {})'.format(constraint.Name, box.Name, boxPos[1], boxPos[2])

                boxIn = box.AnimationNodeInGet()
                if boxIn and boxIn.Nodes:
                    print 'In Properties'
                    for lNode in boxIn.Nodes:
                        print '\t' + lNode.Name

                boxOut = box.AnimationNodeOutGet()
                if boxOut and boxOut.Nodes:
                    print 'Out Properties'
                    for lNode in boxOut.Nodes:
                        print '\t' + lNode.Name
