import sys
import unittest

from src.framework.core import log, Utils, Command, Kontext
from src.framework.core import Framework as fwk
from src.config import info as config
from src.framework import  treePattern as tp
from src.framework import mongo
from src.framework.error import *
from pymongo.objectid import ObjectId

class MongoUnitTests(unittest.TestCase):


    def setUp(self):
        self.shouldPrintVerbose = True
        self.shouldPurgeAll = True
        self.shouldDropAll = False
        
    
#    def test_MongoDB_write(self):
#        dsDict = {"id":Utils().getRandom()}
#        mongo.newMongo(config).save(config.dbDefault,"A_TestCollection", dsDict)

    def test_MongoDB_readAll(self):
        db = mongo.MongoDBComponents(config.dbIP,config.dbPort)
        cols = db.listCollections()
        
        if( self.shouldPrintVerbose ):
            for col in cols:
                print col        

    
    
    def test_purgeAllCollections(self):
        if self.shouldPurgeAll :
            db = mongo.MongoDBComponents(config.dbIP,config.dbPort)
            res = db.purgeAllCollections(config.dbDefault)
            print str(res)
            
    
    def test_dropAllCollections(self):
        if self.shouldDropAll :
            db = mongo.MongoDBComponents(config.dbIP,config.dbPort)
            db.dropAllCollections(config.dbDefault)
   
        

    
      
if __name__ == '__main__':
    unittest.main()
        

