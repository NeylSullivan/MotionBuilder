import pyfbsdk as fb

def PrintClipProperties(inClip):
    print inClip.Name, "Properties: " + "\n"
    for prop in inClip.PropertyList:
        if prop.GetName():
            try:
                print '%s: %s %s' % (prop.GetPropertyTypeName(), prop.GetName(), inClip.__getattribute__(prop.GetName()))
            except BaseException:
                print '%s: %s NOATTRIBUTE' % (prop.GetPropertyTypeName(), prop.GetName())


for track in fb.FBStory().RootFolder.Tracks:
    print '\n'
    print 'Track %s\n' % track.Name
    print '\n'
    for clip in track.Clips:
        PrintClipProperties(clip)

    for subtrack in track.SubTracks:
        print '\n'
        print 'SubTrack %s\n' % subtrack.Name
        print '\n'
        for clip in subtrack.Clips:
            PrintClipProperties(clip)
