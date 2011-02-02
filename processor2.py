"""
       Windows IIS ISAPI pyISAPIe entry point
       FORM POST from XML-RPC interface to BASE64 encoded Macro requests
       expect call from XMLHTTP object in Firefox or MSXMLHTTP in IE
       application/x-www-form-urlencoded
"""

from Http import *
import sys
import json
import time

#to do: path append issues ...
sys.path.append("C:\inetpub\wwwroot\\net4\pyInetPub\\DieTafel\core\src")

from src.framework.core import Utils
from src.framework.core import log
from src.framework.core import Framework as fwk
#from src.framework.core import ReturnEnvelope




""" main http request handler """
def Request():
    
    start = time.time()
    Header("Content-type: text/html")

    
    #$to do: check was a FORM application/x-www-form-urlencoded REQUEST
    #post data is base64 encoded
    post64 = Read()
    postClear = post64.decode('base64','strict')
 
    macroDict = json.loads(postClear)
   
    cmd = fwk().ParseMacroDict(macroDict)

    retEnv = fwk().processCommand(cmd)

    retJSON = retEnv.toJSON()
    end = time.time() - start

    Write( str(retJSON) )
    
    log("JSON SENT <<%s ... %s chars omitted>>]" % (str(retJSON)[0:300],(len(retJSON) -300) ))
    log(" Processing took %s seconds -------------------------------- \n \n" % (str(end)))

 


    
    