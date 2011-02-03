import unittest
from src.framework.core import log, Utils, Command, Framework
from src.config import info

class DomainCommandTests(unittest.TestCase):
  
    def test_Ping(self):
        passed = "Gandalf"
        c = Command("Ping")
        c.addParameter("name",passed)
        re = Framework().processCommand(c,info.commandDomainTuple)
        self.assertEquals(re.commands[0].name,"ReturnCommand")
        s = re.commands[0].params[0].val
        self.assertEquals(s,passed)     
        
    
    def test_SaveNewTableEvent(self):  
        table = {}
        c = Command("SaveNewEvent")
        
        #c.addParameter("table64",table64)
        #re = Framework().processCommand(c,info.commandDomainTuple)
        
    def test_ShowEvents(self):
        c = Command("ShowEvents")
        c.addParameter("panel",'west')
        re = Framework().processCommand(c, info.commandDomainTuple)
        
        print "returned command [%s] had %s parameters" % (re.commands[0].name,len(re.commands[0].params))
   
        
  

  
        
        