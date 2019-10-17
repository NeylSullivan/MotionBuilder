from pyfbsdk import *
from pyfbsdk_additions import *
from contextlib import contextmanager

@contextmanager
def BorderedVertBoxLayout(pMainLayout, pHeight=75, pRegionName='Inset'):
    try:
        borderBox = FBHBoxLayout()
        borderRegionName = pRegionName
        x = FBAddRegionParam(5, FBAttachType.kFBAttachLeft, "")
        y = FBAddRegionParam(5, FBAttachType.kFBAttachTop, "")
        w = FBAddRegionParam(-5, FBAttachType.kFBAttachRight, "")
        h = FBAddRegionParam(-5, FBAttachType.kFBAttachBottom, "")
        borderBox.AddRegion(borderRegionName, 'Loop', x, y, w, h)
        borderBox.SetBorder(borderRegionName, FBBorderStyle.kFBEmbossBorder, False, True, 2, 3, 90, 0)
        vertBox = FBVBoxLayout()
        yield vertBox
    finally:
        borderBox.SetControl(borderRegionName, vertBox)
        pMainLayout.GetControl('main').Add(borderBox, pHeight)

@contextmanager
def HorBoxLayout(pParentLayout, pHeight=25):
    try:
        box = FBHBoxLayout()
        yield box
    finally:
        pParentLayout.Add(box, pHeight)

def LayoutButton(pParentLayout, pSize, pCaption, pCallback, **kwarg):
    b = FBButton()
    b.Caption = pCaption
    b.OnClick.Add(pCallback)

    Look = kwarg.get('Look')
    if Look:
        b.Look = Look

    State0Color = kwarg.get('State0Color')
    if State0Color:
        b.SetStateColor(FBButtonState.kFBButtonState0, State0Color)

    State1Color = kwarg.get('State1Color')
    if State1Color:
        b.SetStateColor(FBButtonState.kFBButtonState1, State1Color)

    pParentLayout.Add(b, pSize)
    return b
