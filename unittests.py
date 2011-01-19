import unittest
import core
import config


class TestIOfunctions(unittest.TestCase):
    
    def setUp(self):
        self.seq = range(10)
        
    def test_log(self):
        core.log("this is a test of the core logging system")
        print "testing log {0}".format(config.LogFile)
    
    def test_commands(self):
        c = core.Command("testCommand")
        c.addParameter("name","grant")
        c.addParameter("age",43)
        #c.onload_JScript = "//add onCommandLoad JavaScript here".encode('base64','strict')
        #c.onblur_JScript = "//add onCommandUnload JavaScript here".encode('base64','strict')
        
        print c.JSON
        
        print "onload JavaScript [%s][%s]" % (c.onload_JScript.decode('base64','strict'),c.onload_JScript)
        print "onblur JavaScript [%s][%s]" % (c.onblur_JScript.decode('base64','strict'),c.onblur_JScript)

    
    def test_paths(self):
        import sys
        paths = sys.path
        #for pth in paths:
            #print pth
        
        
if __name__ == '__main__':
    unittest.main()
        
    