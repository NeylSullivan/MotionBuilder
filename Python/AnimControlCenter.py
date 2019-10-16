#
# AnimControlCenter
#
# Display user and reference properties of controlled character in separate ui
#

from pyfbsdk import *
from pyfbsdk_additions import *
from libHazardUIExtension import *

def UpdateUI(layout):
    layout.RemoveAll()

    if FBApplication().CurrentCharacter is None:
        l = FBLabel()
        l.Caption = "No current character to populate properties"
        l.Justify = FBTextJustify.kFBTextJustifyCenter
        layout.Add(l, 30)
        return

    l = FBLabel()
    l.Caption = FBApplication().CurrentCharacter.Name
    l.Justify = FBTextJustify.kFBTextJustifyCenter
    l.Style = FBTextStyle.kFBTextStyleBold
    layout.Add(l, 30)

    rigCtrlModel = FBApplication().CurrentCharacter.GetCtrlRigModel(FBBodyNodeId.kFBReferenceNodeId)
    if rigCtrlModel is None:
        l = FBLabel()
        l.Caption = "Missed reference control rig to populate properties"
        layout.Add(l, 30)
        return

    kLABEL_COLUMN_RELATIVE_WIDTH = 0.7

    for p in rigCtrlModel.PropertyList:
        if p.IsUserProperty() or p.IsReferenceProperty():
            horLayout = FBHBoxLayout()

            label = FBLabel()
            label.Caption = p.Name
            if p.IsReferenceProperty():
                label.Style = FBTextStyle.kFBTextStyleItalic
            horLayout.AddRelative(label, kLABEL_COLUMN_RELATIVE_WIDTH)

            prop_modern = FBEditPropertyModern()
            prop_modern.Property = p
            horLayout.AddRelative(prop_modern)

            layout.Add(horLayout, 20)

    with HorBoxLayout(layout, height=20) as horBox:
        lbl = FBLabel()
        lbl.Caption = "HUD"
        horBox.AddRelative(lbl, kLABEL_COLUMN_RELATIVE_WIDTH)

        b = FBButton()
        b.Caption = "Add"
        b.OnClick.Add(lambda control=None, event=None: AddOrRemoveHUD(True))
        horBox.AddRelative(b, 0.5)

        b = FBButton()
        b.Caption = "Remove"
        b.OnClick.Add(lambda control=None, event=None: AddOrRemoveHUD(False))
        horBox.AddRelative(b, 0.5)


def CreateHudElement(pHud, pName, pX, pY, pHeight, pSrcProp, pColor=FBColorAndAlpha(1.0, 0.5, 0.0, 1.0)):
    hudElement = FBHUDTextElement(pName)
    hudElement.Content = pName +': %s'
    hudElement.Color = pColor
    hudElement.X = pX
    hudElement.Y = pY
    hudElement.Height = pHeight
    hudElement.ScaleByPercent = False
    hudElement.PositionByPercent = False
    hudElement.Justification = FBHUDElementHAlignment.kFBHUDLeft
    hudElement.HorizontalDock = FBHUDElementHAlignment.kFBHUDLeft
    hudElement.VerticalDock = FBHUDElementVAlignment.kFBHUDTop
    hudElement.ConnectSrc(pSrcProp) # pylint: disable=no-member

    pHud.ConnectSrc(hudElement) #Connect HUDTextElement to the HUD

def AddOrRemoveHUD(pAdd):
    HUD_NAME = 'Character_HUD'

    hudsToDelete = []
    elementsToDelete = []

    for hud in FBSystem().Scene.HUDs:
        hudsToDelete.append(hud)
        for element in hud.Elements:
            elementsToDelete.append(element)

    for element in elementsToDelete:
        element.FBDelete()

    for hud in hudsToDelete:
        hud.FBDelete()

    if not pAdd:
        return

    hud = FBHUD(HUD_NAME)
    FBSystem().Scene.ConnectSrc(hud) #Connect the HUD to the scene
    FBSystem().Scene.Cameras[0].ConnectSrc(hud) #Connect to Perspective camera

    srcRootBone = FBFindModelByLabelName("Root")
    if srcRootBone:
        CreateHudElement(hud, 'Root Pos', 8, -8, 24, srcRootBone.PropertyList.Find('Lcl Translation'))
        CreateHudElement(hud, 'Root Rot', 8, -32, 24, srcRootBone.PropertyList.Find('Lcl Rotation'))

    srcCameraBone = FBFindModelByLabelName("IK_CAMERA")
    if srcCameraBone:
        CreateHudElement(hud, 'Cam Pos', 8, -64, 24, srcCameraBone.PropertyList.Find('Lcl Translation'), FBColorAndAlpha(1, 1, 1, 1))
        CreateHudElement(hud, 'Cam Rot', 8, -88, 24, srcCameraBone.PropertyList.Find('Lcl Rotation'), FBColorAndAlpha(1, 1, 1, 1))


def PopulateLayout(mainLyt):
    x = FBAddRegionParam(0, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(0, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(0, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(0, FBAttachType.kFBAttachBottom, "")
    main = FBVBoxLayout(FBAttachType.kFBAttachTop)
    mainLyt.AddRegion("main", "main", x, y, w, h)
    mainLyt.SetControl("main", main)

    UpdateUI(main)

    #b = FBButton()
    #b.Caption = "Make Markers"
    # b.Justify = FBTextJustify.kFBTextJustifyLeft
    #main.Add(b, 30)
    #b.OnClick.Add(BtnCallback_MakeMarkers)

def CreateTool():
    tool = FBCreateUniqueTool("Anim Control Center")
    tool.StartSizeX = 250
    tool.StartSizeY = 300
    PopulateLayout(tool)
    ShowTool(tool)

CreateTool()
