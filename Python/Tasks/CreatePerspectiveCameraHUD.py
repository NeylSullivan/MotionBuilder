from pyfbsdk import *
from libHazardMoBuFunctions import *

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


HUD_NAME = 'Perspective_HUD'

# Remove all huds
hudsToDelete = []
elementsToDelete = []

for hud in FBSystem().Scene.HUDs:
    hudsToDelete.append(hud)
    for element in hud.Elements:
        elementsToDelete.append(element)

SafeDeleteObjects(elementsToDelete)

# Custom way for hud deletion, crashing when using SafeDeleteObjects
for hud in hudsToDelete:
    FBSystem().Scene.DisconnectSrc(hud)
    for cam in FBSystem().Scene.Cameras:
        cam.DisconnectSrc(hud)
    hud.FBDelete()

# Then create new one

hud = FBHUD(HUD_NAME)
FBSystem().Scene.ConnectSrc(hud) #Connect the HUD to the scene
FBSystem().Scene.Cameras[0].ConnectSrc(hud) #Connect to Perspective camera

srcRootBone = FBFindModelByLabelName("Root")
if srcRootBone:
    CreateHudElement(hud, 'Root Pos', 8, -8, 24, srcRootBone.PropertyList.Find('Lcl Translation'))
    CreateHudElement(hud, 'Root Rot', 8, -32, 24, srcRootBone.PropertyList.Find('Lcl Rotation'))

srcCameraBone = FBFindModelByLabelName("IK_Camera")
if srcCameraBone:
    CreateHudElement(hud, 'Cam Pos', 8, -64, 24, srcCameraBone.PropertyList.Find('Lcl Translation'), FBColorAndAlpha(1, 1, 1, 1))
    CreateHudElement(hud, 'Cam Rot', 8, -88, 24, srcCameraBone.PropertyList.Find('Lcl Rotation'), FBColorAndAlpha(1, 1, 1, 1))
