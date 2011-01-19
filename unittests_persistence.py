import sys
import unittest
import treePattern as tp
import mongo
import config
import error
import core




class TestDBfunctions(unittest.TestCase):


    def setUp(self):
   
        self.shouldPrintVerbose = True

        self.shouldSave = False
        self.shouldPurge = False
        self.saveTrees = False
        
        self.testTreeID = config.rootTableCollectionName



    def test_readAllEvents(self):
        
        
        db = mongo.MongoDBComponents(config.dbIP,config.dbPort)
        allEvents = db.find_all(config.dbDefault, config.rootTableCollectionName)
        
        
        for ev in allEvents:
            print ev['location']['name']
            print ev['tableNumber']
            print list(ev['guests'])
            print "number of guests " + str(len(ev['guests']))
        
        
    def test_MongoDB_write(self):
        dsDict = {"id":core.Utils().getRandom()}

        mongo.newMongo(config).save(config.dbDefault,"A_TestCollection", dsDict)
        
    def test_MongoDB_readAll(self):
        db = mongo.MongoDBComponents(config.dbIP,config.dbPort)
        
        cols = db.listCollections()
        
        if( self.shouldPrintVerbose ):
            for col in cols:
                print col
          
    def test_MongoDB_dropCollection(self):
        import pymongo
        mongo.newMongo(config).dropCollection(config.dbDefault,"A_TestCollection")
        
        if(self.shouldPurge):
            mongo.newMongo(config).dropCollection(config.dbDefault,config.rootTableCollectionName)
        
        try:
            mongo.newMongo(config).dropCollection("db7","system.indexes")
        except pymongo.errors.OperationFailure:
            print "cannot delete system INDEXES!!!"



    def test_PrettyPrintMongoTree(self):
        mongoHelper, root = tp.targetMongo(config.dbDefault,"nodes.general",
                                     {'treeID':self.testTreeID, 'parent':None},
                                     config)
        
        print "\r\n"
        if self.shouldPrintVerbose:
            mongoHelper.printtree(root)


    def test_CreateAndDeleteCollections(self):
        collection = "tmpCollection"
        mongo.newMongo(config).save(config.dbDefault, collection, {} )
        mongo.newMongo(config).purgeCollection(config.dbDefault,collection)
        mongo.newMongo(config).dropCollection(config.dbDefault, collection)
        
        if self.shouldPurge == True:
            mongo.newMongo(config).dropCollection(config.dbDefault, "nodes.general")
     
    def test_MongoDB_addRootNode(self):


        try:
        
            mongoHelper, root = tp.targetMongo(config.dbDefault,"nodes.general",{'treeID':self.testTreeID, 'parent':None},config)

        except error.MongoDocNotFoundException:
            
            tn = tp.TreeNode("A",self.testTreeID)
            tn.addCommand("SumChildren")
            
            dtn = tn.ToDict()
            if self.shouldSave == True:
                mongo.newMongo(config).save(config.dbDefault,"nodes.general",dtn)
            #else:
            #   raise "unknown error {0}".format(list(sys.exec_info())
     

    

    def test_MongoDB_appendNode(self):
        
        mongoB, root = tp.targetMongo(config.dbDefault,"nodes.general",
                                     {'treeID':self.testTreeID, 'parent':None},
                                     config)

        if root != None and self.shouldSave == True:

            self.MakeTreeA(mongoB, root)
            
            print "tree created ..."
            
            
        else:
            print "no tree created"
            #raise error.MongoDocNotFoundException("no root node found for search term {0}".format(searchTerm))        

    def MakeTreeB(self, mongoB, root):
        B = tp.TreeNode("B", self.testTreeID)
        B.addCommand("CommandX")
    
        C = tp.TreeNode("C", self.testTreeID)
        C.addCommand("CommandX")
        
        mongoB.append(root, B)
        mongoB.append(root, C)


    def MakeTreeA(self, mongoB, root):
        B = tp.TreeNode("B ", self.testTreeID)
        B.addCommand("SumChildren")

        C = tp.TreeNode("C", self.testTreeID)
        C.addCommand("SumChildren")

        D = tp.TreeNode("D", self.testTreeID)
        D.addCommand("SumChildren")
        E = tp.TreeNode("E", self.testTreeID)

        E.addCommand("CommandX")
        F = tp.TreeNode("F", self.testTreeID)
        
        F.addCommand("CommandY")
        G = tp.TreeNode("G ", self.testTreeID)
        G.addCommand("SumChildren")

        H = tp.TreeNode("H", self.testTreeID)
        H.addCommand("SumChildren")

        I = tp.TreeNode("I", self.testTreeID)
        I.addCommand("CommandZ")
        
        J = tp.TreeNode("J", self.testTreeID)
        J.addCommand("CommandXY")
        c = mongoB.append(root, B)
        c2 = mongoB.append(c, C)
        mongoB.append(c, D)
        mongoB.append(c2, E)
        mongoB.append(c2, F)
        h = mongoB.append(mongoB.append(root, G), H)
        mongoB.append(h, I), mongoB.append(h, J)
        
   
        
if __name__ == '__main__':
    unittest.main()
        

