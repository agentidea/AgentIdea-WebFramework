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
    cmd = core.ParseMacroDict(macroDict)
    retEnv = core.processCommand(cmd)

    retJSON = retEnv.toJSON()
    end = time.time() - start

    Write( str(retJSON) )
    
    core.log("JSON SENT <<%s>>]" % (str(retJSON)))
    core.log(" Processing took %s seconds -------------------------------- \n \n" % (str(end)))

 


    
    