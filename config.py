"""
    AgentIdea Framework
    config
"""

versionMajor = 1
versionMinor = 0
versionRevision = 0

appName = "DEMO"

ClientID = "demo"
dbDefault = "demo"
identity = (ClientID,dbDefault)


LogPath ="C:\inetpub\wwwroot\\net4\pyInetPub\demo\\demo\logs"
Log = "pyLog.txt"
LogFile = "{0}\{1}".format(LogPath,Log)

commandDefaultTuple = ("coreCommands","cmd")

#MongoDB credentials
dbIP = "127.0.0.1"
dbPort = 27017
dbPwd = ""
dbUsr = ""

rootProjectCollectionName = "nodes.general"
rootProjectTreeName = "root_v1"

SHOW_ACTION = True
HIDE_ACTION = False



appLogoImage = "myLogo.jpg"

#simple navigation defined here
nav = [
       {'name':'about us','A':"ShowAbout('west');"},
       
       {'name':'admin','A':"log('admin to be linked here');"},
       {'name':'contact us','A':"log('contact us');"},
       
       ]

onCommandLoad64 = "Ly9hZGQgb25Db21tYW5kTG9hZCBKYXZhU2NyaXB0IGhlcmU="
onCommandUnload64 = "Ly9hZGQgb25Db21tYW5kVW5sb2FkIEphdmFTY3JpcHQgaGVyZQ=="