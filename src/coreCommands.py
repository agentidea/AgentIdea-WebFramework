"""
    core Commands file
"""
import core
import config
import urllib
import treePattern as tp
import json
import mongo
from pymongo import objectid as OID

class cmdShowAbout:
    
    def executeCommand(self,command):
        core.log("IN command %s" % (command.name))
        panel = command.getValue("panel")
        s = "<div class='clsPanel'>"
        s += "<b>Information about this Application</b>"
        s += "<div class='clsAbout'>{0} ver {1}.{2}.{3}</div>".format(config.appName,config.versionMajor,config.versionMinor,config.versionRevision)
        s += "<div class='clsAbout'>db://{0}:{1} db name: {2}</div>".format(config.dbIP,config.dbPort,config.dbDefault)
        s += "<div class='clsAbout'>logging to {0} path</div>".format(config.LogFile)
        s += "</div>"
        
        re = core.ReturnEnvelope()
        displayCmd = core.Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', core.pack(s) )
        re.add(displayCmd)
        return re

class cmdShowNavigation:
    
    def executeCommand(self,command):
        core.log("IN command %s" % (command.name))
        
        panel = command.getValue("panel")
        
        s = "<div class='clsNavigationPanel'>"
        s += "<table class='clsGrid' border='0' cellspacing='0'>"
        
        s += "<tr>"
        
        s += "<td>"
        s += "<div class='clsNavigationPanel'><img src='./images/{0}' /></div>".format(config.appLogoImage)
        s += "</td>"
        
        
        nav = config.nav
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
        
        w = "{0} ver{1}.{2}.{3}".format(config.appName,config.versionMajor,config.versionMinor,config.versionRevision)
        
        w64 = core.pack(w)
        
        
        re = core.ReturnEnvelope()
        
        
        
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
        
        
        
        displayCmd = core.Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', s64 )
        displayCmd.onload_JScript =  urllib.quote((script.encode('base64','strict')))
        
        DisplayWindowTitle = core.Command('DisplayWindowTitle')
        DisplayWindowTitle.addParameter('html64', w64 )
        
        
        re.add(DisplayWindowTitle)
        re.add(displayCmd)
        return re

class cmdPing:
    def executeCommand(self, command):
        name=command.params[0].val
        
        re = core.ReturnEnvelope()
        displayCmd = core.Command("ReturnCommand")
        displayCmd.addParameter('echo', name )
        re.add(displayCmd)
        
        return re

#domain specific commands should move to seperate file ...    



class cmdProcessInvites:
    
    def executeCommand(self,command):
        core.log("IN command %s" % (command.name))
        panel = command.getValue("panel")
        table_id = command.getValue("table_id")
        
        mongoHelper, tableDoc = tp.targetMongo(config.dbDefault,config.rootTableCollectionName,
                                     {'_id':OID.ObjectId(table_id)},
                                     config)
        
        #fix the error on passing back ObjectId -- need to translate this back on saveing ...
        tableDoc['_id'] = table_id
        
        tableJSON = json.dumps(tableDoc)
        
        re = core.ReturnEnvelope()
        loadJS = core.Command('LoadAppSpecificJS')
        loadJS.addParameter('panel', panel)
        loadJS.addParameter('JSON64', core.pack(tableJSON) )
        loadJS.addParameter('JSmoduleToCall','InviteMx')
        re.add(loadJS)
        return re



class cmdShowEvents:
    
    def executeCommand(self,command):
        core.log("IN command %s" % (command.name))
        panel = command.getValue("panel")
        
        db = mongo.MongoDBComponents(config.dbIP,config.dbPort)
        allEvents = db.find_all(config.dbDefault, config.rootTableCollectionName)
        
        s = "<table>"
        s += "<tr class='clsGridHeaderRow'>"
        s += "<td>Table Number</td><td>location</td><td>city</td><td># guests</td><td># hosts</td><td colspan='2'>actions</td>"
        s += "</tr>"
        
        
        
        for ev in allEvents:
            s += "<tr class='clsGridRow'>"
            s += "<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}<td><input class='clsGridButton' type='button' value='delete' id='{5}' onclick=\"DeleteEvent(this,'{6}');\" /></td><td><input class='clsGridButton' type='button' id='{5}' value='ProcessInvites' onclick='ProcessInvites(this,\"{6}\");' /></td>".format(ev['tableNumber'],ev['location']['name'],ev['location']['city'],len(ev['guests']),len(ev['hosts']),ev['_id'],panel)
            s+= "</tr>"
        
        
        s += "</table>"
        
        re = core.ReturnEnvelope()
        displayCmd = core.Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', core.pack(s) )
        re.add(displayCmd)
        return re


class cmdSaveNewEvent:
    
    def executeCommand(self,command):
        core.log("IN command %s" % (command.name))
        table64 = command.getValue("table64")
        
        tableJSON = table64.decode('base64','strict')
        
        tableDict = json.loads(tableJSON)
        
        ############################################################################
        #find event ID
        db = mongo.MongoDBComponents(config.dbIP,config.dbPort)
        allEvents = db.find_all(config.dbDefault, config.rootTableCollectionName)
        #max = allEvents.count
        maxEvent = 0
        for ev in allEvents:
            maxEvent += 1;
            
        tableNumber = maxEvent + 1
        #############################################################################
        # move this block to function ...
        
        tableDict['tableNumber'] = tableNumber
        
        mongo.newMongo(config).save(config.dbDefault,config.rootTableCollectionName, tableDict)

        core.log("recieved table JSON %s" % (tableJSON) )
        panel = command.getValue("panel")

        s = "Saved new Table Event #%s" % ( str(tableNumber) )

        re = core.ReturnEnvelope()
        displayCmd = core.Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', core.pack(s) )
        
        re.add(displayCmd)
        return re
   

    