"""
    Framework Configuration File
"""
from src.framework.strings import strings

class info(object):
    versionMajor = 0
    versionMinor = 5
    versionRevision = 9
    version = ( versionMajor,versionMinor,versionRevision)

    appName = "Table"
    
    ClientID = "demo"
    dbDefault = "tafel"
    identity = (ClientID,dbDefault)
    
    commandCoreTuple = ("src.framework.coreCommands","cmd")
    commandDomainTuple = ("src.custom.domainCommands","dc")
    
    rootTableCollectionName = "events"
    groupCollection = "groups"
    userCollection = "users"
    
    LoginLogoURL = './images/LoginLogo.jpg' 
    
    authenticateUser = True # users required to login via a login prompt 
    sessionTimeoutMinutes = 2
    
    SHOW_ACTION = True
    HIDE_ACTION = False
    
    
    dbIP = "127.0.0.1"
    dbPort = 27017
    dbPwd = ""
    dbUsr = ""
    
    appLogoImage = "cropped.jpg"
    nav = [
           
           {'name':'New Table','A':"FWK.say('ShowNewTable','west');"},
           {'name':'Tables','A':"FWK.say('ShowEvents','west');"},
           {'name':'Admin','A':"FWK.say('ShowToc','admin','farwest','vertical');"},
           {'name':'help','A':"FWK.say('ShowToc','help','farwest','vertical');"},
           
           {'name': strings.SIGNOUT, 'A':"FWK.say('Signout');"}
           
           ]
    vertNav = {
            
            'help': [
                {'name':'about','A':"FWK.say('ShowAbout','center');"},
                {'name':'support','A':"FWK.say('ShowSupport','center');"},
                {'name':'console','A':"FWK.say('ShowConsole','center');"}
            
            ],
            'admin': [
                {'name':'commands','A':"FWK.say('ShowAdmin','center');"},
                {'name':'pwd reset','A':"FWK.say('ShowPwdReset','center');"}
            ]
            
            }

    supportContacts = [
                       {'name':'Grant Steinfeld','email':'GrantSteinfeld@gmail.com'},
                       #{'name':'','email':'pmcnamee@smartorg.com'}
                       ]

    
    #WINDOWS
    #LogPath ="C:\inetpub\wwwroot\\net4\pyInetPub\DieTafel\core\src\log"
    #PathSep = '\\'
    
    #UNIX
    LogPath = "/var/wsgi/tafel/log"
    PathSep = '/'
    
    Log = "pyLog.txt"
    LogFile = "{0}{1}{2}".format(LogPath,PathSep,Log)
    
    
    
    smtpServer = "mail.agentidea.com"
    smtpUser = "mail_daemon@agentidea.com"
    smtpPwd = "jy1met2"
    
    bitlyKey = 'R_3f5c6a92ce6126b0da95ae9b3821f91b'
    bitlyUsr = 'grantsteinfeld'
    
    twitterAPI = 'aws3PhOfKfulnKNtyz4vQ' 
    """ twitter API key for AgentTweet"""
    
    #command on load string JS as base 64
    onCommandLoad64 = "Ly9hZGQgb25Db21tYW5kTG9hZCBKYXZhU2NyaXB0IGhlcmU="
    onCommandUnload64 = "Ly9hZGQgb25Db21tYW5kVW5sb2FkIEphdmFTY3JpcHQgaGVyZQ=="
    
    
