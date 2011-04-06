
"""
    domain specific Command file
    
    in this case these are the commands specific to a specific system implementation
    
"""
import json
from src.framework.core import log, Utils, Command, ReturnEnvelope
from src.config import info
from src.framework import treePattern as tp
from pymongo import objectid as OID
from src.framework import mongo



        
        
class dcSaveNewEvent:
    
    def executeCommand(self,command):
        log("IN command %s" % (command.name))
        table64 = command.getValue("table64")
        
        tableJSON = table64.decode('base64','strict')
        tableDict = json.loads(tableJSON)
        
        #get event ID
        db = mongo.MongoDBComponents(info.dbIP,info.dbPort)
        allEvents = db.find_all(info.dbDefault, info.rootTableCollectionName)
        
        #$to do: need a better way to do this ...
        #max = allEvents.count
        maxEvent = 0
        for ev in allEvents:
            maxEvent += 1;
            
        tableNumber = maxEvent + 1

        # move this block to function ...
        
        tableDict['tableNumber'] = tableNumber
        
        mongo.newMongo(info).save(info.dbDefault,info.rootTableCollectionName, tableDict)

        log("recieved table JSON %s" % (tableJSON) )
        panel = command.getValue("panel")

        s = "Saved new Table Event #%s" % ( str(tableNumber) )

        displayCmd = Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', Utils().pack(s) )
        
        command.outCommands.append(displayCmd)       
    
 
class dcDeleteEvent:
    
    def executeCommand(self,command):
        log("IN command %s" % (command.name))
        table_id = command.getValue("table_id")
        panel = command.getValue("panel")
        
        mdb = mongo.MongoDBComponents(info.dbIP,info.dbPort)
        mdb.deleteDocument(info.dbDefault, info.rootTableCollectionName, {'_id': OID.ObjectId(table_id) } )
        s = "Deleted Table #%s" % ( str(table_id) )

        displayCmd = Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', Utils().pack(s) )
        
        command.outCommands.append(displayCmd)    

class dcCreateInvitesOffTemplate:
    def executeCommand(self,command):
        """ prepare invitations """
        panel = command.getValue("panel")
        template64 = command.getValue("template64")
        targetUsers = command.getValue("targetUsers")
        eventGUID = command.getValue("eventGUID")
        action = command.getValue("action")
        """save | save+send """
        
        #apply template to all users
        
        
        #persist invites
        
        #send
        
        #dsiplay status...

class dcProcessInvites:
    
    def executeCommand(self,command):
        log("IN command %s" % (command.name))
        panel = command.getValue("panel")
        table_id = command.getValue("table_id")
        mongoHelper, tableDoc = tp.targetMongo(info.dbDefault,info.rootTableCollectionName,
                                     {'_id':OID.ObjectId(table_id)},
                                     info)
        
        #fix the error on passing back ObjectId -- need to translate this back on saveing ...
        tableDoc['_id'] = table_id
        
        tableJSON = json.dumps(tableDoc)
        
        
        loadJS = Command('LoadAppSpecificJS')
        loadJS.addParameter('panel', panel)
        loadJS.addParameter('JSON64', Utils().pack(tableJSON) )
        loadJS.addParameter('JSmoduleToCall','APP.inviteMx')
        command.outCommands.append(loadJS)
    
class dcShowEvents:
    """show events"""
    spec = { 'name':'ShowEvents', 'params':[
                                         {'name':'panel','req':1,'vals':info.panels}
                                         ]}
    
    def executeCommand(self,command):
        log("IN command %s" % (command.name))
        panel = command.getValue("panel")
        
        db = mongo.MongoDBComponents(info.dbIP,info.dbPort)
        allEvents = db.find_all(info.dbDefault, info.rootTableCollectionName)
        
        s = "<table border='0' cellspacing='0' cellpadding='5'>"
        s += "<tr class='clsGridHeaderRow'>"
        s += "<td>table #</td>"
        s += "<td>venue</td>"
        s += "<td>street</td>"
        s += "<td>street2</td>"
        s += "<td>city</td>"
        s += "<td>state</td>"
        s += "<td>zip</td>"
        s += "<td>country</td>"
        s += "<td>date</td>"
        s += "<td>time</td>"
        s += "<td>hosts</td>"
        s += "<td>guests</td>"
        s += "<td colspan='3'>actions</td>"
        s += "</tr>"
        
        
        
        for ev in allEvents:
            s += "<tr class='clsGridRow'>"
            s += "<td>{0}</td>".format(ev['tableNumber'])
            s += "<td>{0}</td>".format(ev['location']['venue'])
            s += "<td>{0}</td>".format(ev['location']['street'])
            s += "<td>{0}</td>".format(ev['location']['street2'])
            s += "<td>{0}</td>".format(ev['location']['city'])
            s += "<td>{0}</td>".format(ev['location']['state'])
            s += "<td>{0}</td>".format(ev['location']['zip'])
            s += "<td>{0}</td>".format(ev['location']['country'])
            s += "<td>{0}</td>".format(ev['meta']['date'])
            s += "<td>{0}</td>".format(ev['meta']['time'])
            s += "<td>{0}</td>".format(len(ev['hosts']))
            s += "<td>{0}</td>".format(len(ev['guests']))
            s += "<td><input class='clsGridButton' type='button' value='edit' id='cmd_{0}_edit' onclick=\"FWK.say('EditEvent','{1}','{2}');\" /></td>".format(ev['tableNumber'],ev['_id'],panel)
            s += "<td><input class='clsGridButton' type='button' value='delete' id='cmd_{0}_delete' onclick=\"FWK.say('DeleteEvent','{1}','{2}','{3}');\" /></td>".format(ev['tableNumber'],ev['_id'],panel,ev['tableNumber'])
            s += "<td><input class='clsGridButton' type='button' value='process invites' id='cmd_{0}_proc' onclick=\"FWK.say('ProcessInvites','{1}','{2}');\" /></td>".format(ev['tableNumber'],ev['_id'],panel)
            s+= "</tr>"
        
        
        s += "</table>"
        
        
        displayCmd = Command('Display')
        displayCmd.addParameter('panel', panel)
        displayCmd.addParameter('html64', Utils().pack(s) )
        
        command.outCommands.append(displayCmd)   