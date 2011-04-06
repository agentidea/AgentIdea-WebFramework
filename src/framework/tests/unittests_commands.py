import unittest

from src.framework.core import log, Utils, Command, Kontext
from src.framework.core import Framework as fwk
from src.framework.core import Itinerary
from src.config import info


class CommandsUnitTests(unittest.TestCase):


     
    
    def test_Ping(self):
            
            kontext = Kontext()
            kontext['REFERER'] = 'From a UNIT TEST'
            
            c = Command("Ping")
            c.addParameter("name",u"echo")
            c.addParameter("age",44)
    
            it = Itinerary(kontext)
            it.addInCommand(c)
            it = fwk().processItinerary(it)
            
            retJSON = fwk().CommandsToJSON(it.outCommands,it.kontext)
            print retJSON
            
    def test_ShowNavigation(self):
            
            kontext = Kontext()
            kontext['REFERER'] = 'From a UNIT TEST'
            
            c = Command("ShowNavigation")
            c.addParameter("panel",u"west")
            
    
            it = Itinerary(kontext)
            it.addInCommand(c)
            it = fwk().processItinerary(it)
            
            retJSON = fwk().CommandsToJSON(it.outCommands,it.kontext)
            print retJSON
            
    def test_ShowToc(self):
            
            kontext = Kontext()
            kontext['REFERER'] = 'From a UNIT TEST'
            
            c = Command("ShowToc")
            c.addParameter("panel",u"west")
            c.addParameter("what","admin")
            c.addParameter("orientation","vertical")
    
            it = Itinerary(kontext)
            it.addInCommand(c)
            it = fwk().processItinerary(it)
            
            retJSON = fwk().CommandsToJSON(it.outCommands,it.kontext)
            print retJSON
            
    def test_CommandsReflect(self):
           
            kontext = Kontext()
            kontext['REFERER'] = 'From a UNIT TEST'
            
            c = Command("CommandsReflect")
            c.addParameter("panel",u"west")
           
    
            it = Itinerary(kontext)
            it.addInCommand(c)
            it = fwk().processItinerary(it)
            
            retJSON = fwk().CommandsToJSON(it.outCommands,it.kontext)
            print retJSON
           
   
        

    
      
if __name__ == '__main__':
    unittest.main()
        

