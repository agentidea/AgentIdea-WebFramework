import unittest

from src.framework.core import log, Utils, Command, Kontext
from src.framework.core import Framework as fwk
from src.framework.core import Itinerary
from src.config import info


class TestCoreComponents(unittest.TestCase):
    
    def setUp(self):
        self.seq = range(10)
        self.shouldPrintVerbose = False
    
    def test_utilsTimestamp(self):
        ts = Utils().Timestamp()
        print "ute.Timestamp() was {0}".format( str(ts) )

    def test_info(self):
        dict = {}
        if self.shouldPrintVerbose:
            Utils().reflectInfo(dict)
     
    def test_log(self):
        log("this is a test of the core logging system")
        print "testing log {0}".format(info.LogFile)
    
    def test_badLogPath(self):
        origLogPath = info.LogPath 
        #$to do: illustrates why log path should be a immutable tuple()
        info.LogPath = """z:\yellowBrickRoad"""
        self.assertRaises(Exception,log,"where is the wicked witch of the east?")
        info.LogPath = origLogPath
         
    def test_info2(self):
        dict = {'king':77}
        fxn = lambda x: x*2
        
        if self.shouldPrintVerbose:
            Utils().interrogate(dict)
            print "____"
            Utils().interrogate(fxn)
              
    def test_peekAtLog(self):
        if self.shouldPrintVerbose:
            s = Utils().tail(info.LogFile,25)
            print s
    
    def test_nav(self):
        nav = info.nav
        print "Nav elements\r\n"
        for n in nav:
            print n['name'] + " : "  + n['A']
            print "---"

    def test_dictToString(self):
        d ={'name':'Grant','age':43}
        print Utils().ConvertDictToString(d)


    def test_commandCreation(self):
        c = Command("testCommand")
        c.addParameter("name","grant")
        c.addParameter("age",43)
       
        
        print c.JSON
        
        #print "onload JavaScript [%s][%s]" % (c.onload_JScript.decode('base64','strict'),c.onload_JScript)
        #print "onblur JavaScript [%s][%s]" % (c.onblur_JScript.decode('base64','strict'),c.onblur_JScript)



    def test_CallingPing(self):
        name = "babu"
        c = Command("Ping")
        c.addParameter("name",name)
       
        kontext = Kontext()
        kontext.setKeyValue("user", "grant")
        itinerary = Itinerary(kontext)
        itinerary.addInCommand(c)
        
        re = fwk().processItinerary(itinerary)
        
        self.assertEquals(re.outCommands[0].name,"ReturnCommand")
        self.assertEquals(re.outCommands[0].params[0].name,"echo")
        self.assertEquals(re.outCommands[0].params[0].val,name)
        
    def test_CallingPingContextual(self):
        
        kontext = Kontext()
        kontext['REFERER'] = 'From a UNIT TEST'
        
        c = Command("Ping")
        c.addParameter("name","echo")

        
        
        it = Itinerary(kontext)
        it.addInCommand(c)
        it = fwk().processItinerary(it)
        
        retJSON = fwk().CommandsToJSON(it.outCommands,it.kontext)
        print retJSON
        

    def test_newGroup(self):
        from src.framework.core import Group
        g = Group(None, {'groupname':'test','description':'new group for testing','users':['tom','dick','harry']})
        
        print type(g)
        print dir(g)
        print g['users']
        
    def test_newUser(self):
        from src.framework.core import User
        u = User(None, {'username':'naam','description':'new user for testing','password':'babu'})
        
        print type(u)
        print dir(u)
    
        
        
        
        
      
if __name__ == '__main__':
    unittest.main()
        
    