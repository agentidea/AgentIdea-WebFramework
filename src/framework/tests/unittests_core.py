import unittest

from src.framework.core import log, Utils, Command
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


    def test_mailer(self):
        from src.framework.mail import message,postMan
        
        msg = message('g@agentidea.com','grantsteinfeld@gmail.com','test','body of message')
        po = postMan()
        po.sendMail(msg)
        
        
        
        
      
if __name__ == '__main__':
    unittest.main()
        
    