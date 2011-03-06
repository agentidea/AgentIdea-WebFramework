from src.framework.core import User, Group, Utils
from src.config import info as config
from src.framework import mongo

def initializeUsersAndGroups():
    """ default system setup / initialization script """
    
    username = 'admin'
    password = 'smart'
    groupname = 'administrators'
    
    msgs = []
    
    userCollection = config.userCollection
    groupCollection = config.groupCollection
    
    pwdEncryped = Utils().md5encode(password)
    
    
    usr = mongo.MongoDBComponents(config.dbIP,config.dbPort).find_one(config.dbDefault, userCollection, {'username': username } )
    if usr:
        msgs.append( '%s user already setup - %s' % (username,usr['_id']))
    else:

        u = User(None, {'username':username,'password':pwdEncryped,'description':'base administrator account'})
        usrID = mongo.newMongo(config).save(config.dbDefault,userCollection, u)
        msgs.append( 'created new user %s with objectID %s' % (username,usrID))
        usr = mongo.MongoDBComponents(config.dbIP,config.dbPort).find_one(config.dbDefault, userCollection, {'username': username } )
    
    grp = mongo.MongoDBComponents(config.dbIP,config.dbPort).find_one(config.dbDefault, groupCollection, {'groupname': groupname } )
    if grp:
        msgs.append( '%s group already setup %s' % (groupname,grp['_id']))
    else:
        g = Group(None, {'groupname':groupname,'description':'admin group'})
        grpID = mongo.newMongo(config).save(config.dbDefault,groupCollection, g)
        msgs.append( 'created new group %s with objectID %s' % (groupname,grpID) )
        grp = mongo.MongoDBComponents(config.dbIP,config.dbPort).find_one(config.dbDefault, groupCollection, {'groupname': groupname } )

   
    
    if( usr['_id'] in grp['users']):
        msgs.append( 'user [%s] is already in group [%s]' % (username,groupname))
    else:
        
        grp['users'].append(usr['_id'])
        mongo.newMongo(config).save(config.dbDefault,groupCollection, grp)
        msgs.append( 'added user to group')
    
    return msgs
    
def setupSystem():
    return initializeUsersAndGroups()
       
        
if __name__ == '__main__':
    msgs = setupSystem()
    for msg in msgs:
        print msg        