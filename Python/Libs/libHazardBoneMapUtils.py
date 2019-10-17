def __AddLimbs(pBoneMap):
    templateMap = {'UpLeg' : 'UpLeg',
                   'Leg' : 'Leg',
                   'Foot' : 'Foot',
                   'ToeBase' : 'Toe',
                   'Shoulder' : 'Clavicle',
                   'Arm' : 'Arm',
                   'ForeArm' : 'ForeArm',
                   'Hand' : 'Hand',}

    for slotSide, jointSide in {'Right' : '_R', 'Left' : '_L'}.iteritems():
        for slot, joint in templateMap.iteritems():
            pBoneMap[slotSide + slot] = joint  + jointSide

def __AddHandFingers(pBoneMap):
    templateMap = {'HandThumb' : 'HandThumb',
                   'HandIndex' : 'HandIndex',
                   'HandMiddle' : 'HandMid',
                   'HandRing' : 'HandRing',
                   'HandPinky' : 'HandPinky'}

    for slotSide, jointSide in {'Right' : '_R', 'Left' : '_L'}.iteritems():
        for slot, joint in templateMap.iteritems():
            for slotIndex, jointIndex in {'1' : '1', '2' : '2', '3' : '3'}.iteritems():
                pBoneMap[slotSide+slot+slotIndex] = joint + jointIndex + jointSide
            # Special case for carpal bones
            pBoneMap[slotSide + 'In' + slot] = joint + '0' + jointSide
            # Special case for END bones
            pBoneMap[slotSide + slot + '4'] = joint + '3' + jointSide + '_END'

def __AddToeFingers(pBoneMap):
    templateMap = {'ExtraFinger' : 'ToeBig',
                   'Index' : 'ToeIndex',
                   'Middle' : 'ToeMid',
                   'Ring' : 'ToeRing',
                   'Pinky' : 'ToePinky'}

    for slotSide, jointSide in {'RightFoot' : '_R', 'LeftFoot' : '_L'}.iteritems():
        for slot, joint in templateMap.iteritems():
            for slotIndex, jointIndex in {'1' : '1', '2' : '2'}.iteritems():
                pBoneMap[slotSide+slot+slotIndex] = joint + jointIndex + jointSide

            # Special case for END bones
            pBoneMap[slotSide + slot + '3'] = joint + '2' + jointSide + '_END'


def GetBoneMap():
    boneMap = {'Reference' : 'Root',
               'Hips' : 'Hips',
               'Spine' : 'Spine_1',
               'Spine1' : 'Spine_2',
               'Spine2' : 'Spine_3',
               'Spine3' : 'Spine_4',
               'Neck' : 'Neck_1',
               'Neck1' : 'Neck_2',
               'Head' : 'Head',
               'LeafLeftUpLegRoll1' : 'UpLeg_L_TWIST',
               'LeafRightUpLegRoll1' : 'UpLeg_R_TWIST',
               'LeafLeftArmRoll1' : 'Arm_L_TWIST',
               'LeafLeftForeArmRoll1' : 'ForeArm_L_TWIST',
               'LeafRightArmRoll1' : 'Arm_R_TWIST',
               'LeafRightForeArmRoll1' : 'ForeArm_R_TWIST'}
    __AddLimbs(boneMap)
    __AddHandFingers(boneMap)
    __AddToeFingers(boneMap)
    return boneMap
