#
# APACHE WSGI entry point
#

import json
import time
import core

def index(environ, start_response):
    
    start = time.time()
    #post data is base64 encoded
 
    post64 = Read()
    postClear = post64.decode('base64','strict')
 
    macroDict = json.loads(postClear)
    cmd = ParseMacroDict(macroDict)
    retEnv = core.processCommand(cmd)
    retJSON = retEnv.toJSON()
    
    end = time.time() - start
    
    return str(retJSON)


    

def ParseMacroDict(macro):

    
    cmd = core.Command(macro["name"])
    
    for param in macro["parameters"]:
        cmd.addParameter(param["name"],param["value"])

    return cmd