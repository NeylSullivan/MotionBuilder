import os
from pyfbsdk import *
from pyfbsdk_additions import *
import decimal
from libHazardUIExtension import *
from libHazardMoBuFunctions import *
import libHazardMoBuFunctions
reload(libHazardMoBuFunctions)

enbBlendPercent = FBEditNumber()
radbtnKeepTime = FBButton()
radbtnKeepSpeed = FBButton()
enbRescaleTime = FBEditNumber()
chbxDisableCnstrWhenPlot = FBButton()



# Simple buttom to offset looped take to the opposide side of the loop
def BtnCallback_GotoLoop(_control, _event):
    oldFrame = FBSystem().LocalTime.GetFrame(FBTimeMode.kFBTimeModeDefault)
    takeLength = GetTimeSpan()
    takeHalfLength = takeLength / 2
    newFrame = (oldFrame + takeHalfLength) % takeLength
    FBPlayerControl().Goto(FBTime(0, 0, 0, newFrame, 0))

def BtnCallback_SetTimerangeFromKeys(_control, _event):
    if FBApplication().CurrentCharacter is None:
        FBMessageBox("Error", '\nNone character to set timerange from keys', "OK")
        return

    iCurrentStartFrame = FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()
    iCurrentEndFrame = FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()

    nodeLimitsTupple = (None, None)

    for lEffectorId in FBEffectorId.values.values():
        effectorModel = FBApplication().CurrentCharacter.GetEffectorModel(lEffectorId)
        if effectorModel:
            lNodes = effectorModel.AnimationNode.Nodes
            for node in lNodes:
                nodeLimitsTupple = libHazardMoBuFunctions.FindLimits(node, nodeLimitsTupple[0], nodeLimitsTupple[1])

    iNewStartFrame = nodeLimitsTupple[0].GetFrame()
    iNewEndFrame = nodeLimitsTupple[1].GetFrame()

    message = '\n\nCurrent timerange: ({}, {}).\nCalculated time range: ({}, {})\n\nApply modifications?'.format(iCurrentStartFrame, iCurrentEndFrame, iNewStartFrame, iNewEndFrame)

    result = FBMessageBox("Set Timerange From Keys", message, "Apply", "Cancel")

    if result == 1:
        SetTimeSpan(iNewStartFrame, iNewEndFrame)
        SceneRefresh()


def BtnCallback_MakeLoopable(_control, _event):
    CleanStoryTrack()
    FBStory().Mute = False

    blendFraction = float(enbBlendPercent.Value / 100.0)
    iTakeFramesNum = GetTimeSpan()
    iExtraFramesNum = int(iTakeFramesNum * blendFraction)
    bKeepTime = radbtnKeepTime.State == FBButtonState.kFBButtonState1
    fNewSpeed = 1.0

    if bKeepTime: # Keep time - adjust speed
        fNewSpeed = 1.0 / (1.0 + blendFraction)

    FBSystem().CurrentTake.MergeLayers(FBAnimationLayerMergeOptions.kFBAnimLayerMerge_AllLayers_CompleteScene, True, FBMergeLayerMode.kFBMergeLayerModeAutomatic)
    lTrack = FBStoryTrack(FBStoryTrackType.kFBStoryTrackCharacter, FBStory().RootFolder)
    lTrack.Label = 'MakeLoopable'
    lTrack.Details.append(FBApplication().CurrentCharacter)
    lTrack.CopyTakeIntoTrack(FBSystem().CurrentTake.LocalTimeSpan, FBSystem().CurrentTake)

    clip = lTrack.Clips[0]

    clip.Name = 'Base'
    if bKeepTime:
        clip.Stop = FBTime(0, 0, 0, iTakeFramesNum + iExtraFramesNum)
    clip.Speed = fNewSpeed

    iClipOffset = (clip.Stop.GetFrame() - clip.Start.GetFrame()) - iExtraFramesNum
    if bKeepTime:
        iClipOffset = iTakeFramesNum
    print iClipOffset

    preClip = FBStoryClip(clip.Clone(), lTrack, FBTime(0, 0, 0, clip.Start.GetFrame() - iClipOffset))
    preClip.Name = 'Pre'

    postClip = FBStoryClip(clip.Clone(), lTrack, FBTime(0, 0, 0, clip.Start.GetFrame() + iClipOffset))
    postClip.Name = 'Post'

    if not bKeepTime:
        SetTimeSpan(0, iClipOffset)##Set Our Time Span To Match Our Desired Time Line Length


    #clip.Speed = adjSpeed##Set Our Clips New Speed To Be Our Adjustment Speed

def BtnCallback_RetimeAnim(_control, _event):
    CleanStoryTrack()
    FBStory().Mute = False

    length = int(enbRescaleTime.Value)

    FBSystem().CurrentTake.MergeLayers(FBAnimationLayerMergeOptions.kFBAnimLayerMerge_AllLayers_CompleteScene, True, FBMergeLayerMode.kFBMergeLayerModeAutomatic)
    lTrack = FBStoryTrack(FBStoryTrackType.kFBStoryTrackCharacter, FBStory().RootFolder)
    lTrack.Label = FBSystem().CurrentTake.Name + "_RETIME"
    lTrack.Details.append(FBApplication().CurrentCharacter)
    lTrack.CopyTakeIntoTrack(FBSystem().CurrentTake.LocalTimeSpan, FBSystem().CurrentTake)
    for clip in lTrack.Clips:
        oClipStopFrame = GetTimeSpan()##Get Clips New End Frame
        adjSpeed = round((decimal.Decimal(oClipStopFrame) / decimal.Decimal(length)), 4)##Create Our Adjustment Speed (Clips Current Legnth / Our Desired Length)
        clip.Stop = FBTime(0, 0, 0, (length+1))##Set StopFrame So Anim Does Not Get Cut Off
        clip.Speed = adjSpeed##Set Our Clips New Speed To Be Our Adjustment Speed
        SetTimeSpan(0, length)##Set Our Time Span To Match Our Desired Time Line Length
    FBStory().Mute = False

def BtnCallback_PlotStory(_control, _event):
    constraintsList = []
    if chbxDisableCnstrWhenPlot.State:
        for node in FBSystem().Scene.Constraints:
            if node.Name.startswith('MACRO_'):
                continue
            elif node.Active and isinstance(node, FBConstraintRelation):
                constraintsList.append(node)

    for node in constraintsList:
        print 'Disabling ' + node.Name
        node.Active = False


    PlotStoryClip()
    FBStory().Mute = True

    for node in constraintsList:
        print 'Enabling ' + node.Name
        node.Active = True

def CreateMirrorSetup():
    CleanStoryTrack()

    oClipStopFrame = GetTimeSpan()

    FBSystem().CurrentTake.MergeLayers(FBAnimationLayerMergeOptions.kFBAnimLayerMerge_AllLayers_CompleteScene, True, FBMergeLayerMode.kFBMergeLayerModeAutomatic)
    lTrackOrig = FBStoryTrack(FBStoryTrackType.kFBStoryTrackCharacter)
    lTrackOrig.Label = "ORIGINAL"
    lTrackOrig.Details.append(FBApplication().CurrentCharacter)
    lTrackOrig.CopyTakeIntoTrack(FBSystem().CurrentTake.LocalTimeSpan, FBSystem().CurrentTake)

    clip = lTrackOrig.Clips[0]
    clip.Stop = FBTime(0, 0, 0, oClipStopFrame)
    clip.Speed = 1.0

    lSubTrackMod = lTrackOrig.CreateSubTrack(FBStoryTrackType.kFBStoryTrackCharacter, FBStoryTrackRefMode.kFBStoryTrackOverride)
    lSubTrackMod.Label = "MIRROR_OFFSET"
    lSubTrackMod.Weight = 50.0
    lSubTrackMod.OffsetEnable = True #Important for root motion fixing

    sModClipPath = os.path.normpath(os.path.join(os.path.expanduser("~/Desktop"), FBSystem().CurrentTake.Name + '_TEMP.fbx'))
    print sModClipPath
    try:
        os.remove(sModClipPath)
    except BaseException:
        print("Error while deleting file ", sModClipPath)

    print lTrackOrig.Clips[0].ExportToFile(sModClipPath)

    iModClipStart = -1 * (oClipStopFrame/2)
    modClip = FBStoryClip(sModClipPath, lSubTrackMod, FBTime(0, 0, 0, iModClipStart))
    modClip.Stop = FBTime(0, 0, 0, iModClipStart + 2 * oClipStopFrame)
    modClip.MirrorAnimation = True
    modClip.MirrorPlane = FBStoryClipMirrorPlane.kFBStoryClipMirrorPlaneZY

    # Fix RootMotionOffset
    modClip.AutoLoop = True
    loopTranslation = modClip.LoopTranslation #auto calculated value
    modClip.Translation = loopTranslation / -2.0

    FBStory().Mute = False

    return lTrackOrig


def BtnCallback_ResimLoop(_control, _event):
    CreateMirrorSetup()

def BtnCallback_MirrorArmLeftRight(_control, _event):
    lTrackOrig = CreateMirrorSetup()

    srcClip = lTrackOrig.SubTracks[0].Clips[0]

    lSubTrackLeftArm = lTrackOrig.CreateSubTrack(FBStoryTrackType.kFBStoryTrackCharacter, FBStoryTrackRefMode.kFBStoryTrackOverride)
    lSubTrackLeftArm.Label = "LEFT ARM"
    lSubTrackLeftArm.Weight = 100.0
    lSubTrackLeftArm.EnableBodyPart(FBStoryTrackBodyPart.kFBStoryTrackBodyPartAll, False)
    lSubTrackLeftArm.EnableBodyPart(FBStoryTrackBodyPart.kFBStoryTrackBodyPartLeftArm, True)

    leftArmClip = FBStoryClip(srcClip.Clone(), lSubTrackLeftArm, srcClip.Start)    #Left arm uses original clip
    leftArmClip.MarkIn = srcClip.Start ##
    leftArmClip.Stop = srcClip.Stop
    leftArmClip.MirrorAnimation = False

    lSubTrackRightArm = lTrackOrig.CreateSubTrack(FBStoryTrackType.kFBStoryTrackCharacter, FBStoryTrackRefMode.kFBStoryTrackOverride)
    lSubTrackRightArm.Label = "RIGHT ARM"
    lSubTrackRightArm.Weight = 100.0
    lSubTrackRightArm.EnableBodyPart(FBStoryTrackBodyPart.kFBStoryTrackBodyPartAll, False)
    lSubTrackRightArm.EnableBodyPart(FBStoryTrackBodyPart.kFBStoryTrackBodyPartRightArm, True)

    rightArmClip = FBStoryClip(srcClip.Clone(), lSubTrackRightArm, srcClip.Start) #Right arm uses mirrored
    rightArmClip.Stop = srcClip.Stop
    rightArmClip.MirrorAnimation = True
    rightArmClip.MirrorPlane = FBStoryClipMirrorPlane.kFBStoryClipMirrorPlaneZY


def BtnCallback_MirrorArmRightLeft(_control, _event):
    lTrackOrig = CreateMirrorSetup()

    srcClip = lTrackOrig.SubTracks[0].Clips[0]

    lSubTrackLeftArm = lTrackOrig.CreateSubTrack(FBStoryTrackType.kFBStoryTrackCharacter, FBStoryTrackRefMode.kFBStoryTrackOverride)
    lSubTrackLeftArm.Label = "LEFT ARM"
    lSubTrackLeftArm.Weight = 100.0
    lSubTrackLeftArm.EnableBodyPart(FBStoryTrackBodyPart.kFBStoryTrackBodyPartAll, False)
    lSubTrackLeftArm.EnableBodyPart(FBStoryTrackBodyPart.kFBStoryTrackBodyPartLeftArm, True)

    leftArmClip = FBStoryClip(srcClip.Clone(), lSubTrackLeftArm, srcClip.Start)    #Left arm uses mirrored clip
    leftArmClip.Stop = srcClip.Stop
    leftArmClip.MirrorAnimation = True

    lSubTrackRightArm = lTrackOrig.CreateSubTrack(FBStoryTrackType.kFBStoryTrackCharacter, FBStoryTrackRefMode.kFBStoryTrackOverride)
    lSubTrackRightArm.Label = "RIGHT ARM"
    lSubTrackRightArm.Weight = 100.0
    lSubTrackRightArm.EnableBodyPart(FBStoryTrackBodyPart.kFBStoryTrackBodyPartAll, False)
    lSubTrackRightArm.EnableBodyPart(FBStoryTrackBodyPart.kFBStoryTrackBodyPartRightArm, True)

    rightArmClip = FBStoryClip(srcClip.Clone(), lSubTrackRightArm, srcClip.Start) #Right arm uses mirrored
    rightArmClip.MarkIn = srcClip.Start ##
    rightArmClip.Stop = srcClip.Stop
    rightArmClip.MirrorAnimation = False



def PopulateLayout(mainLyt):
    x = FBAddRegionParam(5, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(5, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(-5, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(-5, FBAttachType.kFBAttachBottom, "")
    main = FBVBoxLayout(FBAttachType.kFBAttachTop)
    mainLyt.AddRegion("main", "main", x, y, w, h)
    mainLyt.SetControl("main", main)

    with BorderedVertBoxLayout(mainLyt, pHeight=80) as vertBox:
        b = FBButton()
        b.Caption = ">> GoTo Loop >>"
        b.OnClick.Add(BtnCallback_GotoLoop)
        vertBox.Add(b, 40)

        b = FBButton()
        b.Caption = "Set Timerange from Keys"
        b.OnClick.Add(BtnCallback_SetTimerangeFromKeys)
        vertBox.Add(b, 20)

    # Start loop ui region
    with BorderedVertBoxLayout(mainLyt, pHeight=100) as vertBox:
        b = FBButton()
        b.Caption = "Make Loopable"
        b.OnClick.Add(BtnCallback_MakeLoopable)
        vertBox.AddRelative(b)

        with HorBoxLayout(vertBox, pHeight=20) as horBox:
            lbl = FBLabel()
            lbl.Visible = True
            lbl.ReadOnly = False
            lbl.Enabled = True
            lbl.Hint = ""
            lbl.Caption = "Blend percent"
            lbl.Style = FBTextStyle.kFBTextStyleNone
            lbl.Justify = FBTextJustify.kFBTextJustifyLeft
            lbl.WordWrap = True
            horBox.Add(lbl, 90)

            #enbBlendPercent = FBEditNumber()
            enbBlendPercent.Value = 10.0
            enbBlendPercent.Min = 1.0
            enbBlendPercent.Max = 75.0 # Awoid 100% blending
            enbBlendPercent.Precision = 0.0
            enbBlendPercent.LargeStep = 1.0
            enbBlendPercent.SmallStep = 1.0
            horBox.AddRelative(enbBlendPercent)


        with HorBoxLayout(vertBox) as horBox:
            group = FBButtonGroup()

            radbtnKeepTime.Caption = 'Keep Time'
            radbtnKeepTime.Style = FBButtonStyle.kFBRadioButton
            radbtnKeepTime.State = FBButtonState.kFBButtonState1
            group.Add(radbtnKeepTime)
            horBox.AddRelative(radbtnKeepTime)

            radbtnKeepSpeed.Caption = 'Keep Speed'
            radbtnKeepSpeed.Style = FBButtonStyle.kFBRadioButton
            radbtnKeepSpeed.State = FBButtonState.kFBButtonState0
            group.Add(radbtnKeepSpeed)
            horBox.AddRelative(radbtnKeepSpeed)

        # End loop ui region

    # Start retime ui region
    with BorderedVertBoxLayout(mainLyt) as vertBox:
        b = FBButton()
        b.Caption = "Retime Animation"
        b.OnClick.Add(BtnCallback_RetimeAnim)
        vertBox.AddRelative(b)

        with HorBoxLayout(vertBox, pHeight=20) as horBox:
            lbl = FBLabel()
            lbl.Visible = True
            lbl.ReadOnly = False
            lbl.Enabled = True
            lbl.Hint = ""
            lbl.Caption = "New frames num"
            lbl.Style = FBTextStyle.kFBTextStyleNone
            lbl.Justify = FBTextJustify.kFBTextJustifyLeft
            lbl.WordWrap = True
            horBox.Add(lbl, 90)

            #enbRescaleTime = FBEditNumber()
            enbRescaleTime.Value = 30.0
            enbRescaleTime.Min = 1.0
            enbRescaleTime.Precision = 0.0
            enbRescaleTime.LargeStep = 1.0
            enbRescaleTime.SmallStep = 0.1
            horBox.AddRelative(enbRescaleTime, 1.0)
    # End retime ui region

    # Start resim ui region
    with BorderedVertBoxLayout(mainLyt) as vertBox:
        with HorBoxLayout(vertBox) as horBox:
            b = FBButton()
            b.Caption = "Mirror Arm R->L"
            b.OnClick.Add(BtnCallback_MirrorArmRightLeft)
            horBox.AddRelative(b)

            b = FBButton()
            b.Caption = "Mirror Arm L->R"
            b.OnClick.Add(BtnCallback_MirrorArmLeftRight)
            horBox.AddRelative(b)

        b = FBButton()
        b.Caption = "Resim Loop"
        b.OnClick.Add(BtnCallback_ResimLoop)
        vertBox.Add(b, 25)
    # End resim ui region



    b = FBButton()
    b.Caption = "Plot Story"
    b.OnClick.Add(BtnCallback_PlotStory)
    b.Look = FBButtonLook.kFBLookColorChange
    b.SetStateColor(FBButtonState.kFBButtonState0, FBColor(0.5, 0.0, 0.0))
    b.SetStateColor(FBButtonState.kFBButtonState1, FBColor(0.0, 1.0, 0.0))
    main.Add(b, 40, space=15)

    chbxDisableCnstrWhenPlot.Caption = "Disable constraint during plotting"
    chbxDisableCnstrWhenPlot.Hint = "Disable enable not MACRO relation constraints during plotting to prevent animation glitches"
    chbxDisableCnstrWhenPlot.Style = FBButtonStyle.kFBCheckbox
    chbxDisableCnstrWhenPlot.Justify = FBTextJustify.kFBTextJustifyLeft
    chbxDisableCnstrWhenPlot.State = True
    main.Add(chbxDisableCnstrWhenPlot, 40)



def CreateTool():
    # Tool creation will serve as the hub for all other controls
    t = FBCreateUniqueTool("Process Anim Tool")
    t.StartSizeX = 210
    t.StartSizeY = 500
    PopulateLayout(t)
    ShowTool(t)

CreateTool()
