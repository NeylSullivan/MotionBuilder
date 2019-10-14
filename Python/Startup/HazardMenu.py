from pyfbsdk import *
import os
import ntpath

rootScriptsDir = r'e:\blackops\__WorkFlow\MotionBuilder\Python'
subdirsToCheck = ['Utils', 'Tasks', 'ThirdParty']

scriptsPaths = []

def split_on_uppercase(s, keep_contiguous=False):
    """

    Args:
        s (str): string
        keep_contiguous (bool): flag to indicate we want to keep contiguous uppercase chars together

    Returns:

    """

    string_length = len(s)
    is_lower_around = (lambda: s[i-1].islower() or 
                       string_length > (i + 1) and s[i + 1].islower())

    start = 0
    parts = []
    for i in range(1, string_length):
        if s[i].isupper() and (not keep_contiguous or is_lower_around()):
            parts.append(s[start: i])
            start = i
    parts.append(s[start:])
    
    finalName = ' '.join(parts)
    
    return finalName

def GetNiceName(path):
    fileName = ntpath.basename(path)
    fileNameWithoutExt = os.path.splitext(fileName)[0]
    niceName = split_on_uppercase(fileNameWithoutExt, True)
    return niceName
    
def EventMenu(control, event):
    desiredFileName = event.Name.replace(" ", "") + ".py"
    
    #check root dir first
    pathToFile = os.path.join(rootScriptsDir, desiredFileName)
    
    if os.path.isfile(pathToFile) and os.path.exists(pathToFile):
        FBApplication().ExecuteScript(pathToFile)
        return
    
    #check subdirs now
    for subdir in subdirsToCheck:
        directory = os.path.join(rootScriptsDir, subdir)
        pathToFile = os.path.join(directory, desiredFileName)
    
        if os.path.isfile(pathToFile) and os.path.exists(pathToFile):
            FBApplication().ExecuteScript(pathToFile)
            return
    
    print "Can't execute menu item: " + event.Name

    
id = 10

gMenuMgr = FBMenuManager()

gMenuMgr.InsertLast(None, "Hazard")
lNewMenu = gMenuMgr.GetMenu("Hazard")

# Debug
# lNewMenu.OnMenuActivate.RemoveAll()

for subdir in subdirsToCheck:
    directory = os.path.join(rootScriptsDir, subdir)
    insideMenu = FBGenericMenu()
    for file in os.listdir(directory):
        if file.endswith('.py'):
           menuItemName = GetNiceName(file)
           # print  subdir + "   " + menuItemName
           insideMenu.InsertLast(menuItemName, id)
           id += 1
    
    insideMenu.OnMenuActivate.Add(EventMenu)
    lNewMenu.InsertLast(subdir, id * 100, insideMenu)           
           

for file in os.listdir(rootScriptsDir):
    if file.endswith('.py'):
        menuItemName = GetNiceName(file)
        # print menuItemName
        lNewMenu.InsertLast(menuItemName, id)
        id += 1
   
    

lNewMenu.OnMenuActivate.Add(EventMenu)
