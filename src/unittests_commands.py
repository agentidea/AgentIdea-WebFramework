import unittest
import config
import core
import error
import coreCommands
#import treePattern as tp

class CommandTests(unittest.TestCase):
    
    def setUp(self):
        #self.nodeToUse = '4d349e48f1e5841594000001'
    
    def test_CoreCommandDirectExecution(self):

        #call command directly

        s = "grant"
        c = core.Command("Ping")
        c.addParameter("name",s)
        
        cmd = coreCommands.cmdPing()
        re = cmd.executeCommand(c)
        
        self.assertEquals(re.commands[0].name,"ReturnCommand")
        self.assertEquals(re.commands[0].params[0].name,"echo")
        self.assertEquals(re.commands[0].params[0].val,s)
    
    def test_CallingShowList(self):

        c = core.Command("ShowList")
        c.addParameter("treeID",config.rootProjectTreeName)
        c.addParameter("collection","nodes.general")
        c.addParameter("panel","west")

        re = core.processCommand(c)
        
        self.assertEquals(re.commands[0].name,"Display")
        self.assertEquals(re.commands[0].params[0].name,"panel")
        self.assertEquals(re.commands[0].params[1].name,"html64")
        
        s = re.commands[0].params[1].val
        s = core.unpack(s)
        print s
         
    #@unittest.expectedFailure
    def test_CallingNonExistentCommand(self):
        #with self.assertRaises(error.CommandNotFoundException):
        try:
            
            c = core.Command("VeryUnlikelyCommandName77721")
            c.addParameter("collection","nodes.general")
            re = core.processCommand(c)
        except error.CommandNotFoundException:
            print "non-existent threw CommandNotFoundException"
         
   

   
        
  

  
        
        