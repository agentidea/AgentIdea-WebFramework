"""
    core Commands file
"""
import urllib
from src.framework.core import log, Utils, Command, ReturnEnvelope
from src.config import info
from src.framework.core import Framework 
from src.framework.strings import strings


class cmdInitialize:
    def executeCommand(self,command):
        
        import uuid
        guid = uuid.uuid1()
        panel = command.getValue("panel")
        
        command.kontext['SessionGUID'] = str(guid)
        setKontext = Command('SetKontext')
        setKontext.addParameter('SessionGUID', str(guid))
        command.outCommands.append(setKontext)
        
        
        Framework().intializeSystem(info)
        
        
        
        if( info.authenticateUser == True ):
            
            
            s = "<div><form id='frmLogin'>"
            s += "<table cellpadding='5'><tr><td>"
            s += "<img src='%s' />"
            s += "</td><td>"
            s += "<table>"
            s += "<tr><td>"
            s += "<DIV class='clsTextbox'>username:</DIV> </td>"            
            s += "<td>"            
            s += "<input type='text' value='' id='txtUsr'/>"
            s += "</td></tr>"
            s += "<tr><td>"
            s += "<DIV class='clsTextbox'>password: </DIV></td>"            
            s += "<td>"               
            s += "<input type='password' value='' id='txtPwd' />"
            s += "</td></tr>"
            s += "<tr><td>&nbsp;</td><td>"
            s += "<input type='button' value='%s' onclick=\" FWK.say('LocalLogin','%s'); \" />"
            s += "</td></tr></table></td></tr></table></form></div>"
            
            
            s = s % (info.LoginLogoURL,strings.LOGIN,panel)
            
            
            beforescript = """ 
            //JavaScript
            displayMsg('Please enter your username and password',msgCode.info);
            """
            
            afterscript = """
            try { document.getElementById('txtUsr').focus(); } catch (expp) {} 
            
            """
            
            displayCmd = Command('Display')
            displayCmd.addParameter('panel', panel)
            displayCmd.addParameter('html64', Utils().pack(s) )
            displayCmd.beforeload_JScript = Utils().pack(beforescript)
            displayCmd.afterload_JScript = Utils().pack(afterscript)
            
            
            command.outCommands.append(displayCmd)   
        else:
            """display navigation"""
            showNavigation = Command('ShowNavigation')
            showNavigation.addParameter('panel', panel)
            command.outCommands.append(showNavigation)


class cmdAuthenticate:
    def executeCommand(self,command):
        panel = command.getValue("panel")
        usr  = command.getValue("usr").decode('base64','strict')
        pwd =  command.getValue("pwd").decode('base64','strict')
       
        from src.framework import mongo
        userInDB = mongo.MongoDBComponents(info.dbIP,info.dbPort).find_one(info.dbDefault, info.userCollection, {'username': usr } )
        s = strings.NO_SUCH_USER
        if(userInDB):
            #user found
            if(userInDB['password'] == pwd):
                #user authenticated
                s = strings.WELCOME + " " + userInDB['username']
                
                """display navigation"""
                showNavigation = Command('ShowNavigation')
                showNavigation.addParameter('panel', panel)
                command.outCommands.append(showNavigation)
                
                
                """set session timeout value"""
                setKontext = Command('SetKontext')
                setKontext.addParameter('sessionTimeoutMinutes', info.sessionTimeoutMinutes)
                command.outCommands.append(setKontext)
                
                
                """set kredentials"""
                setKreds = Command('SetKontext')
                kredPair = "%s_%s" % ( userInDB['username'], userInDB['password'] )
                setKreds.addParameter('kreds',Utils().pack(kredPair))
                command.outCommands.append(setKreds)
                

       
        displayCmd = Command('Alert')
        displayCmd.addParameter('msg', Utils().pack(s) )
        command.outCommands.append(displayCmd)    
    
    
class cmdSignout:
    def executeCommand(self,command):
        log("%s signed out" % (command.kontext['SessionGUID'])) 
        
        displayCmd = Command('Intialize')
        displayCmd.addParameter('panel', 'farnorth')
        command.outCommands.append(displayCmd)      
    
class cmdRemoveRemoteLog:
    def executeCommand(self,command):
        panel = command.getValue("panel")

        Utils().removeFile(info.LogFile)
        
        s = "removed server log file permanently"
        log("command %s - %s" % (command.name,s)) #log after the fact to make sure log file is clean looking ( not half the log event from this command
        
       
        displayCmd = Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', Utils().pack(s) )
        command.outCommands.append(displayCmd)        
       
class cmdShowRemoteLog:
    def executeCommand(self,command):
       
        panel = command.getValue("panel")
        lines = command.getValue("lines")
        intLines = int(lines)
        
        
        s = "<div id='windowRemoteLog' class='clsPanel'>"
        s += "<b>Server Log Remote View</b>"
        s += "<span id='xRemoteLog' title='close panel' class='clsXWindowX' onclick=\" FWK.say('ClearXwindow',this.id); \">x</span>"
        s += "<div class='clsLog'><textarea id='TexAreaLog' class='clsTextAreaLog'>"
        s += Utils().tail(info.LogFile,intLines)
        s += "</textarea></div>"
      
        s += "<div class='clsAbout'><input type='button' value='clear server log' onclick=\" FWK.say('RemoveRemoteLog','%s',25); \" /></div>" % panel
        s += "</div>"
        
        log("IN command %s( %s %s)" % (command.name,lines,panel)) #log after the fact to make sure log file is clean looking ( not half the log event from this command
        
        
        displayCmd = Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', Utils().pack(s) )
        command.outCommands.append(displayCmd)        
  
class cmdShowAbout:
    
    def executeCommand(self,command):
        log("IN command %s" % (command.name))
        panel = command.getValue("panel")
        s = "<div class='clsPanel'>"
        s += "<b>Information about this Application</b>"
        s += "<div class='clsAbout'>{0} ver {1}.{2}.{3}</div>".format(info.appName,info.versionMajor,info.versionMinor,info.versionRevision)
        s += "<div class='clsAbout'>db://{0}:{1} db name: {2}</div>".format(info.dbIP,info.dbPort,info.dbDefault)
        s += "<div class='clsAbout'>session {0} path</div>".format(command.kontext['SessionGUID'])
        s += ""
        s += "</div>"
        
        
        displayCmd = Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', Utils().pack(s) )
        command.outCommands.append(displayCmd)


class cmdCommandsReflect:
    
    def executeCommand(self,command):
        log("IN command %s" % (command.name))
        panel = command.getValue("panel")
        
        s = "<div class='clsPanel'>"
        
        from src.framework import coreCommands
        from src.custom import domainCommands
        
        s += "<div class='clsHeader'>core commands</div>"
        s = self.listCmds(s, dir(coreCommands) ,info.commandCoreTuple)
        s += "<div class='clsHeader'>custom commands</div>"
        s = self.listCmds(s, dir(domainCommands),info.commandDomainTuple)
        
        
        
        s += "</div>"
        
        
        displayCmd = Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', Utils().pack(s) )
        command.outCommands.append(displayCmd)
        
        
    def listCmds(self,s,lst,t):
        
        s += "<table border='1'>"
        for item in lst:
            if item.startswith(t[1]):
                s += "<tr>"
                s += "<td>"
                s += item
                s += "</td>"
                s += "<td>set group[rwxd] user[rwxd]"
                s += "</tr>"
        
        s += "</table>"
        
        return s

class cmdShowNavigation:
    
    def executeCommand(self,command):
        log("IN command %s" % (command.name))
        
        panel = command.getValue("panel")
        
        s = "<div class='clsNavigationPanel'>"
        s += "<table class='clsGrid' border='0' cellspacing='0'>"
        s += "<tr>"
        s += "<td>"
        s += "<div class='clsNavigationPanel'><img src='./images/{0}' /></div>".format(info.appLogoImage)
        s += "</td>"

        nav = info.nav
        for n in nav:
            
            s += "<td class='clsNavElement' valign='bottom'>"
            s += "<div class='clsHyperlink' "
            s += ' onclick="{0}" >'.format(n['A'])
            s += n['name']
            s += "</div>"
            s += "</td>"
            
        
        s += "</tr>"
        
        s += "</table>"
        s += "</div>"
        
        s64 = s.encode('base64','strict')
        s64 = urllib.quote(s64)

        
        
        
        
        displayCmd = Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', s64 )
        command.outCommands.append(displayCmd)
        
        w = "{0} ver{1}.{2}.{3}".format(info.appName,info.versionMajor,info.versionMinor,info.versionRevision)
        w64 = Utils().pack(w)
        DisplayWindowTitle = Command('DisplayWindowTitle')
        DisplayWindowTitle.addParameter('html64', w64 )
        command.outCommands.append(DisplayWindowTitle)
        

class cmdPing:
    def executeCommand(self, command):
        name=command.params[0].val
        
        displayCmd = Command("ReturnCommand")
        displayCmd.addParameter('echo', name )
        
        command.outCommands.append(displayCmd)



