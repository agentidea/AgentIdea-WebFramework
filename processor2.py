from Http import *
import sys
import json
import time

#tafel
sys.path.append('C:\inetpub\wwwroot\\net4\pyInetPub\DieTafel\core\src')

import core

"""

       POST to XML-RPC interface to BASE64 encoded Macro requests
       expect call from XMLHTTP object in Firefox or MSXMLHTTP in IE
"""


""" main request handler """


def Request():
    
    start = time.time()
    Header("Content-type: text/html")

    #post data is base64 encoded
    post64 = Read()
    postClear = post64.decode('base64','strict')
 
    macroDict = json.loads(postClear)
    cmd = ParseMacroDict(macroDict)
    retEnv = core.processCommand(cmd)

    retJSON = retEnv.toJSON()
    
    end = time.time() - start

    Write( str(retJSON) )
    
    Log("JSON SENT <<%s>>]" % (str(retJSON)))
    Log(" Processing took %s seconds -------------------------------- \n \n" % (str(end)))

 
def ParseMacroDict(macro):
    #Log("parsing macro dictionary")
    
    """
    {"name":"GetInputs","paramCount":0,
    "parameters":[{"name":"template","value":"testTemplate_v1.xls"},{"name":"datasetID","value":"ds1"}],
    "UserCurrentTxID":"not_set_yet"}
    """
    
    cmd = core.Command(macro["name"])
    
    for param in macro["parameters"]:
        cmd.addParameter(param["name"],param["value"])

    return cmd

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

def Log(s):
    core.log(s)
 

    
    