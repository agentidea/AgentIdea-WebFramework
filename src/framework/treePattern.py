from src.framework import mongo
from src.framework.error import *
from src.config import info as config
      
class Visitor(object):
    def __init__(self):
        self.trajectory = []  
        self.compositeRoot = None   
        self.compositeLevels = 0
        self.HTML = ""


""" tree builder helper functions and objects"""
def targetMongo(dbName,collectionName,searchTerm,conf):

    targetNode = mongo.newMongo(conf).find_one(dbName, collectionName, searchTerm)
    if (targetNode == None):
        raise MongoDocNotFoundException("No MongoDB Node found at {0}/{1}/{2}".format(dbName, collectionName, searchTerm))
    mongoHelper = MongoTreeBuilder(conf, dbName, collectionName)
    return mongoHelper, targetNode


class MongoTreeBuilder(object):
    def __init__(self,conf,dbName,collectionName):
        self.conf = conf
        self.dbName = dbName
        self.collectionName = collectionName
        self.PRETTY_PRINT_SPACING = 2
    

    def getTreeAsLevels(self,node,totalLevels,level=1,visitor=None):
        
        if visitor == None: 
            visitor = Visitor()
            
            for i in range(totalLevels):
                visitor.trajectory.append([])
                

        #abs((level-(totalLevels -1)))        
        visitor.trajectory[level-1].append(node)
        
        s = ""
        for i in range(level*self.PRETTY_PRINT_SPACING):
            s = s + "    "
            
        #print "{0} <<{1}>> {2} ({3})".format(s,level,node["name"],node['_id'] )
        
        for childMNode in node['MNodes']:
            self.getTreeAsLevels(childMNode,totalLevels,level + 1,visitor)
            
        return visitor            
            
    def obtainPathToRoot(self,node,visitor=None):
        if(visitor == None): visitor = Visitor()
        visitor.trajectory.append(node)
        
        parent = node['parent']
       
        if(parent==None):
            return visitor
        else:
            searchTerm = {'_id':parent}
            p = mongo.newMongo(self.conf).find_one(self.dbName,self.collectionName,searchTerm)
            if(p != None):
                return self.obtainPathToRoot(p, visitor)
            else:
                raise MongoTreeCorruptException("Node [{0}] was not found".format(searchTerm))
                return visitor
    
    def getLeaves(self,node,level=1,visitor=None):

        if node == None:
            return None
        '''
        extract tree leaf nodes only
        ''' 
        #tree been built
        if visitor == None:
            visitor = Visitor()
            
        #visitor.trajectory.append(str(node['name']))   
            
        #print "{0} ({1}) {2}".format(s,level,node["name"] )
        
        if len(node['children']) > 0:
            for childID in node['children']:
                #recurse
                searchTerm = {'_id':childID}
                childNode = mongo.newMongo(self.conf).find_one(self.dbName,self.collectionName,searchTerm)
                self.getLeaves(childNode,level + 1,visitor)
        else:
            visitor.leaves.append( node['_id'] )
                
        return visitor
                   
    def loadComposite(self,node,level=1,visitor=None,parent=None):

        #build and load a dictionary style tree
         
        if visitor == None:
            visitor = Visitor()
            r = MNode(node)
            visitor.compositeRoot = r
            parent = r
        else:
            parent.appendChild(node) 
            parent = node

        if(level > visitor.compositeLevels): visitor.compositeLevels = level
        
        for childID in node['children']:
            
            searchTerm = {'_id':childID}
            childNode = mongo.newMongo(self.conf).find_one(self.dbName,self.collectionName,searchTerm)
            c = MNode(childNode)
            self.loadComposite(c,level + 1,visitor,parent)
                
        return visitor
        
    def append(self,parent,child,conf=None,dbName=None,collectionName=None):

        if conf == None:
            conf = self.conf
        if dbName == None:
            dbName = self.dbName
        if collectionName == None:
            collectionName = self.collectionName
        
        
        child['parent'] = parent['_id']
        child_id = mongo.newMongo(conf).save(dbName,collectionName,child.ToDict())
        parent['children'].append(child_id)
        mongo.newMongo(conf).save(dbName,collectionName,parent)
        
        child['_id'] = child_id
        return child
    
    
    def getAsHTML(self,node,level=1,visitor=None):
        
        if(visitor == None): visitor = Visitor()
        
        s = "\r\n <br/>"
        for i in range(level*self.PRETTY_PRINT_SPACING):
            s = s + "    "
        
        #$to do: remove panel position hard coding
        visitor.HTML = "{0}{1}{2}".format(visitor.HTML,s,node['name'])
        visitor.HTML = "{0} <span class='clsPlusMinus' onclick=\"FWK.say('DisplayInputScreen','{1}','{2}','center','{3}');\">+</span>".format(visitor.HTML,node['name'],node['_id'],config.rootProjectCollectionName)
        
        if node['MNodes'] != None and len(node['MNodes']) > 0:
            for childMNode in node['MNodes']:
                self.getAsHTML(childMNode,level + 1,visitor)
        #else:
            #leaf 
            #if 'data' in node and node['data'] != None:
            #    visitor.HTML = "{0} <span class='clsHyperlink' onclick=\"displayInputScreen('{1}','{2}','north','{3}');\">edit</span>".format(visitor.HTML,node['name'],node['_id'],config.rootProjectCollectionName)  
            #add leaf indicator
            #visitor.HTML = "{0} -|".format(visitor.HTML)
        
        
        
        return visitor
            
    def printMNodeTree(self,node,level=1):
        
        s = ""
        for i in range(level*self.PRETTY_PRINT_SPACING):
            s = s + "    "
            
        print "{0} ({1}) {2} ({3})".format(s,config.levels[level-1],node["name"],node['_id'] )
        
        '''
        if node['data'] != None:
            print "\t\t\t"
            print list(node['data'])
            print "\r\n\r\n"
        '''
        
        for childMNode in node['MNodes']:
            self.printMNodeTree(childMNode,level + 1)
        
    def printtree(self,node,level=1):

        s = ""
        for i in range(level*self.PRETTY_PRINT_SPACING):
            s = s + "    "
        try:    
            print "{0} ({1}) {2}".format(s,config.levels[level-1],node["name"] )
        except:
            print "error printing tree"
            return

        for childID in node['children']:
            searchTerm = {'_id':childID}
            childNode = mongo.newMongo(self.conf).find_one(self.dbName,self.collectionName,searchTerm)
            self.printtree(childNode,level + 1)
        
'''node used to create a composite object tree from mongo documents'''
class MNode(dict):
    def __init__(self,d):
        self['_id'] = d['_id']
        self['name'] = d['name']
        self['MNodes'] = []             #do not load here as sometimes just want a node with no children loaded
        self['treeID'] = d['treeID']
        
        if( 'parent' in d): self['parent'] = d['parent']
        if( 'children' in d): self['children'] = d['children'] # _id refs
        if( 'commands' in d): self['commands'] = d['commands']
        if( 'data' in d): self['data'] = d['data']

        
        
    def appendChild(self,child):
        self['MNodes'].append(child)
        
    def ToDict(self):
        return dict(self)
    
    def ToString(self):
        return str(self.ToDict())
    
    
    
''' node used to load mongo db '''
class TreeNode(dict):
    def __init__(self,_name,rootName=None,shouldSave=False,*args,**kw):
        
        self["parent"] = None
        self["children"] = []
        self["name"] = _name
        self['commands'] = []
        self['data'] = None

        ''' save data . sum nodes . tag entries '''
        ''' David's 3 kind of commands'''
        ''' local templates '''
        ''' aggregation templates '''
        ''' common PTS aggregate children ... parent EV '''

        if rootName != None:
            self["treeID"] = rootName
        
        
    def ToDict(self):
        return dict(self)
        
    def append_child(self, child):
        self["children"].append(child)
    
    def addCommand(self,commandName):
        self['commands'].append(commandName)
    
    '''syntactic sugar'''    
    def setParent(self,_id):
        self["parent"]=_id
        



        
'''classic design patter objects, added parent ref for backtracking    '''    
class Component(object):
    def __init__(self,_id, *args, **kw):
    
        #do nothing ... pass
        self.id = _id
        self.parent = None
 
    def component_function(self): pass
class Leaf(Component):
    def __init__(self, _id,*args, **kw):
        Component.__init__(self,_id, *args, **kw)
 
    def component_function(self):
        print "some LEAF {0} function!!!".format(str(self))
class Composite(Component):
    def __init__(self, _id,*args, **kw):
        Component.__init__(self,_id, *args, **kw)
        self.children = []
 
    def append_child(self, child):
        self.children.append(child)
        child.parent = self
 
    def remove_child(self, child):
        self.children.remove(child)
 
    def component_function(self):
        map(lambda x: x.component_function(), self.children)        