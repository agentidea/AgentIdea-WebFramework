from Http import *


#import urllib
#import sys
# $to do: intended for GET based requests / RESTFUL interface ... needs revisioin ...
pass

'''
                                                                    #add module path search info to this module
sys.path.append('C:\inetpub\wwwroot\\net4\pyInetPub\site\src')
import core



"""

   RESTFUL interface to requesting string based Command p1 p2 p3

"""



    

def processCommand(cmd):
    """ processess a Command dynamically """
    #core.inspectCommand(cmd)

    moduleID = "coreCommands"
    klassID = "cmd" + cmd.name
   
    Log("about to load %s" % (klassID))
    
    
    mod = __import__(moduleID, globals(), locals(), [klassID]) 
    klass = getattr(mod, klassID) 
    c = klass()
    ret = c.executeCommand(cmd)
    
    return ret


""" main request handler """
def Request():
    Header("Content-type: text/html")
    
    Log("%s request" % ( Env.REQUEST_METHOD ))
    
    Log("QUERY from %s" % (Env.QUERY_STRING))
    
    query_in = dict((N.lower(), V) for N, V in [Item.split('=',1) for Item in Env.QUERY_STRING.split('&') if Item])
    
    if query_in.has_key('cmd') == 1:
        passedCommand = urllib.unquote(query_in["cmd"])
        cmd = Parse(passedCommand)
        ret = processCommand(cmd)
        #Log("processed Command %s" % (cmd.name))
        #Write("type " + type(ret).ToString() )
        Write(str(ret))
        Log("End Processing")
        
    else:
        WriteAndLog("please pass in a cmd QUERY string variable")

    


def Parse(commandString):
    bits = commandString.split(' ')
    
    cmd = None

    cursor = 0
    for bit in bits:
        cursor += 1
        if cursor == 1:
            cmd=core.Command(bit)
        else:
            cmd.addParameterAnon(bit)
   
    return cmd


def WriteAndLog(s):
    Log(s)
    Write(s)
    
def Log(s):
    core.log(s)
 

    
'''    