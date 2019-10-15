#
# AnimController
#
# Display user and reference properties of controlled character in separate ui
#

from pyfbsdk import *
from pyfbsdk_additions import *

def UpdateUI(layout):
    layout.RemoveAll()

    if FBApplication().CurrentCharacter is None:
        l = FBLabel()
        l.Caption = "No current character to populate properties"
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

    for p in rigCtrlModel.PropertyList:
        if p.IsUserProperty() or p.IsReferenceProperty():
            horLayout = FBHBoxLayout()

            label = FBLabel()
            label.Caption = p.Name
            if p.IsReferenceProperty():
                label.Style = FBTextStyle.kFBTextStyleItalic
            horLayout.AddRelative(label, 0.7)

            prop_modern = FBEditPropertyModern()
            prop_modern.Property = p
            horLayout.AddRelative(prop_modern)

            layout.Add(horLayout, 20)



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
    t = FBCreateUniqueTool("Anim Controller")
    t.StartSizeX = 250
    t.StartSizeY = 300
    PopulateLayout(t)
    ShowTool(t)

CreateTool()
