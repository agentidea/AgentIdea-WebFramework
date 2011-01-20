import os
"""
    Configuration File v1
"""

versionMajor = 0
versionMinor = 4
versionRevision = 5

appName = "tafel"

ClientID = "demo"
dbDefault = "tafel"
identity = (ClientID,dbDefault)

commandCoreTuple = ("coreCommands","cmd")
commandDomainTuple = ("domainCommands","dc")

rootTableCollectionName = "events"


SHOW_ACTION = True
HIDE_ACTION = False


dbIP = "127.0.0.1"
dbPort = 27017
dbPwd = ""
dbUsr = ""

appLogoImage = "cropped.jpg"
nav = [
       {'name':'new event','A':"ShowNewTableForm('west');"},
       {'name':'event admin','A':"ShowEvents('west');"},
       {'name':'about us','A':"ShowAbout('west');"},
       ]



LogPath ="C:\inetpub\wwwroot\\net4\pyInetPub\DieTafel\core\src\logs"
#LogPath = "/var/wsgi/tafel/log

Log = "pyLog.txt"
LogFile = "{0}{1}{2}".format(LogPath,os.pathsep,Log)


#command on load string JS as base 64
onCommandLoad64 = "Ly9hZGQgb25Db21tYW5kTG9hZCBKYXZhU2NyaXB0IGhlcmU="
onCommandUnload64 = "Ly9hZGQgb25Db21tYW5kVW5sb2FkIEphdmFTY3JpcHQgaGVyZQ=="