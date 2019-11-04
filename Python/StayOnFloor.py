from pyfbsdk import *
from pyfbsdk_additions import *
import libHazardMoBuFunctions
from libHazardMoBuFunctions import *
import libHazardUIExtension
from libHazardUIExtension import *
reload(libHazardMoBuFunctions)
reload(libHazardUIExtension)

class StayOnFloor(FBTool):
    def AddKey(self, pCurve, pTime, pValue):
        keyIdx = pCurve.KeyAdd(pTime, pValue)
        if keyIdx >= 0:
            pCurve.Keys[keyIdx].TangentMode = FBTangentMode.kFBTangentModeUser
            pCurve.Keys[keyIdx].LeftDerivative = 0.0
            pCurve.Keys[keyIdx].RightDerivative = 0.0


    def ProcessFCurve(self, pCurve, pReferenceTime, pStartTime, pStopTime, pBlendTime):
        referenceValue = pCurve.Evaluate(pReferenceTime)
        distance = pCurve.Evaluate(FBSystem().CurrentTake.LocalTimeSpan.GetStop()) - pCurve.Evaluate(FBSystem().CurrentTake.LocalTimeSpan.GetStart())
        print 'Curve: {}, keys: {}, referenceValue: {:0.2f}, distance: {:0.2f}'.format(pCurve.LongName, len(pCurve.Keys), referenceValue, distance)

        bPassOverLoop = pStartTime > pStopTime

        startTimeBlend = pStartTime - pBlendTime
        stopTimeBlend = pStopTime + pBlendTime

        if bPassOverLoop:
            pCurve.KeyDeleteByTimeRange(startTimeBlend, FBTime.Infinity, True)
            pCurve.KeyDeleteByTimeRange(FBTime.MinusInfinity, stopTimeBlend, True)
            startVal = referenceValue
            if pReferenceTime < pStartTime:
                startVal = referenceValue + distance
            self.AddKey(pCurve, FBSystem().CurrentTake.LocalTimeSpan.GetStop(), startVal)
            self.AddKey(pCurve, pStartTime, startVal)

            stopVal = referenceValue
            if pReferenceTime > pStopTime:
                stopVal = referenceValue - distance
            self.AddKey(pCurve, FBSystem().CurrentTake.LocalTimeSpan.GetStart(), stopVal)
            self.AddKey(pCurve, pStopTime, stopVal)

        else:
            pCurve.KeyDeleteByTimeRange(startTimeBlend, stopTimeBlend, True)
            self.AddKey(pCurve, pStartTime, referenceValue)
            self.AddKey(pCurve, pStopTime, referenceValue)

    def ProcessModel(self, pModel, pReferenceFrame, pStartFrame, pStopFrame, pBlendFramesNum):
        referenceTime = FBTime(0, 0, 0, int(pReferenceFrame))
        startTime = FBTime(0, 0, 0, int(pStartFrame))
        stopTime = FBTime(0, 0, 0, int(pStopFrame))
        blendTime = FBTime(0, 0, 0, int(pBlendFramesNum))

        animNode = pModel.Translation.GetAnimationNode()
        for node in animNode.Nodes:
            if node.FCurve:
                self.ProcessFCurve(node.FCurve, referenceTime, startTime, stopTime, blendTime)

    def ButtonActionEvent(self, _control, _event):
        selectedModel = self.GetSelectedModel()[0]
        if selectedModel is None:
            return

        lUndo = FBUndoManager()

        lUndo.TransactionBegin("StayOnFloor")
        lUndo.TransactionAddModelTRS(selectedModel)

        self.ProcessModel(selectedModel, self.enbReferenceFrame.Value, self.enbStart.Value, self.enbStop.Value, self.enbBlendFrames.Value)

        if self.chbxSymmetry.State:
            symModel, _symModelName, symStart, symStop, symReferenceFrame = self.GetSymmetryData(selectedModel)
            if symModel:
                lUndo.TransactionAddModelTRS(symModel)
                self.ProcessModel(symModel, symReferenceFrame, symStart, symStop, self.enbBlendFrames.Value)

        lUndo.TransactionEnd()


    def OnLayoutUpdate(self, _control, _event):
        self.UpdateUI()

    def GetSelectedModel(self):
        lModelList = FBModelList()
        FBGetSelectedModels(lModelList, None, True, True)

        selectedModel = None

        selectedCount = lModelList.GetCount()
        if selectedCount > 0:
            selectedModel = lModelList.GetModel(selectedCount-1)

        lModelList.Clear()

        return selectedModel, selectedCount

    def UpdateUI(self):
        self.enbStart.Min = self.enbStop.Min = FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()
        self.enbStart.Max = self.enbStop.Max = FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()

        selectedModel, selectedCount = self.GetSelectedModel()

        if selectedModel != self.lastSelectedModel:
            if selectedModel:
                if selectedCount > 1:
                    self.lblModelName.Caption = '{} +{}'.format(selectedModel.Name, selectedCount-1)
                else:
                    self.lblModelName.Caption = selectedModel.Name
            else:
                self.lblModelName.Caption = 'None'


        bIsAverageMode = self.rbgReferenceMode.buttons[0].State

        if bIsAverageMode:
            lTakeLength = GetTimeSpan()
            lFrameDistance = (self.enbStop.Value - self.enbStart.Value)
            if lFrameDistance < 0:
                lFrameDistance += lTakeLength
            self.enbReferenceFrame.Value = (self.enbStart.Value + int(lFrameDistance * 0.5)) % lTakeLength
        else:
            self.enbReferenceFrame.Value = FBSystem().LocalTime.GetFrame()


        self.btnAction.Enabled = selectedModel is not None

        _symModel, symModelName, symStart, symStop, symReferenceFrame = self.GetSymmetryData(selectedModel)

        self.lblSymModelName.Caption = symModelName
        self.enbSymStart.Value = symStart
        self.enbSymStop.Value = symStop
        self.enbSymReferenceFrame.Value = symReferenceFrame

        # Do it on end to optimize finding symmetry model
        self.lastSelectedModel = selectedModel

    def TryFindSymmetricalModel(self, pModel):
        if pModel is None:
            return None

        name = pModel.Name
        namespace = pModel.LongName.split(':')[:-1]
        symName = None
        if 'Left' in name:
            symName = name.replace('Left', 'Right')
        elif 'Right' in name:
            symName = name.replace('Right', 'Left')

        if symName is not None:
            if namespace:
                symName = "{}:{}".format(':'.join(namespace), symName)
            symModel = FBFindModelByLabelName(symName)

            if symModel:
                return symModel
        return None


    def GetSymmetryData(self, pSelectedModel):
        symModel = None
        symModelName = ''
        symStart, symStop, symReferenceFrame = 0, 0, 0

        if not self.chbxSymmetry.State:
            return symModel, symModelName, symStart, symStop, symReferenceFrame

        if pSelectedModel:
            symModel = self.TryFindSymmetricalModel(pSelectedModel)

        if symModel:
            symModelName = symModel.Name

        bLoopOffset = self.chbxLoopOffset.State
        if not bLoopOffset:
            symStart = self.enbStart.Value
            symStop = self.enbStop.Value
            symReferenceFrame = self.enbReferenceFrame.Value
        else:
            takeLength = GetTimeSpan()
            takeHalfLength = takeLength / 2
            symStart = (self.enbStart.Value + takeHalfLength) % takeLength
            symStop = (self.enbStop.Value + takeHalfLength) % takeLength
            symReferenceFrame = (self.enbReferenceFrame.Value + takeHalfLength) % takeLength

        return symModel, symModelName, symStart, symStop, symReferenceFrame


    def ButtonStartEvent(self, _control, _event):
        self.enbStart.Value = FBSystem().LocalTime.GetFrame()

    def ButtonStopEvent(self, _control, _event):
        self.enbStop.Value = FBSystem().LocalTime.GetFrame()

    def CheckboxSymmetryEvent(self, _control, _event):
        self.chbxLoopOffset.Enabled = self.chbxSymmetry.State
        self.symmetryDataLayout.Enabled = self.chbxSymmetry.State


    def BuildLayout(self):
        x = FBAddRegionParam(5, FBAttachType.kFBAttachLeft, "")
        y = FBAddRegionParam(5, FBAttachType.kFBAttachTop, "")
        w = FBAddRegionParam(-5, FBAttachType.kFBAttachRight, "")
        h = FBAddRegionParam(-5, FBAttachType.kFBAttachBottom, "")
        self.main = FBVBoxLayout(FBAttachType.kFBAttachTop)
        self.AddRegion("main", "main", x, y, w, h)
        self.SetControl("main", self.main)

        with BorderedVertBoxLayout(self, 220) as vert:
            with HorBoxLayout(vert, 20) as horBox:
                LayoutLabel(horBox, 60, 'Model')
                self.lblModelName = LayoutLabel(horBox, 1.0, 'None')

            with HorBoxLayout(vert, 20) as horBox:
                LayoutLabel(horBox, 60, 'Start')
                self.enbStart = LayoutEditNumber(horBox, 1.0, FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame(), Precision=0.0, LargeStep=1.0, SmallStep=1.0)
                LayoutButton(horBox, 40, 'Set', self.ButtonStartEvent)

            with HorBoxLayout(vert, 20) as horBox:
                LayoutLabel(horBox, 60, 'Stop')
                self.enbStop = LayoutEditNumber(horBox, 1.0, FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame(), Precision=0.0, LargeStep=1.0, SmallStep=1.0)
                LayoutButton(horBox, 40, 'Set', self.ButtonStopEvent)

            with HorBoxLayout(vert, 20) as horBox:
                LayoutLabel(horBox, 60, 'Blend Time')
                self.enbBlendFrames = LayoutEditNumber(horBox, 1.0, 3, Precision=0.0, LargeStep=1.0, SmallStep=1.0)
                self.enbBlendFrames.Value = max(3, int(GetTimeSpan() * 0.1))
                self.enbBlendFrames.Min = 1
                LayoutButton(horBox, 40, 'Guess', None)

            LayoutLabel(vert, 20, 'Reference Mode')

            with HorBoxLayout(vert, 20) as horBox:
                self.rbgReferenceMode = LayoutRadioButtonsGroup(horBox, 1.0, ('Average', 'Slider'), 0)

            with HorBoxLayout(vert, 20) as horBox:
                LayoutLabel(horBox, 60, 'Frame')
                self.enbReferenceFrame = LayoutEditNumber(horBox, 1.0, 0.0, ReadOnly=True, Precision=0.0, LargeStep=1.0, SmallStep=1.0)
                LayoutEmptySpace(horBox, 40)

            self.btnAction = LayoutButton(vert, 40, 'Action', self.ButtonActionEvent, State0Color=FBColor(0.5, 0, 0), State1Color=FBColor(0, 1, 0))

        self.chbxSymmetry = LayoutCheckbox(self.main, 20, 'Symmetry', True, self.CheckboxSymmetryEvent)
        self.chbxLoopOffset = LayoutCheckbox(self.main, 20, 'Loop offset', True)
        self.chbxLoopOffset.Enabled = self.chbxSymmetry.State

        with BorderedVertBoxLayout(self, 110, 'SymmetryData') as vert:
            self.symmetryDataLayout = vert
            self.symmetryDataLayout.Enabled = self.chbxSymmetry.State
            with HorBoxLayout(vert, 20) as horBox:
                LayoutLabel(horBox, 60, 'Model')
                self.lblSymModelName = LayoutLabel(horBox, 1.0, 'None')

            with HorBoxLayout(vert, 20) as horBox:
                LayoutLabel(horBox, 60, 'Start')
                self.enbSymStart = LayoutEditNumber(horBox, 1.0, 0, Precision=0.0, LargeStep=1.0, SmallStep=1.0, ReadOnly=True)
                LayoutEmptySpace(horBox, 40)

            with HorBoxLayout(vert, 20) as horBox:
                LayoutLabel(horBox, 60, 'Stop')
                self.enbSymStop = LayoutEditNumber(horBox, 1.0, 0, Precision=0.0, LargeStep=1.0, SmallStep=1.0, ReadOnly=True)
                LayoutEmptySpace(horBox, 40)

            with HorBoxLayout(vert, 20) as horBox:
                LayoutLabel(horBox, 60, 'Frame')
                self.enbSymReferenceFrame = LayoutEditNumber(horBox, 1.0, 0, Precision=0.0, LargeStep=1.0, SmallStep=1.0, ReadOnly=True,)
                LayoutEmptySpace(horBox, 40)


    def __init__(self, name):
        FBTool.__init__(self, name) # pylint: disable=no-member, non-parent-init-called
        self.lastSelectedModel = None
        lConfig = FBConfigFile("@Hazard.txt")
        self.animExportDir = lConfig.Get('AnimExport', 'AnimExportDir', None)
        self.BuildLayout()
        self.StartSizeX = 200
        self.StartSizeY = 440
        self.UpdateUI()

        self.Unregister()
        self.main.OnIdle.Add(self.OnLayoutUpdate)
        FBApplication().OnFileExit.Add(self.Unregister)

    def Unregister(self, _control=None, _event=None):
        print 'Unregister'
        self.main.OnIdle.Remove(self.OnLayoutUpdate)
        FBApplication().OnFileExit.Remove(self.Unregister)


gToolName = "Stay On Floor"

gDEVELOPMENT = True # Development? - need to recreate each time!

if gDEVELOPMENT:
    FBDestroyToolByName(gToolName)

if gToolName in FBToolList:
    tool = FBToolList[gToolName]
    ShowTool(tool)
else:
    tool = StayOnFloor(gToolName)
    FBAddTool(tool)
    if gDEVELOPMENT:
        ShowTool(tool)
