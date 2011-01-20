"""

    set template inputs via .NET webservcice
    return template outputs
    
"""
import core
import config

import httplib
from xml.dom.minidom import parse, parseString


class TemplateSet(object):

    def parseResponse(self,fileResponse):
        #parse the response here
        xmltree = None
        
        try:
            xmltree = parse(fileResponse)
            #core.log("parsed xml")
            #respString = core.prettyPrint(xmltree)
            #core.log(respString)
            
        except:
            core.log("error parsing XML ? response XML???")
        
        lines = fileResponse.readlines()
        for line in lines:
            core.log(line)

        dataset = {}
#        dataset['outputs'] = self.getCellInfoFromXMLIST('outputs',xmltree)
#        dataset['sOutputs'] = self.getCellInfoFromXMLIST('sOutputs',xmltree)
        dataset['inputs'] = self.getCellInfoFromXMLIST('inputs',xmltree)
        dataset['outputs'] = self.getCellInfoFromXMLIST('outputs',xmltree)
        dataset['sOutputs'] = self.getCellInfoFromXMLIST('sOutputs',xmltree)
        dataset['sInputs'] = self.getCellInfoFromXMLIST('sInputs',xmltree)
        
        #core.log("finished creating OUTPUT and INPUT dataset")
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

    
    def setTemplateInputs(self,templateName,templatePath,templateInputList):
        

        SM_TEMPLATE = """
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <setTemplateInputs xmlns="http://smartorg.com/coreAPI/">
          <templateDir>%s</templateDir>
          <templateName>%s</templateName>
          <inputList></inputList>
        </setTemplateInputs>
      </soap:Body>
    </soap:Envelope>
    """

        
        SoapMessage = SM_TEMPLATE % (templatePath, templateName)
        xmlsoap = parseString(str(SoapMessage))
       
        #get the attach point for template inputs
        nl = xmlsoap.getElementsByTagName("inputList")
        inputListNode  = nl.item(0)
        
        for inputVal in templateInputList:
            tmpElement = xmlsoap.createElement("double")                    #create new <double> value </double> element
            tmpElement.appendChild( xmlsoap.createTextNode(str(inputVal)))  
            
            inputListNode.appendChild(tmpElement)
        
  
        FinalSOAPmessage = core.prettyPrint(xmlsoap).strip()
        

        #core.log("Posting to %s" % (config.HTTP_DESTINATION))
        #core.log("Posting SOAP REQUEST [%s]" % (FinalSOAPmessage))
        #core.log("Path [%s] TemplateName [%s]" % (templatePath,templateName))
        
        webservice = httplib.HTTP(config.HTTP_DESTINATION)
        #/Services/TemplateHelper.asmx 
        webservice.putrequest("POST",config.HTTP_PATH)
        webservice.putheader("Host",config.HTTP_DESTINATION)
        webservice.putheader("User-Agent","Serverside Python Originated Post")
        webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        webservice.putheader("Content-length", "%d" % len(FinalSOAPmessage))
        webservice.putheader("SOAPAction", "\"http://smartorg.com/coreAPI/setTemplateInputs\"")
        webservice.endheaders()
        webservice.send(FinalSOAPmessage)
        
        # get the response
        
        resp = None
        
        try:
            statuscode, statusmessage, header = webservice.getreply()
            if(statuscode != 200):
                core.log("HTTP ERROR %s %s" % (statuscode,statusmessage))
            else:
                resp = self.parseResponse(webservice.getfile())
        except:
            core.log("HTTP request to %s failed" % (config.HTTP_PATH))
            
        return resp
    
    

""" 
listInputs = ['100', '0.05', '45', '5', '30', '2010', '0.3', '0.1']
altInuts = [ 12, 0.05, 32, 8, 15, 2010, 0.3, 0.1]

dataset = TemplateSet().setTemplateInputs("testTemplate_v1.xls", config.TemplatePath,altInuts)

if(dataset != None):
    
    core.printList(dataset['outputs'])
    print ""
    core.printList(dataset['sOutputs'])
   
   
else:
    print "nothing to report"





  
"""
"""
        expected output for altInuts = [ 12, 0.05, 32, 8, 15, 2010, 0.3, 0.1]
        
      NPV  val    796.95593942291555    double
      totalVolumeSold         val    66.307575    double

"""
    

