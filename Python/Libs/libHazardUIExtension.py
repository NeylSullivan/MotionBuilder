from pyfbsdk import *
from pyfbsdk_additions import *
from contextlib import contextmanager

@contextmanager
def BorderedVertBoxLayout(mainLyt, height=75):
    try:
        borderBox = FBHBoxLayout()
        borderRegionName = 'Inset'
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
        mainLyt.GetControl('main').Add(borderBox, height)

@contextmanager
def HorBoxLayout(parentLayout, height=25):
    try:
        box = FBHBoxLayout()
        yield box
    finally:
        parentLayout.Add(box, height)
