# 
# Degrees of freedom tool
# 


from pyfbsdk import *
from pyfbsdk_additions import *

import libHazardMoBuFunctions
reload(libHazardMoBuFunctions)
from libHazardMoBuFunctions import *

btn_Pos_Active = FBButton()
cb_Pos_MinX = FBButton()
cb_Pos_MaxX = FBButton()
cb_Pos_MinY = FBButton()
cb_Pos_MaxY = FBButton()
cb_Pos_MinZ = FBButton()
cb_Pos_MaxZ = FBButton()

btn_Rot_Active = FBButton()
cb_Rot_MinX = FBButton()
cb_Rot_MaxX = FBButton()
cb_Rot_MinY = FBButton()
cb_Rot_MaxY = FBButton()
cb_Rot_MinZ = FBButton()
cb_Rot_MaxZ = FBButton()


def CheckBoxCallback_PosAxis(control, event):
    if tool.model:
        propNameMin = 'Translation' + control.Caption
        tool.model.PropertyList.Find( propNameMin ).Data = control.State
        
        if control.Caption == 'MinX':
            Min = tool.model.PropertyList.Find( 'TranslationMin' ).Data
            Min[0] = tool.model.Translation[0]
            tool.model.PropertyList.Find( 'TranslationMin' ).Data = Min
        elif control.Caption == 'MaxX':
            Max = tool.model.PropertyList.Find( 'TranslationMax' ).Data
            Max[0] = tool.model.Translation[0]
            tool.model.PropertyList.Find( 'TranslationMax' ).Data = Max
        elif control.Caption == 'MinY':
            Min = tool.model.PropertyList.Find( 'TranslationMin' ).Data
            Min[1] = tool.model.Translation[1]
            tool.model.PropertyList.Find( 'TranslationMin' ).Data = Min
        elif control.Caption == 'MaxY':
            Max = tool.model.PropertyList.Find( 'TranslationMax' ).Data
            Max[1] = tool.model.Translation[1]
            tool.model.PropertyList.Find( 'TranslationMax' ).Data = Max
        elif control.Caption == 'MinZ':
            Min = tool.model.PropertyList.Find( 'TranslationMin' ).Data
            Min[2] = tool.model.Translation[2]
            tool.model.PropertyList.Find( 'TranslationMin' ).Data = Min
        elif control.Caption == 'MaxZ':
            Max = tool.model.PropertyList.Find( 'TranslationMax' ).Data
            Max[2] = tool.model.Translation[2]
            tool.model.PropertyList.Find( 'TranslationMax' ).Data = Max
    UpdateUI()
    
def CheckBoxCallback_RotAxis(control, event):
    if tool.model:
        propNameMin = 'Rotation' + control.Caption
        tool.model.PropertyList.Find( propNameMin ).Data = control.State
        
        if control.Caption == 'MinX':
            Min = tool.model.PropertyList.Find( 'RotationMin' ).Data
            Min[0] = tool.model.Rotation[0]
            tool.model.PropertyList.Find( 'RotationMin' ).Data = Min
        elif control.Caption == 'MaxX':
            Max = tool.model.PropertyList.Find( 'RotationMax' ).Data
            Max[0] = tool.model.Rotation[0]
            tool.model.PropertyList.Find( 'RotationMax' ).Data = Max
        elif control.Caption == 'MinY':
            Min = tool.model.PropertyList.Find( 'RotationMin' ).Data
            Min[1] = tool.model.Rotation[1]
            tool.model.PropertyList.Find( 'RotationMin' ).Data = Min
        elif control.Caption == 'MaxY':
            Max = tool.model.PropertyList.Find( 'RotationMax' ).Data
            Max[1] = tool.model.Rotation[1]
            tool.model.PropertyList.Find( 'RotationMax' ).Data = Max
        elif control.Caption == 'MinZ':
            Min = tool.model.PropertyList.Find( 'RotationMin' ).Data
            Min[2] = tool.model.Rotation[2]
            tool.model.PropertyList.Find( 'RotationMin' ).Data = Min
        elif control.Caption == 'MaxZ':
            Max = tool.model.PropertyList.Find( 'RotationMax' ).Data
            Max[2] = tool.model.Rotation[2]
            tool.model.PropertyList.Find( 'RotationMax' ).Data = Max
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
       
       cb_Pos_MinX.State = tool.model.PropertyList.Find( 'TranslationMinX' ).Data
       cb_Pos_MaxX.State = tool.model.PropertyList.Find( 'TranslationMaxX' ).Data
       cb_Pos_MinY.State = tool.model.PropertyList.Find( 'TranslationMinY' ).Data
       cb_Pos_MaxY.State = tool.model.PropertyList.Find( 'TranslationMaxY' ).Data
       cb_Pos_MinZ.State = tool.model.PropertyList.Find( 'TranslationMinZ' ).Data
       cb_Pos_MaxZ.State = tool.model.PropertyList.Find( 'TranslationMaxZ' ).Data
       
       btn_Rot_Active.State = tool.model.PropertyList.Find( 'RotationActive' ).Data
       
       cb_Rot_MinX.State = tool.model.PropertyList.Find( 'RotationMinX' ).Data
       cb_Rot_MaxX.State = tool.model.PropertyList.Find( 'RotationMaxX' ).Data
       cb_Rot_MinY.State = tool.model.PropertyList.Find( 'RotationMinY' ).Data
       cb_Rot_MaxY.State = tool.model.PropertyList.Find( 'RotationMaxY' ).Data
       cb_Rot_MinZ.State = tool.model.PropertyList.Find( 'RotationMinZ' ).Data
       cb_Rot_MaxZ.State = tool.model.PropertyList.Find( 'RotationMaxZ' ).Data
       

    btn_Pos_Active.Enabled = bEditEnabled
    cb_Pos_MinX.Enabled = btn_Pos_Active.State and bEditEnabled
    cb_Pos_MaxX.Enabled = btn_Pos_Active.State and bEditEnabled
    cb_Pos_MinY.Enabled = btn_Pos_Active.State and bEditEnabled
    cb_Pos_MaxY.Enabled = btn_Pos_Active.State and bEditEnabled
    cb_Pos_MinZ.Enabled = btn_Pos_Active.State and bEditEnabled
    cb_Pos_MaxZ.Enabled = btn_Pos_Active.State and bEditEnabled
    
    btn_Rot_Active.Enabled = bEditEnabled
    cb_Rot_MinX.Enabled = btn_Rot_Active.State and bEditEnabled
    cb_Rot_MaxX.Enabled = btn_Rot_Active.State and bEditEnabled
    cb_Rot_MinY.Enabled = btn_Rot_Active.State and bEditEnabled
    cb_Rot_MaxY.Enabled = btn_Rot_Active.State and bEditEnabled
    cb_Rot_MinZ.Enabled = btn_Rot_Active.State and bEditEnabled
    cb_Rot_MaxZ.Enabled = btn_Rot_Active.State and bEditEnabled
    
       

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
    
    #
    #   position (Translation)
    #
    
    btn_Pos_Active.Caption = "Translation"
    btn_Pos_Active.Justify = FBTextJustify.kFBTextJustifyLeft
    btn_Pos_Active.Style = FBButtonStyle.kFB2States
    btn_Pos_Active.Look = FBButtonLook.kFBLookColorChange
    main.Add(btn_Pos_Active, 20)
    btn_Pos_Active.OnClick.Add(BtnCallback_PosActive)
    
    box = FBHBoxLayout(FBAttachType.kFBAttachLeft)
    
    cb_Pos_MinX.Caption = "MinX"
    cb_Pos_MinX.Justify = FBTextJustify.kFBTextJustifyLeft
    cb_Pos_MinX.Style = FBButtonStyle.kFB2States 
    cb_Pos_MinX.Look = FBButtonLook.kFBLookColorChange
    box.Add(cb_Pos_MinX, 60)
    cb_Pos_MinX.OnClick.Add(CheckBoxCallback_PosAxis)
    
    cb_Pos_MaxX.Caption = "MaxX"
    cb_Pos_MaxX.Justify = FBTextJustify.kFBTextJustifyLeft
    cb_Pos_MaxX.Style = FBButtonStyle.kFB2States
    cb_Pos_MaxX.Look = FBButtonLook.kFBLookColorChange
    box.Add(cb_Pos_MaxX, 60)
    cb_Pos_MaxX.OnClick.Add(CheckBoxCallback_PosAxis)
    
    main.Add(box, 20)
    
    
    box = FBHBoxLayout(FBAttachType.kFBAttachLeft)
    
    cb_Pos_MinY.Caption = "MinY"
    cb_Pos_MinY.Justify = FBTextJustify.kFBTextJustifyLeft
    cb_Pos_MinY.Style = FBButtonStyle.kFB2States 
    cb_Pos_MinY.Look = FBButtonLook.kFBLookColorChange
    box.Add(cb_Pos_MinY, 60)
    cb_Pos_MinY.OnClick.Add(CheckBoxCallback_PosAxis)
    
    cb_Pos_MaxY.Caption = "MaxY"
    cb_Pos_MaxY.Justify = FBTextJustify.kFBTextJustifyLeft
    cb_Pos_MaxY.Style = FBButtonStyle.kFB2States
    cb_Pos_MaxY.Look = FBButtonLook.kFBLookColorChange
    box.Add(cb_Pos_MaxY, 60)
    cb_Pos_MaxY.OnClick.Add(CheckBoxCallback_PosAxis)
    
    main.Add(box, 20)
    
    box = FBHBoxLayout(FBAttachType.kFBAttachLeft)
    
    cb_Pos_MinZ.Caption = "MinZ"
    cb_Pos_MinZ.Justify = FBTextJustify.kFBTextJustifyLeft
    cb_Pos_MinZ.Style = FBButtonStyle.kFB2States 
    cb_Pos_MinZ.Look = FBButtonLook.kFBLookColorChange
    box.Add(cb_Pos_MinZ, 60)
    cb_Pos_MinZ.OnClick.Add(CheckBoxCallback_PosAxis)
    
    cb_Pos_MaxZ.Caption = "MaxZ"
    cb_Pos_MaxZ.Justify = FBTextJustify.kFBTextJustifyLeft
    cb_Pos_MaxZ.Style = FBButtonStyle.kFB2States
    cb_Pos_MaxZ.Look = FBButtonLook.kFBLookColorChange
    box.Add(cb_Pos_MaxZ, 60)
    cb_Pos_MaxZ.OnClick.Add(CheckBoxCallback_PosAxis)

    main.Add(box, 20)
    
    
    #
    #   Rotation
    #
    
    
    btn_Rot_Active.Caption = "Rotation"
    btn_Rot_Active.Justify = FBTextJustify.kFBTextJustifyLeft
    btn_Rot_Active.Style = FBButtonStyle.kFB2States
    btn_Rot_Active.Look = FBButtonLook.kFBLookColorChange
    main.Add(btn_Rot_Active, 20)
    btn_Rot_Active.OnClick.Add(BtnCallback_RotActive)

    
    box = FBHBoxLayout(FBAttachType.kFBAttachLeft)
    
    cb_Rot_MinX.Caption = "MinX"
    cb_Rot_MinX.Justify = FBTextJustify.kFBTextJustifyLeft
    cb_Rot_MinX.Style = FBButtonStyle.kFB2States 
    cb_Rot_MinX.Look = FBButtonLook.kFBLookColorChange
    box.Add(cb_Rot_MinX, 60)
    cb_Rot_MinX.OnClick.Add(CheckBoxCallback_RotAxis)
    
    cb_Rot_MaxX.Caption = "MaxX"
    cb_Rot_MaxX.Justify = FBTextJustify.kFBTextJustifyLeft
    cb_Rot_MaxX.Style = FBButtonStyle.kFB2States
    cb_Rot_MaxX.Look = FBButtonLook.kFBLookColorChange
    box.Add(cb_Rot_MaxX, 60)
    cb_Rot_MaxX.OnClick.Add(CheckBoxCallback_RotAxis)
    
    main.Add(box, 20)
    
    
    box = FBHBoxLayout(FBAttachType.kFBAttachLeft)
    
    cb_Rot_MinY.Caption = "MinY"
    cb_Rot_MinY.Justify = FBTextJustify.kFBTextJustifyLeft
    cb_Rot_MinY.Style = FBButtonStyle.kFB2States 
    cb_Rot_MinY.Look = FBButtonLook.kFBLookColorChange
    box.Add(cb_Rot_MinY, 60)
    cb_Rot_MinY.OnClick.Add(CheckBoxCallback_RotAxis)
    
    cb_Rot_MaxY.Caption = "MaxY"
    cb_Rot_MaxY.Justify = FBTextJustify.kFBTextJustifyLeft
    cb_Rot_MaxY.Style = FBButtonStyle.kFB2States
    cb_Rot_MaxY.Look = FBButtonLook.kFBLookColorChange
    box.Add(cb_Rot_MaxY, 60)
    cb_Rot_MaxY.OnClick.Add(CheckBoxCallback_RotAxis)
    
    main.Add(box, 20)
    
    box = FBHBoxLayout(FBAttachType.kFBAttachLeft)
    
    cb_Rot_MinZ.Caption = "MinZ"
    cb_Rot_MinZ.Justify = FBTextJustify.kFBTextJustifyLeft
    cb_Rot_MinZ.Style = FBButtonStyle.kFB2States 
    cb_Rot_MinZ.Look = FBButtonLook.kFBLookColorChange
    box.Add(cb_Rot_MinZ, 60)
    cb_Rot_MinZ.OnClick.Add(CheckBoxCallback_RotAxis)
    
    cb_Rot_MaxZ.Caption = "MaxZ"
    cb_Rot_MaxZ.Justify = FBTextJustify.kFBTextJustifyLeft
    cb_Rot_MaxZ.Style = FBButtonStyle.kFB2States
    cb_Rot_MaxZ.Look = FBButtonLook.kFBLookColorChange
    box.Add(cb_Rot_MaxZ, 60)
    cb_Rot_MaxZ.OnClick.Add(CheckBoxCallback_RotAxis)

    main.Add(box, 20)
    
    

    
   


def CreateTool():
    global tool
    tool = FBCreateUniqueTool("DOF Tool Updated")
    tool.StartSizeX = 200
    tool.StartSizeY = 320
    PopulateLayout(tool)
    ShowTool(tool)
    UpdateUI()
    
    # strictModeCheckBox.State = True
    

CreateTool()