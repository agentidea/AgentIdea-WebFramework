#
# APACHE WSGI entry point
#

# $to do: REFACTOR !!! HORRIBLE TMP JOB ...

import json
from urllib import unquote_plus
#import core

import sys
sys.path.append('/var/wsgi/tafel/')

from src.framework.core import Utils
from src.framework.core import log
from src.framework.core import Framework as fwk
from src.framework.error import InvalidRequestMethod
from src.framework.core import Kontext
from src.framework.core import Itinerary


def application(environ, start_response):
    status = '200 OK'

    output = ""

    #SEED relatvie application root as well as Document Root?
    #documentRoot = environ['DOCUMENT_ROOT']

    if 'REQUEST_METHOD' in environ:
        if environ['REQUEST_METHOD'].upper() == 'POST':
            content_type = environ['CONTENT_TYPE'].lower()
            
            #application/x-www-form-urlencoded; charset=UTF-8
            if not 'application/x-www-form-urlencoded' in content_type:
            	 output += "content-type [{0}] not supported".format(content_type)
            else:
            	#Proper FORM POST 
                #retrieve the POST http://bit.ly/icvahV

		kontext = Kontext()
	    #kontext['src'] = 'index.wsgi'
		#kontext['referer'] = 'unknown'

		itinerary = Itinerary(kontext)

		post64 = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
		postClear = post64.decode('base64','strict')
		
		
		#referrer = "not yet implemented in WSGI ".encode('base64')

		itineraryDict = json.loads(postClear)
		itinerary = fwk().parseItinerayDict(itineraryDict)
		itinerary.set_KontextVal('script','index.wsgi')
		#itinerary.set_KontextVal('REFERER64',referrer)

		retEnvIT = fwk().processItinerary(itinerary)
		output = fwk().CommandsToJSON( retEnvIT.outCommands,retEnvIT.kontext )

		response_headers = [('Content-type', 'text/html'),
			('Content-Length',str(len(output)))]

		start_response(status, response_headers)
		return [str(output)] 
               
        else:
            output += "method [{0}] not supported".format(environ['REQUEST_METHOD'])
    
    #WAS NOT A POST, DISPLAY REASONABLE MESSAGE
    output += "<hr/>"
    output += "<pre style='font-size:6pt;'>"
    #output += core.ConvertDictToString(environ)
    output += "POST (application/x-www-form-urlencoded) FORM method only to this endpoint -- METHOD [%s] is UNSUPPORTED" %  environ['REQUEST_METHOD'].upper()
    output += "</pre>"


    response_headers = [('Content-type', 'text/html'),
        ('Content-Length',str(len(output)))]

    start_response(status, response_headers)

    return [output]














