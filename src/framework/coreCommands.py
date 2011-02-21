"""
    core Commands file
"""
import urllib
from src.framework.core import log, Utils, Command, ReturnEnvelope
from src.config import info



class cmdInitialize:
    def executeCommand(self,command):
        
        import uuid
        guid = uuid.uuid1()

        command.kontext['SessionGUID'] = str(guid)
        
        s = "<b>initialize command called </b>" + command.kontext['SessionGUID']
        
        log("command %s - %s" % (command.name,s))
        
        
        displayCmd = Command('Display')
        displayCmd.addParameter('panel', 'west')
        displayCmd.addParameter('html64', Utils().pack(s) )
        
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
        s += "<div class='clsAbout'>logging to {0} path</div>".format(info.LogFile)
        s += "</div>"
        
        
        displayCmd = Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', Utils().pack(s) )
        command.outCommands.append(displayCmd)

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
        
        w = "{0} ver{1}.{2}.{3}".format(info.appName,info.versionMajor,info.versionMinor,info.versionRevision)
        
        w64 = Utils().pack(w)
        
        
        
        
        
        
        script = """ //JavaScript
        
        //ping('hello happy world');
        /*
        var d = document.createElement("div");
        var t = document.createTextNode("hello");
        d.appendChild(t);
        
        var attachPoint = document.getElementById("east");
        attachPoint.appendChild(d);
        */
        
        
        """
        
        
        
        displayCmd = Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', s64 )
        displayCmd.onload_JScript =  urllib.quote((script.encode('base64','strict')))
        
        DisplayWindowTitle = Command('DisplayWindowTitle')
        DisplayWindowTitle.addParameter('html64', w64 )
        
        
        command.outCommands.append(DisplayWindowTitle)
        command.outCommands.append(displayCmd)

class cmdPing:
    def executeCommand(self, command):
        name=command.params[0].val
        
        displayCmd = Command("ReturnCommand")
        displayCmd.addParameter('echo', name )
        
        command.outCommands.append(displayCmd)



