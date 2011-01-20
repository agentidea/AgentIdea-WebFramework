"""

    gets template stuff from .NET webservcice
    
"""
import sys
import core
import config

import httplib
from xml.dom.minidom import parse


class TemplateInfo(object):
    

    def parseResponse(self,fileResponse):
        #parse the response here
        xmltree = None
        
        try:
            xmltree = parse(fileResponse)
            core.log("parsed xml")
            
            #print core.prettyPrint(xmltree)
            
        except:
            core.log("error parsing XML ? response XML???")
            
            lines = fileResponse.readlines()
            for line in lines:
                core.log(line)
            
            return None
        
        dataset = {}
        dataset['inputs'] = self.getCellInfoFromXMLIST('inputs',xmltree)
        dataset['outputs'] = self.getCellInfoFromXMLIST('outputs',xmltree)
        dataset['sOutputs'] = self.getCellInfoFromXMLIST('sOutputs',xmltree)
        dataset['sInputs'] = self.getCellInfoFromXMLIST('sInputs',xmltree)
        
        core.log("finished creating I/0 dataset")
        return dataset
               

       
    def getCellInfoFromXMLIST(self,rangeName,xmltree): 
        array = []
        for node1 in xmltree.getElementsByTagName(rangeName):
            for node2 in node1.childNodes:
                stuff = {}
                array.append(stuff)
                for tupNodes in node2.childNodes:
                    s = tupNodes.nodeName
                    tupTxt = tupNodes.firstChild.data
                    stuff[s] = tupTxt  
                    
        return array 
    
    


    def getTemplateIO(self,templateName,templatePath):
        #connect to webservice
        SM_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <GetTemplateDefinition xmlns="http://smartorg.com/coreAPI/">
          <templateDir>%s</templateDir>
          <templateName>%s</templateName>
        </GetTemplateDefinition>
      </soap:Body>
    </soap:Envelope>"""
    
        SoapMessage = SM_TEMPLATE % (templatePath, templateName)
        
        core.log("Posting to destination %s" % (config.HTTP_DESTINATION))
        #core.log("Posting SOAP REQUEST [%s] % (SoapMessage))
        core.log("Path [%s] TemplateName [%s]" % (templatePath,templateName))
        
        ret = None
        
        try:
                
            webservice = httplib.HTTP(config.HTTP_DESTINATION)
            #/Services/TemplateHelper.asmx 
            webservice.putrequest("POST",config.HTTP_PATH)
            webservice.putheader("Host",config.HTTP_DESTINATION)
            webservice.putheader("User-Agent","Serverside Python Originated Post")
            webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
            webservice.putheader("Content-length", "%d" % len(SoapMessage))
            webservice.putheader("SOAPAction", "\"http://smartorg.com/coreAPI/GetTemplateDefinition\"")
            webservice.endheaders()
            webservice.send(SoapMessage)
            
            # get the response
            statuscode, statusmessage, header = webservice.getreply()
            core.log("HTTP Response [%s] %s" % (statuscode,statusmessage))
            ret = self.parseResponse(webservice.getfile())
            
        except:
            core.log("ext webservice CALL failed %s" % (sys.exc_info()))
               
        return ret
    
    
    

"""

dataset = TemplateInfo().getTemplateIO("testTemplate_v1.xls", config.TemplatePath)
if(dataset != None):
    core.printList(dataset['inputs'])
    print ""
    core.printList(dataset['outputs'])
    print ""
    core.printList(dataset['sOutputs'])
    print ""
    core.printList(dataset['sInputs'])
else:
    print "nothing to report"



"""

