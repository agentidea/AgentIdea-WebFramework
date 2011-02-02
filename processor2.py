from Http import *
import sys
import json
import time

#tafel
#to do: path append issues ...

sys.path.append("C:\inetpub\wwwroot\\net4\pyInetPub\\DieTafel\core\src\src")
sys.path.append("C:\inetpub\wwwroot\\net4\pyInetPub\\DieTafel\core\src\custom")
sys.path.append("C:\inetpub\wwwroot\\net4\pyInetPub\\DieTafel\core\src\framework")

import core

"""
       Windows IIS ISAPI pyISAPIe entry point
       FORM POST from XML-RPC interface to BASE64 encoded Macro requests
       expect call from XMLHTTP object in Firefox or MSXMLHTTP in IE
       application/x-www-form-urlencoded
"""


""" main request handler """


def Request():
    
    start = time.time()
    Header("Content-type: text/html")

    
    #$to do: check was a FORM application/x-www-form-urlencoded REQUEST
    #post data is base64 encoded
    post64 = Read()
    postClear = post64.decode('base64','strict')
 
    macroDict = json.loads(postClear)
    cmd = core.ParseMacroDict(macroDict)

    retEnv = core.processCommand(cmd)

    retJSON = retEnv.toJSON()
    end = time.time() - start

    Write( str(retJSON) )
    
    core.log("JSON SENT <<%s ... %s chars omitted>>]" % (str(retJSON)[0:300],(len(retJSON) -300) ))
    core.log(" Processing took %s seconds -------------------------------- \n \n" % (str(end)))

 


    
    