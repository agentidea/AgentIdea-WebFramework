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
from urlparse import urlparse

#to do: path append issues ...
sys.path.append("C:\inetpub\wwwroot\\net4\pyInetPub\\DieTafel\core\src")

from src.framework.core import Utils
from src.framework.core import log
from src.framework.core import Framework as fwk
from src.framework.error import InvalidRequestMethod
from src.framework.core import Kontext
from src.framework.core import Itinerary





""" main http request handler """
def Request():
    
    start = time.time()
    Header("Content-type: text/html")

    if Env.REQUEST_METHOD != "POST":
        raise InvalidRequestMethod(Env.REQUEST_METHOD + " not supported")
    
    """pass http header - Context"""
    """look at headers"""
    #parse request headers into a dictionary
    headers_in  = dict((N.upper(), V) for N, V in [Item.split(':',1) for Item in Env.ALL_RAW.split('\n') if Item])
    #log(Utils().ConvertDictToString(headers_in))

    referrer = ""
    if( 'REFERER' in headers_in ):
        referrer = Utils().pack(headers_in['REFERER'])

    
    #$to do: check was a FORM application/x-www-form-urlencoded REQUEST
    #post data is base64 encoded
    
    
    post64 = Read()
    postClear = post64.decode('base64','strict')
 
    itineraryDict = json.loads(postClear)
    itinerary = fwk().parseItinerayDict(itineraryDict)
    itinerary.set_KontextVal('script','processor2.py')
    itinerary.set_KontextVal('REFERER64',referrer)
    
    retEnvIT = fwk().processItinerary(itinerary)
    retJSON = fwk().CommandsToJSON( retEnvIT.outCommands,retEnvIT.kontext )

    Write( str(retJSON) )
    
    end = time.time() - start

    log("JSON SENT <<%s>>]" % (str(retJSON)))
    # log("JSON SENT <<%s ... %s chars omitted>>]" % (str(retJSON)[0:300],(len(retJSON) -300) ))
    log(" Processing took %s seconds -------------------------------- \n \n" % (str(end)))

 


    
    