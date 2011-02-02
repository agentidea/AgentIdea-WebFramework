import unittest
import core
import config


class TestCoreComponents(unittest.TestCase):
    
    def setUp(self):
        self.seq = range(10)
        self.shouldPrintVerbose = False
    
  
    def test_info(self):
        dict = {}
        if self.shouldPrintVerbose:
            core.info(dict)
     
    def test_nav(self):
        nav = config.nav
        print "Nav elements"
        for n in nav:
            print n['name'] + " : "  + n['A']
        print "---"
           
    def test_dictToString(self):
        d ={'name':'Grant','age':43}
        
        print core.ConvertDictToString(d)

    def test_badLogPath(self):
        origLogPath = config.LogPath 
        config.LogPath = """z:\yellowBrickRoad"""
        self.assertRaises(Exception,core.log,"where is the wicked witch of the east?")
        #core.log("Where is the wicked witch of the east")
        config.LogPath = origLogPath
    
    def test_utilsTimestamp(self):
        ute = core.Utils()
        ts = ute.Timestamp()
        print "ute.Timestamp() was {0}".format( str(ts) )
        
        
    def test_log(self):
        core.log("this is a test of the core logging system")
        print "testing log {0}".format(config.LogFile)
        
        
    def test_composite(self):
        import treePattern as tp
        id = 619
        c = tp.Composite(id)
        l = tp.Leaf(2)
        l_two = tp.Leaf(3)
        
        c.append_child(l)
        c.append_child(l_two)
        
        c.component_function()

    def test_addNode(self):
        tR = core.TreeNode_v1(1)
        t2 = core.TreeNode_v1(2)
        t3 = core.TreeNode_v1(3)
        t4 = core.TreeNode_v1(4)
        t5 = core.TreeNode_v1(5)
        t6 = core.TreeNode_v1(6)
        
        tR.addNode(t2)
        tR.addNode(t3)
        t3.addNode(t4)
        t3.addNode(t5)
        t5.addNode(t6)
        
        
        
        x = tR.children.__len__()
        print "tree created with {0} root children".format(x)
        
    
    def test_commands(self):
        c = core.Command("testCommand")
        c.addParameter("name","grant")
        c.addParameter("age",43)
        #c.onload_JScript = "//add onCommandLoad JavaScript here".encode('base64','strict')
        #c.onblur_JScript = "//add onCommandUnload JavaScript here".encode('base64','strict')
        
        print c.JSON
        
        print "onload JavaScript [%s][%s]" % (c.onload_JScript.decode('base64','strict'),c.onload_JScript)
        print "onblur JavaScript [%s][%s]" % (c.onblur_JScript.decode('base64','strict'),c.onblur_JScript)

    
    """
    def test_paths(self):
        import sys
        paths = sys.path
        #for pth in paths:
            #print pth
    """
        
if __name__ == '__main__':
    unittest.main()
        
    