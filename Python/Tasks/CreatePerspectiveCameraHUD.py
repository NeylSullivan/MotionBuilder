from pyfbsdk import *

#Init
Scene = FBSystem().Scene
System = FBSystem()
Application = FBApplication()

HUD = FBHUD("HazardHUD")
lHudCamPos = FBHUDTextElement("IK_FPCam Pos")
Scene.ConnectSrc(HUD)          #Connect the HUD to the scene
lHudCamPos.Content =  "IK_FPCam Pos %s"
lHudCamPos.X = 2
lHudCamPos.Y = -2
lHudCamPos.Height = 6
lHudCamPos.Justification = FBHUDElementHAlignment.kFBHUDLeft
lHudCamPos.HorizontalDock = FBHUDElementHAlignment.kFBHUDLeft
lHudCamPos.VerticalDock = FBHUDElementVAlignment.kFBHUDTop

lHudCamPos.Font = "Times New Roman"   #Set Font of FBHUDTextElement

HUD.ConnectSrc(lHudCamPos) #Connect HUDTextElement to the HUD

lIK_FPCam = FBFindModelByLabelName("IK_FPCam")
plIK_FPCamTranslation = lIK_FPCam.PropertyList.Find('Lcl Translation')
lHudCamPos.ConnectSrc(plIK_FPCamTranslation) # Connect the HUD to the property

lHudCamRot = FBHUDTextElement("IK_FPCam Rot")
Scene.ConnectSrc(HUD)          #Connect the HUD to the scene
lHudCamRot.Content =  "IK_FPCam Rot %s"
lHudCamRot.X = 2
lHudCamRot.Y = -8
lHudCamRot.Height = 6
lHudCamRot.Justification = FBHUDElementHAlignment.kFBHUDLeft
lHudCamRot.HorizontalDock = FBHUDElementHAlignment.kFBHUDLeft
lHudCamRot.VerticalDock = FBHUDElementVAlignment.kFBHUDTop

lHudCamRot.Font = "Times New Roman"   #Set Font of FBHUDTextElement

HUD.ConnectSrc(lHudCamRot) #Connect HUDTextElement to the HUD


plIK_FPCamRotation = lIK_FPCam.PropertyList.Find('Lcl Rotation')
lHudCamRot.ConnectSrc(plIK_FPCamRotation) # Connect the HUD to the property


Scene.Cameras[0].ConnectSrc(HUD) #Connect to Perspective camera
