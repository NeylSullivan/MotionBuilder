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


def LayoutRadioButtonsGroup(pParentLayout, pSize, pCaptions, pSelectedIndex=0):
    group = FBButtonGroup()

    for i in range(len(pCaptions)): # pylint: disable=consider-using-enumerate
        b = FBButton()
        group.Add(b)
        b.Caption = pCaptions[i]
        b.Style = FBButtonStyle.kFBRadioButton
        if i == pSelectedIndex:
            b.State = True

        __AddToParentLayout(b, pParentLayout, pSize)

    return group


def LayoutEditNumber(pParentLayout, pSize, pValue, **kwarg):
    enb = FBEditNumber()
    enb.Value = pValue

    if 'Precision' in kwarg:
        enb.Precision = kwarg.get('Precision')

    if 'LargeStep' in kwarg:
        enb.LargeStep = kwarg.get('LargeStep')

    if 'SmallStep' in kwarg:
        enb.SmallStep = kwarg.get('SmallStep')

    if 'ReadOnly' in kwarg:
        enb.ReadOnly = kwarg.get('ReadOnly')

    __AddToParentLayout(enb, pParentLayout, pSize)
    return enb


def LayoutLabel(pParentLayout, pSize, pCaption, **kwarg):
    lbl = FBLabel()
    lbl.Caption = pCaption

    if 'Visible' in kwarg:
        lbl.Visible = kwarg.get('Visible')

    if 'ReadOnly' in kwarg:
        lbl.ReadOnly = kwarg.get('ReadOnly')

    if 'Enabled' in kwarg:
        lbl.Enabled = kwarg.get('Enabled')

    if 'Hint' in kwarg:
        lbl.Hint = kwarg.get('Hint')

    if 'Style' in kwarg:
        lbl.Style = kwarg.get('Style')

    if 'Justify' in kwarg:
        lbl.Justify = kwarg.get('Justify')

    if 'WordWrap' in kwarg:
        lbl.WordWrap = kwarg.get('WordWrap')

    __AddToParentLayout(lbl, pParentLayout, pSize)
    return lbl

def LayoutEmptySpace(pParentLayout, pSize):
    lbl = FBLabel()
    lbl.Visible = True
    lbl.ReadOnly = True
    lbl.Enabled = False
    lbl.Hint = None
    lbl.Caption = None
    lbl.WordWrap = True

    __AddToParentLayout(lbl, pParentLayout, pSize)
    return lbl

def LayoutCheckbox(pParentLayout, pSize, pCaption, pState, pCallback=None, **kwarg):
    chbx = FBButton()
    chbx.Caption = pCaption
    chbx.Style = FBButtonStyle.kFBCheckbox
    chbx.State = pState

    if pCallback:
        chbx.OnClick.Add(pCallback)

    if 'Hint' in kwarg:
        chbx.Hint = kwarg.get('Hint')

    if 'Justify' in kwarg:
        chbx.Justify = kwarg.get('Justify')
    else:
        chbx.Justify = FBTextJustify.kFBTextJustifyLeft


    __AddToParentLayout(chbx, pParentLayout, pSize)
    return chbx

def LayoutButton(pParentLayout, pSize, pCaption, pCallback, **kwarg):
    b = FBButton()
    b.Caption = pCaption
    if pCallback:
        b.OnClick.Add(pCallback)

    if 'Look' in kwarg:
        b.Look = kwarg.get('Look')

    if ('State0Color' in kwarg) and ('State1Color' in kwarg):
        b.Look = FBButtonLook.kFBLookColorChange
        b.SetStateColor(FBButtonState.kFBButtonState0, kwarg.get('State0Color'))
        b.SetStateColor(FBButtonState.kFBButtonState1, kwarg.get('State1Color'))

    __AddToParentLayout(b, pParentLayout, pSize)
    return b

def __AddToParentLayout(pWidget, pParentLayout, pSize):
    if pParentLayout:
        if isinstance(pSize, float):
            pParentLayout.AddRelative(pWidget, pSize)
        else:
            pParentLayout.Add(pWidget, pSize)
