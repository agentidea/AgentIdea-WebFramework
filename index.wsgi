#
# APACHE WSGI entry point ... rename to index.wsgi
#

# REFACTOR !!! HORRIBLE TMP JOB ...

import json
from urllib import unquote_plus
import core


def application(environ, start_response):
    status = '200 OK'

    output = ""

    # SEED relatvie application root as well as Document Root?
    #documentRoot = environ['DOCUMENT_ROOT']

    if 'REQUEST_METHOD' in environ:
        if environ['REQUEST_METHOD'].upper() == 'POST':
            content_type = environ['CONTENT_TYPE']
            if content_type.lower() == 'application/x-www-form-urlencoded':
                # was really a FORM POST 
                #retrieve the POST http://bit.ly/icvahV
                post64 = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
                postClear = post64.decode('base64','strict')
                macroDict = json.loads(postClear)
                cmd = core.ParseMacroDict(macroDict)
                retEnv = core.processCommand(cmd)

                output = retEnv.toJSON()
                response_headers = [('Content-type', 'text/html'),
                            ('Content-Length',str(len(output)))]

                start_response(status, response_headers)
                return [str(output)] 


            else:
                output += "content-type [{0}] not supported".format(content_type)
        else:
            output += "method [{0}] not supported".format(environ['REQUEST_METHOD'])
    
    #WAS NOT A POST, DISPLAY REASONABLE MESSAGE
    output += "<hr/>"
    output += "<pre style='font-size:6pt;'>"
    #output += core.ConvertDictToString(environ)
    output += "</pre>"


    ute = core.Utils()
    ts = ute.Timestamp()
    output += "<div style='color:red;'>timestamp on server was {0}</div>".format(str(ts))
    response_headers = [('Content-type', 'text/html'),
        ('Content-Length',str(len(output)))]

    start_response(status, response_headers)

    return [output]














