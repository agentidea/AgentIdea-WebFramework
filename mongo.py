import pymongo
import error

def newMongo(config):
    return MongoDBComponents(config.dbIP,config.dbPort)



class MongoDBComponents(object):
    
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        # if null set to config.dbIP, config.dbPort???
     
     
    def getConnection(self):
        con = None
        try:
            con = pymongo.Connection(self.ip,self.port)
        except pymongo.errors.OperationFailure as opfex:
            raise error.MongoInstanceException(opfex)
        except:
            raise error.MongoConnectionException("unable to connect to MongoDB instance on tcp://{0}:{1}".format(self.ip,self.port))
        return con
       
    def save(self,db_id,collection_id,content):
        connection = self.getConnection()
        db = connection[db_id]
        return db[collection_id].save(content)
    
    def purgeCollection(self,db_id,collection_id):
        connection = self.getConnection()
        db = connection[db_id]
        db[collection_id].remove()
        
    def dropCollection(self,db_id,collection_id):
        connection = self.getConnection()
        db = connection[db_id]
        db.drop_collection(collection_id)
    
    def find_all(self,db_id,collection_id):
        connection = self.getConnection()
        db = connection[db_id]
        cursorFound = db[collection_id].find()
        #numItems = len(items)
        return cursorFound
        
        
    def find_one(self,db_id,collection_id,searchStructure):
        connection = self.getConnection()
        db = connection[db_id]
        item = db[collection_id].find_one(searchStructure)
        #$to_do: throw exception if not found?
        return item
    
    def listCollections(self):
        connection = self.getConnection()
        list = []
        db_names  = connection.database_names()

        '''enumerate db's and collections'''
        for name in db_names:
            db = connection[name]
            
            cols = db.collection_names()
    
            for col in cols:
                list.append("db {0} collection called {1}\r\n".format(name,col))

                #what docs ???
                for q in db[col].find():
                    list.append("\t DOC {0}\r\n".format(str(q))) 

        return list
    
    



            
        
    
    