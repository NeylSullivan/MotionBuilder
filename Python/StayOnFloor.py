from pyfbsdk import *
from pyfbsdk_additions import *
import libHazardMoBuFunctions
from libHazardMoBuFunctions import *
import libHazardUIExtension
from libHazardUIExtension import *
reload(libHazardMoBuFunctions)
reload(libHazardUIExtension)

class StayOnFloor(FBTool):
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

        self.enbStart.Min = FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()
        self.enbStart.Max = FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()-1

        self.enbStop.Min = FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()+1
        self.enbStop.Max = FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()

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
            self.enbFrame.Value = self.enbStart.Value + int((self.enbStop.Value - self.enbStart.Value) * 0.5)
        else:
            self.enbFrame.Value = FBSystem().LocalTime.GetFrame()

        _symModel, symModelName, symStart, symStop, symFrame = self.GetSymmetryData(selectedModel)


        self.lblSymModelName.Caption = symModelName
        self.enbSymStart.Value = symStart
        self.enbSymStop.Value = symStop
        self.enbSymFrame.Value = symFrame

        # Do it on end to optimize finding symmetry model
        self.lastSelectedModel = selectedModel



    def GetSymmetryData(self, pSelectedModel):
        symModel = None
        symModelName = ''
        symStart, symStop, symFrame = 0, 0, 0

        if not self.chbxSymmetry.State:
            return symModel, symModelName, symStart, symStop, symFrame

        if pSelectedModel:
            symModel = pSelectedModel

        if symModel:
            symModelName = symModel.Name

        bLoopOffset = self.chbxLoopOffset.State
        if not bLoopOffset:
            symStart = self.enbStart.Value
            symStop = self.enbStop.Value
            symFrame = self.enbFrame.Value
        else:
            takeLength = GetTimeSpan()
            takeHalfLength = takeLength / 2
            symStart = (self.enbStart.Value + takeHalfLength) % takeLength
            symStop = (self.enbStop.Value + takeHalfLength) % takeLength
            symFrame = (self.enbFrame.Value + takeHalfLength) % takeLength

        return symModel, symModelName, symStart, symStop, symFrame


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
                self.enbBlendTime = LayoutEditNumber(horBox, 1.0, 3, Precision=0.0, LargeStep=1.0, SmallStep=1.0)
                LayoutButton(horBox, 40, 'Guess', None)

            LayoutLabel(vert, 20, 'Reference Mode')

            with HorBoxLayout(vert, 20) as horBox:
                self.rbgReferenceMode = LayoutRadioButtonsGroup(horBox, 1.0, ('Average', 'Slider'), 0)

            with HorBoxLayout(vert, 20) as horBox:
                LayoutLabel(horBox, 60, 'Frame')
                self.enbFrame = LayoutEditNumber(horBox, 1.0, 0.0, ReadOnly=True, Precision=0.0, LargeStep=1.0, SmallStep=1.0)
                LayoutEmptySpace(horBox, 40)

            LayoutButton(vert, 40, 'Action', None, Look=FBButtonLook.kFBLookColorChange, State0Color=FBColor(0.5, 0, 0), State1Color=FBColor(0, 1, 0))

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
                self.enbSymFrame = LayoutEditNumber(horBox, 1.0, 0, Precision=0.0, LargeStep=1.0, SmallStep=1.0, ReadOnly=True,)
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
