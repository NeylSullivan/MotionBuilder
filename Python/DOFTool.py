# 
# Degrees of freedom tool
# 


from pyfbsdk import *
from pyfbsdk_additions import *

import libHazardMoBuFunctions
reload(libHazardMoBuFunctions)
from libHazardMoBuFunctions import *

btn_Pos_Active = FBButton()
cb_Pos_X = FBButton()
cb_Pos_Y = FBButton()
cb_Pos_Z = FBButton()

btn_Rot_Active = FBButton()
cb_Rot_X = FBButton()
cb_Rot_Y = FBButton()
cb_Rot_Z = FBButton()


def CheckBoxCallback_PosAxis(control, event):
    if tool.model:
        propNameMin = 'TranslationMin' + control.Caption
        tool.model.PropertyList.Find( propNameMin ).Data = control.State
        propNameMax = 'TranslationMax' + control.Caption
        tool.model.PropertyList.Find( propNameMax ).Data = control.State
    UpdateUI()
    
def CheckBoxCallback_RotAxis(control, event):
    if tool.model:
        propNameMin = 'RotationMin' + control.Caption
        tool.model.PropertyList.Find( propNameMin ).Data = control.State
        propNameMax = 'RotationMax' + control.Caption
        tool.model.PropertyList.Find( propNameMax ).Data = control.State
    UpdateUI()

def BtnCallback_PosActive(control, event):
    if tool.model:
        tool.model.PropertyList.Find( 'TranslationActive' ).Data = btn_Pos_Active.State
    UpdateUI()
    
def BtnCallback_RotActive(control, event):
    if tool.model:
        tool.model.PropertyList.Find( 'RotationActive' ).Data = btn_Rot_Active.State
    UpdateUI()
    
def EventContainerDragAndDrop(control, event):
    if event.State == FBDragAndDropState.kFBDragAndDropDrag:
        event.Accept()
    elif event.State == FBDragAndDropState.kFBDragAndDropDrop:
        model = event.Components[0]
        tool.container.Items.removeAll()
        tool.model = model
        
        if model:
            tool.container.Items.append(model.Name)
    
    UpdateUI()
    
def EventContainerDblClick(control, event):
    tool.container.Items.removeAll()
    tool.model = None
    UpdateUI()
    
def BtnCallback_GetSelected(control, event):
    model = GetLastSelectedModel()
    print model
    tool.container.Items.removeAll()
    tool.model = model
    
    if model:
        tool.container.Items.append(model.Name)
    
    UpdateUI()
    
def UpdateUI():
    bEditEnabled = False

    if tool.model:
       bEditEnabled = True
       btn_Pos_Active.State = tool.model.PropertyList.Find( 'TranslationActive' ).Data
       cb_Pos_X.State = tool.model.PropertyList.Find( 'TranslationMinX' ).Data and tool.model.PropertyList.Find( 'TranslationMaxX' ).Data
       cb_Pos_Y.State = tool.model.PropertyList.Find( 'TranslationMinY' ).Data and tool.model.PropertyList.Find( 'TranslationMaxY' ).Data
       cb_Pos_Z.State = tool.model.PropertyList.Find( 'TranslationMinZ' ).Data and tool.model.PropertyList.Find( 'TranslationMaxZ' ).Data
       
       btn_Rot_Active.State = tool.model.PropertyList.Find( 'RotationActive' ).Data
       cb_Rot_X.State = tool.model.PropertyList.Find( 'RotationMinX' ).Data and tool.model.PropertyList.Find( 'RotationMaxX' ).Data
       cb_Rot_Y.State = tool.model.PropertyList.Find( 'RotationMinY' ).Data and tool.model.PropertyList.Find( 'RotationMaxY' ).Data
       cb_Rot_Z.State = tool.model.PropertyList.Find( 'RotationMinZ' ).Data and tool.model.PropertyList.Find( 'RotationMaxZ' ).Data

    btn_Pos_Active.Enabled = bEditEnabled
    cb_Pos_X.Enabled = btn_Pos_Active.State and bEditEnabled
    cb_Pos_Y.Enabled = btn_Pos_Active.State and bEditEnabled
    cb_Pos_Z.Enabled = btn_Pos_Active.State and bEditEnabled
    btn_Rot_Active.Enabled = bEditEnabled
    cb_Rot_X.Enabled = btn_Rot_Active.State and bEditEnabled
    cb_Rot_Y.Enabled = btn_Rot_Active.State and bEditEnabled
    cb_Rot_Z.Enabled = btn_Rot_Active.State and bEditEnabled
       

def PopulateLayout(mainLyt):
    x = FBAddRegionParam(5,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(5,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(-5,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(-5,FBAttachType.kFBAttachBottom,"")
    main = FBVBoxLayout(FBAttachType.kFBAttachTop)
    mainLyt.AddRegion("main","main", x, y, w, h)
    mainLyt.SetControl("main",main)
    
    box = FBHBoxLayout(FBAttachType.kFBAttachLeft)
    
    tool.model = None
    tool.container = FBVisualContainer()
    tool.container.ItemHeight = 20
    tool.container.ItemWidth = 120
    tool.container.OnDragAndDrop.Add(EventContainerDragAndDrop)
    tool.container.OnDblClick.Add(EventContainerDblClick)
    box.Add(tool.container, 140)
    
    btn_GetSelected = FBButton()
    btn_GetSelected.Caption = "..."
    btn_GetSelected.Hint = "Get Selected Model"
    btn_GetSelected.Justify = FBTextJustify.kFBTextJustifyLeft
    box.Add(btn_GetSelected, 20)
    btn_GetSelected.OnClick.Add(BtnCallback_GetSelected)
    
    main.Add(box, 20)
    
    box = FBHBoxLayout(FBAttachType.kFBAttachLeft)
    
    
    btn_Pos_Active.Caption = "Translation"
    btn_Pos_Active.Justify = FBTextJustify.kFBTextJustifyLeft
    btn_Pos_Active.Style = FBButtonStyle.kFB2States
    btn_Pos_Active.Look = FBButtonLook.kFBLookColorChange
    box.Add(btn_Pos_Active, 60)
    btn_Pos_Active.OnClick.Add(BtnCallback_PosActive)
    
    
    cb_Pos_X.Caption = "X"
    cb_Pos_X.Style = FBButtonStyle.kFBCheckbox 
    cb_Pos_X.Justify = FBTextJustify.kFBTextJustifyLeft
    box.Add(cb_Pos_X, 30)
    cb_Pos_X.OnClick.Add(CheckBoxCallback_PosAxis)
    
    cb_Pos_Y.Caption = "Y"
    cb_Pos_Y.Style = FBButtonStyle.kFBCheckbox 
    cb_Pos_Y.Justify = FBTextJustify.kFBTextJustifyLeft
    box.Add(cb_Pos_Y, 30)
    cb_Pos_Y.OnClick.Add(CheckBoxCallback_PosAxis)
    
    cb_Pos_Z.Caption = "Z"
    cb_Pos_Z.Style = FBButtonStyle.kFBCheckbox 
    cb_Pos_Z.Justify = FBTextJustify.kFBTextJustifyLeft
    box.Add(cb_Pos_Z, 30)
    cb_Pos_Z.OnClick.Add(CheckBoxCallback_PosAxis)
    
    main.Add(box, 20)
    
    box = FBHBoxLayout(FBAttachType.kFBAttachLeft)
    
    btn_Rot_Active.Caption = "Rotation"
    btn_Rot_Active.Justify = FBTextJustify.kFBTextJustifyLeft
    btn_Rot_Active.Style = FBButtonStyle.kFB2States
    btn_Rot_Active.Look = FBButtonLook.kFBLookColorChange
    box.Add(btn_Rot_Active, 60)
    btn_Rot_Active.OnClick.Add(BtnCallback_RotActive)
    
    cb_Rot_X.Caption = "X"
    cb_Rot_X.Style = FBButtonStyle.kFBCheckbox 
    cb_Rot_X.Justify = FBTextJustify.kFBTextJustifyLeft
    box.Add(cb_Rot_X, 30)
    cb_Rot_X.OnClick.Add(CheckBoxCallback_RotAxis)
    
    cb_Rot_Y.Caption = "Y"
    cb_Rot_Y.Style = FBButtonStyle.kFBCheckbox 
    cb_Rot_Y.Justify = FBTextJustify.kFBTextJustifyLeft
    box.Add(cb_Rot_Y, 30)
    cb_Rot_Y.OnClick.Add(CheckBoxCallback_RotAxis)
    
    cb_Rot_Z.Caption = "Z"
    cb_Rot_Z.Style = FBButtonStyle.kFBCheckbox 
    cb_Rot_Z.Justify = FBTextJustify.kFBTextJustifyLeft
    box.Add(cb_Rot_Z, 30)
    cb_Rot_Z.OnClick.Add(CheckBoxCallback_RotAxis)
    
    main.Add(box, 20)


def CreateTool():
    global tool
    tool = FBCreateUniqueTool("DOF Tool")
    tool.StartSizeX = 200
    tool.StartSizeY = 120
    PopulateLayout(tool)
    ShowTool(tool)
    UpdateUI()
    
    # strictModeCheckBox.State = True
    

CreateTool()