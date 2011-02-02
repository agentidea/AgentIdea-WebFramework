import unittest
import config
import core
import error
import coreCommands


class CommandTests(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_CreateTable(self):

        c = core.Command("CreateNewTable")
        c.addParameter("name","test table event")
        c.addParameter("collection","tables")
        c.addParameter("description","table at DeVinos")

        re = core.processCommand(c)
        
        self.assertEquals(re.commands[0].name,"Display")
        self.assertEquals(re.commands[0].params[0].name,"panel")
        self.assertEquals(re.commands[0].params[1].name,"html64")
        
        s = re.commands[0].params[1].val
        s = core.unpack(s)
        print s
         
   
        
  

  
        
        