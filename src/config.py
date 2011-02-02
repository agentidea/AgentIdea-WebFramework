"""
    Framework Configuration File
"""
class info(object):
    versionMajor = 0
    versionMinor = 4
    versionRevision = 8
    version = ( versionMajor,versionMinor,versionRevision)

    appName = "Table"
    
    ClientID = "demo"
    dbDefault = "tafel"
    identity = (ClientID,dbDefault)
    
    commandCoreTuple = ("src.framework.coreCommands","cmd")
    commandDomainTuple = ("src.custom.domainCommands","dc")
    
    rootTableCollectionName = "events"
    
    
    SHOW_ACTION = True
    HIDE_ACTION = False
    
    
    dbIP = "127.0.0.1"
    dbPort = 27017
    dbPwd = ""
    dbUsr = ""
    
    appLogoImage = "cropped.jpg"
    nav = [
           {'name':'new event','A':"APP.showNewTableForm('west');"},
           {'name':'event admin','A':"ShowEvents('west');"},
           {'name':'about','A':"ShowAbout('west');"},
           ]
    
    
    #WINDOWS
    #LogPath ="C:\inetpub\wwwroot\\net4\pyInetPub\DieTafel\core\src\log"
    #PathSep = '\\'
    
    #UNIX
    LogPath = "/var/wsgi/tafel/log"
    PathSep = '/'
    
    Log = "pyLog.txt"
    LogFile = "{0}{1}{2}".format(LogPath,PathSep,Log)
    
    
    #command on load string JS as base 64
    onCommandLoad64 = "Ly9hZGQgb25Db21tYW5kTG9hZCBKYXZhU2NyaXB0IGhlcmU="
    onCommandUnload64 = "Ly9hZGQgb25Db21tYW5kVW5sb2FkIEphdmFTY3JpcHQgaGVyZQ=="