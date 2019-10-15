# Copyright 2009 Autodesk, Inc.  All rights reserved.
# Use of this software is subject to the terms of the Autodesk license agreement
# provided at the time of installation or download, or which otherwise accompanies
# this software in either electronic or hard copy form.
#
# Script description:
# Create a tool that shows how drag and drop works.
# Allow for a model to be dropped in a container. From that model show its property list and allow edition/selection
# of all the properties.
#
# Topic: FBVisualContainer, FBSceneChangeType, FBDragAndDropState, FBPropertyFlag, FBEditPropertyModern, FBEditProperty
#

from pyfbsdk import *
from pyfbsdk_additions import *

def SetupPropertyList(model):
    tool.container.Items.removeAll()
    tool.list.Items.removeAll()
    tool.prop_list = []

    tool.prop.Property = None
    tool.prop_modern.Property = None

    tool.model = model

    if model:
        tool.container.Items.append(model.Name)
        tool.list.Items.append("<Select Property>")
        tool.prop_list.append(None)
        for p in model.PropertyList:
            if p and p.IsInternal() and not p.GetPropertyFlag(FBPropertyFlag.kFBPropertyFlagHideProperty):
                tool.list.Items.append(p.Name)
                tool.prop_list.append(p)
        tool.list.ItemIndex = 0
        PropertyListChanged(tool.list, None)


def EventContainerDblClick(control, event):
    SetupPropertyList(None)

def EventContainerDragAndDrop(control, event):
    if event.State == FBDragAndDropState.kFBDragAndDropDrag:
        event.Accept()
    elif event.State == FBDragAndDropState.kFBDragAndDropDrop:
        SetupPropertyList( event.Components[0] )

def PropertyListChanged(control, event):
    tool.prop.Property = tool.prop_list[control.ItemIndex]
    tool.prop_modern.Property = tool.prop_list[control.ItemIndex]

def PrevProperty(control, event):
    if tool.list.ItemIndex - 1 < 0:
        tool.list.ItemIndex = len(tool.list.Items)-1
    else:
        tool.list.ItemIndex = tool.list.ItemIndex - 1
    PropertyListChanged(tool.list, None)

def NextProperty(control, event):
    if tool.list.ItemIndex + 1 >= len(tool.list.Items):
        tool.list.ItemIndex = 0
    else:
        tool.list.ItemIndex = tool.list.ItemIndex + 1
    PropertyListChanged(tool.list, None)

def SceneChanged(scene, event):
    if len(tool.container.Items) != 0 and \
        event.Type == FBSceneChangeType.kFBSceneChangeDetach  and \
        event.ChildComponent == tool.model:
        SetupPropertyList(None)


def PopulateLayout(mainLyt):
    x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachBottom,"")
    mainLyt.AddRegion("main","main", x, y, w, h)
    vlyt = FBVBoxLayout()
    mainLyt.SetControl("main",vlyt)

    l = FBLabel()
    l.Caption = "Drag and drop a model into the container. Double click to clear."
    vlyt.Add(l,30)

    tool.model = None
    tool.container = FBVisualContainer()
    tool.container.OnDragAndDrop.Add(EventContainerDragAndDrop)
    tool.container.OnDblClick.Add(EventContainerDblClick)
    vlyt.Add(tool.container,30)

    hlyt = FBHBoxLayout()
    tool.list = FBList()
    tool.list.OnChange.Add(PropertyListChanged)
    hlyt.AddRelative(tool.list)

    prev = FBButton()
    prev.OnClick.Add(PrevProperty)
    prev.Caption = "<"
    hlyt.Add(prev, 30)

    next = FBButton()
    next.OnClick.Add(NextProperty)
    next.Caption = ">"
    hlyt.Add(next, 30)

    vlyt.Add(hlyt, 30)

    tool.prop = FBEditProperty()
    vlyt.Add(tool.prop, 30)

    tool.prop_modern = FBEditPropertyModern()
    vlyt.Add(tool.prop_modern, 30)

    # Register for scene event
    FBSystem().Scene.OnChange.Add(SceneChanged)

    # register when this tool is destroyed.
    tool.OnUnbind.Add(OnToolDestroy)


def OnToolDestroy(control,event):
    # Important: each time we run this script we need to remove
    # the SceneChanged from the Scene else they will accumulate
    FBSystem().Scene.OnChange.Remove(SceneChanged)

def CreateTool():
    global tool

    tool = FBCreateUniqueTool("Property Example")
    tool.StartSizeX = 400
    tool.StartSizeY = 200
    PopulateLayout(tool)
    ShowTool(tool)


CreateTool()
