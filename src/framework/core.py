import sys
import os
import error
import hashlib

from src.config import info
from src.framework import mongo
from src.framework.error import *

def log(s):

    import os.path 
    
    logfile = None
    
    dt = Utils().Timestamp()
    
    
    if not os.path.exists(info.LogPath): 
        try:
            os.makedirs(info.LogPath)
        except:
            print "Unexpected dir creation error:" % list(sys.exc_info())
            raise
             
      
    if( os.path.isfile(info.LogFile) == False ):
        try:
            """new file, open for writing"""  
            logfile = open(info.LogFile,'w') 
        except IOError as (errno, strerror):
            print "I/O error W ({0}): {1}".format(errno, strerror)
            return
        except:
            print "Unexpected file open W error: %s" % list(sys.exc_info())
            return
    else:
        try:
            """existing log, open for appending"""
            logfile = open(info.LogFile,'a') 
        except IOError as (errno, strerror):
            print "I/O error A({0}): {1}".format(errno, strerror)
            return
        except:
            print "Unexpected file open A error: %s" % list(sys.exc_info())
            return


        logfile.write(str(dt))
        logfile.write(" :: ")
        logfile.write(str(s))
        logfile.write('\n')
        logfile.close()
        
    return str(dt)


class UserHelper(object):
    """ responsible for managing users and groups """
    def allUsers(self):
        """retrieve all users"""
        
        db = mongo.MongoDBComponents(info.dbIP,info.dbPort)
        return db.find_all(info.dbDefault, info.userCollection)
        
    def passwd(self,username,oldpassword,newpassword,newpasswordConfirm):
       
        if(newpassword != newpasswordConfirm):
            raise NewPasswordMismatchException("passwords did not match")
        
        usr = mongo.MongoDBComponents(info.dbIP,info.dbPort).find_one(info.dbDefault, info.userCollection, {'username': username } )
        
        if(oldpassword != usr['password']):
            raise OldPasswordMismatchException("old password was incorrect")
        
        
        usr['password'] = newpassword
        mongo.newMongo(info).save(info.dbDefault,info.userCollection, usr)
        
        return "password changed"
        
      


class Framework(object):
    
    def intializeSystem(self,conf):
        """ if db is specified, and has no users ( + other cirteria? )
        intializeSystem adds persistent aspects, like users and groups"""
        
        if info.dbIP:
            #system uses db, self provision if need be
            countUsers = int(UserHelper().allUsers().count());
            if(countUsers == 0):
                from src.framework import systemInit
                #add default user and groups
                systemInit.initializeUsersAndGroups()
                
                log("************************************************************")
                log("intializeSystem() -%s- users and groups " % (conf.appName))
                log("************************************************************")
                
                
    def validateCommand(self,command,macro):
        """validate command off it's specification valid spec = {} """
        if("spec" in dir(command)):
            if( command.spec['name'] != macro.name):
                raise error.CommandNotFoundException("incorrect name expected {0}".format() )
            else:
                #check parameters
                params = command.spec['params']
                
                passedParamCount = len(macro.params)
                expectedParamCount = len(params)
                
                if( passedParamCount > expectedParamCount):
                    raise error.WrongNumberParametersException("passed in %s expected %s" % (passedParamCount,expectedParamCount ))
                
                for param in params:
                    req = param['req']
                    nme = param['name']
                    
                    #was there a requirement constraint?
                    if(req ==1):
                        # this parameter is required
                        if( macro.hasNameValue( nme ) == 1 and macro.getValue( nme ) != ""):
                            #good
                            log("required value for %s was passed as %s" % (nme,macro.getValue( nme )))
                        else:
                            raise error.RequiredParameterMissingException("Required Parameter '%s' not passed" % (nme))
                    
                    #was a value passed?   
                    valPassed = macro.getValue(nme)
                    
                    #apply default values to values not passed
                    if(valPassed == None):
                        if('defaultVal' in param):
                            if('vals' in param):
                                try:
                                    valPassed = param['vals'][int(param['defaultVal'])]
                                except Exception:
                                    raise error.InvalidCommandSpecificationException("defaultVal is 0 based index into the vals list.")
                            else:
                                raise error.InvalidCommandSpecificationException("a default parameter needs a vals list with at least one value")
                    else:
                        # a value was passed
                        #was there a type constraint
                        if('type' in param):
                            sType = type(valPassed).__name__
                            if( sType == param['type']):
                                log("type check passed %s " % sType)
                            else:
                                raise error.InvalidParameterTypeException("Invalid parameter type %s for parameter called %s" % ( sType,nme))
                    

                        #was there a value constraint
                        if('vals' in param):
                            #check if parameter value matches one of these
                            if(valPassed in param['vals']):
                                #do nothing
                                log("good value")
                            else:
                                raise error.UnexpectedParameterException("Param Name '{0}' with Value '{1}' did not match one of the required possible values [{2}]".format(nme,valPassed,str(list(param['vals']))))

                return True
        else:
            raise error.MissingCommandSpecificationException("this command needs a specification")

        return False
        
        
                   
    def processItinerary(self,itinerary,commandTuple = None):
        """processes the commands in the itinerary"""
        for cmd in itinerary.inCommands:
            self.__processCommand( cmd.set_itinerary(itinerary), commandTuple )
        return itinerary
    
    def __processCommand(self,cmd,commandCoreTuple = None):
        """ processess a Command dynamically """
        moduleID = None
        klassID = None
        
        if(commandCoreTuple == None):
            moduleID = info.commandCoreTuple[0]
            klassID =  info.commandCoreTuple[1] + cmd.name
        else:
            moduleID = commandCoreTuple[0]
            klassID =  commandCoreTuple[1] + cmd.name

        try:
            c = self.LoadClass(moduleID,klassID)   
            log("core") 
        except error.CommandNotFoundException:
            #$to do: refactor more elegantly?  dir() on module to see if contains command?
            #command not found in core, look in domain tuple command file
            moduleID = info.commandDomainTuple[0]
            klassID = info.commandDomainTuple[1] + cmd.name
            c = self.LoadClass(moduleID,klassID)
            log("custom")
        except:
            log("Error loading %s %s" % (klassID,list(sys.exc_info())))
            raise
        
        try:
            
            """determine if command can be run"""

            log("looking up meta for command %s " % (cmd.name))
            
            if 'kreds' in cmd.kontext:
                kreds = cmd.kontext['kreds']
                clearKreds = Utils().unpack(kreds)
                kredBits = clearKreds.split('_')
                log(" pre execution kreds %s %s " % (kredBits[0],kredBits[1]))
            
            
            """validate command if spec is present"""
            
            if('spec' in dir(c)):
                if(self.validateCommand(c, cmd)):
                    c.executeCommand(cmd)
                    log("EXECUTE {0}".format(cmd.name))
            else:
                c.executeCommand(cmd)
                log("EXECUTE {0}".format(cmd.name))
        except:
            tupList = sys.exc_info()
            
            log("Error EXECUTE command %s %s" % (klassID,list(tupList)))
            raise
            
        
    
    def LoadClass(self,moduleID,klassID):
        
        actualClass = None
        try:
            mod = __import__(moduleID, globals(), locals(), [klassID]) 
            klass = getattr(mod, klassID) 
            actualClass = klass()
        except AttributeError as ae:
            logMsg = "{0} {1}".format(moduleID,klassID)
            raise error.CommandNotFoundException(logMsg)
        except:
            log("Error loading %s %s" % (klassID,list(sys.exc_info())))
            raise
        
        return actualClass
        
        
        
        
        
    def ParseMacroDict(self,macro):
        cmd = Command(macro['name'])
        for param in macro['parameters']:
            cmd.addParameter(param['name'], param['value'])
        return cmd
    
    def parseItinerayDict(self,itinerary):
        it = Itinerary(itinerary['kontext'])
        for macro in itinerary['inCommands']:
            cmd = self.ParseMacroDict(macro)
            it.addInCommand(cmd)
        return it
    

    def CommandsToJSON(self,commandList,kontext):
        """takes a list of commands and creates JSON repreentation"""
        
        json = "{"
        json += " 'commands': ["
        
        for cmd in commandList:
            json += cmd.toJSON()
            json += ","
            
        json = json[:-1]
        json += "]"
        json += ","
        
        json += "'context':{"
        
        if(kontext):
            for k in kontext:
                if(k=='key'): 
                    continue
                
                json += "'{0}':'{1}',".format(k, kontext[k] )
            json = json[:-1]
            
        json += "}"
        
        
        
        
        json += "}"
        return json
            
        

class Utils(object):
    def reflectInfo(self,object, spacing=10, collapse=1):
        """Print methods and doc strings.
        
        Takes module, class, list, dictionary, or string."""
        methodList = [e for e in dir(object) if callable(getattr(object, e))]
        processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
        print "\n".join(["%s %s" %
                         (method.ljust(spacing),
                          processFunc(str(getattr(object, method).__doc__)))
                         for method in methodList])
        
    def interrogate(self,item):
        """Print useful information about item."""
        if hasattr(item, '__name__'):
            print "NAME:    ", item.__name__
        if hasattr(item, '__class__'):
            print "CLASS:   ", item.__class__.__name__
        print "ID:      ", id(item)
        print "TYPE:    ", type(item)
        print "VALUE:   ", repr(item)
        print "CALLABLE:",
        if callable(item):
            print "Yes"
        else:
            print "No"
            
        if hasattr(item, '__doc__'):
            doc = getattr(item, '__doc__')
            
            if hasattr(doc,'strip'):
                doc = doc.strip()   # Remove leading/trailing whitespace.
                firstline = doc.split('\n')[0]
                print "DOC:     ", firstline

        
    def ConvertDictToString(self,d):
        #from pprint import pprint 
        #pprint(d)
        return ''.join(["'%s':%s\r\n" % item for item in d.iteritems()])

    prettyPrint = lambda self, dom: '\n'.join([line for line in dom.toprettyxml(indent=' '*2).split('\n') if line.strip()])

    def Ping(self,n):
        return n /3
     
    def md5encode(self,plain):
        m = hashlib.md5()
        m.update(plain)
        return m.hexdigest()
    
    def getRandom(self):
        import random
        return random.random()   
        
    def Timestamp(self):
        import datetime
        d = datetime.datetime.now()
        #return '{:%Y-%m-%d %H:%M:%S}'.format(d)
        return d
    
    def printList(self,list):
        for item in list:
            print item
     
        
    
    
    def pack(self,what):
        import urllib
        s = what.encode('base64','strict')
        return urllib.quote(s)
    
    def unpack(self,what):
        import urllib
        s = urllib.unquote(what)
        return s.decode('base64','strict')
    
    def tail(self,filepath, nol=10):
        f = open(filepath, 'rU')    # U is to open it with Universal newline support 
        allLines = f.readlines()
        f.close()
        ret = "\r\n".join(allLines[-nol:])
        return ret
    
    def removeFile(self,filePath):
        os.remove(filePath)
        
class Kontext(dict):
    """context dictionary"""
    def setKeyValue(self,key,value):
        self[key] = value
        return self
    
    def getKeyValue(self,key):
        return self[key]
    
    def KeyExists(self,key):
        if( key in self):
            return True
        else:
            return False
        
    
    
class Command(object):
    def __init__(self, commandName):
        self._name = commandName
        self._parameterList = []
        self._preScript = info.onCommandLoad64
        self._postScript = info.onCommandUnload64
        self._kontext = None
        self._itinerary = None
        self._outCommands = None
        
    def get_name(self):
        return self._name
    
    def set_itinerary(self,itinerary):
        """reference to the itenerary """
        self._itinerary = itinerary
        self._kontext = itinerary.kontext
        self._outCommands = itinerary.outCommands
        return self
    
    def get_kontext(self):
        """get a reference to the kontext dictionary"""
        return self._kontext
    def get_itinerary(self):
        """get a reference to the itinerary dictionary"""
        return self._itinerary
    
    def get_outCommands(self):
        return self._outCommands
    
    kontext = property(get_kontext) 
    itinerary = property(get_itinerary)
    outCommands = property(get_outCommands)
    
      
    def get_params(self):
        return self._parameterList
    
    
    def hasNameValue(self,key):
        
        for param in self.params:
            if param.name == key:
                return True
    
        return False
        
    
    def getValue(self,key):
        
        for param in self.params:
            if param.name == key:
                return param.val
            
        raise error.MissingParameterException("no parameter found for key [{0}]".format(key))

    def set_postScript(self,script64):
        self._postScript = script64
        
    def get_postScript(self):
        return self._postScript;
        
    def set_preScript(self,script64):
        self._preScript = script64
        
    def get_preScript(self):
        return self._preScript;

    beforeload_JScript = property(get_preScript,set_preScript)
    afterload_JScript = property(get_postScript,set_postScript)
    name = property(get_name)
    params = property(get_params) 
    
    
    
    def addParameterAnon(self,val):
        index = len(self._parameterList) + 1
        indexParameterName = "p_%s" % (str(index))
        p = Parameter(indexParameterName,val)
        self._parameterList.append(p)
        
    def addParameter(self,nme,val):
        p = Parameter(nme,val)
        self._parameterList.append(p)
        
    
    def toJSON(self):
        """
{"name":"GetInputs","paramCount":0,"parameters":[{"name":"template","value":"testTemplate_v1.xls"},{"name":"datasetID","value":"ds1"}],
"UserCurrentTxID":"not_set_yet"}        
        
        """
        x = len(self._parameterList)
        
        s = ""
        s += "{'name':'%s'," % (self._name)
        s += "'paramCount':'%s'," % (str(x))
        s += "'parameters':["
        for p in self._parameterList:
            s += "{"
            s += "'name':'%s'," % (p.name)
            s += "'value':'%s'" % (p.val)
            s += "},"
        
        s = s[:-1] #snip last char
        s += "],"
        s += "'preJS64':'{0}',".format(self.beforeload_JScript)
        s += "'postJS64':'{0}'".format(self.afterload_JScript)
        #s += "'UserCurrentTxID':'%s'" % ('not_set_yeti')
        s += "}"
        
        return s
    
    JSON = property(toJSON)
         
class Parameter(object):
    def __init__(self, paramName,paramValue):
        self._paramName = paramName
        self._paramVal = paramValue
    
    def getName(self):
        return self._paramName
    
    def getValue(self):
        return self._paramVal
    
    name = property(getName)
    val = property(getValue)    



class User(dict):
    def __init__(self,_id=None,spec=None):
        """spec is dict { 'name':'userName'|None, """
        if(_id != None):
            """lookup user"""
        else:
            """new user from spec"""
            if(spec != None):
                """load spec"""
                self['username'] = spec['username']
                self['description'] = spec['description']
                self['password'] = spec['password']
                self['passwordAttempts'] = 0
                self['created'] = Utils().Timestamp()
                self['locked'] = False
            else:
                raise Exception("User constructor, needs at least one valid parameter")


class Group(dict):
    def __init__(self,_id=None,spec=None):
        """spec is dict { 'name':'groupName'|None, """
        if(_id != None):
            """lookup group"""
        else:
            """new group from spec"""
            if(spec != None):
                """load spec"""
                self['groupname'] = spec['groupname']
                if('users' in spec):
                    self['users'] = spec['users']
                else:
                    self['users'] = []
                    
                self['description'] = spec['description']
            else:
                raise Exception("Group constructor, needs at least one valid parameter")
        
    def addUser(self,_id):
        if('users' not in self):
            self['users'] = []
            
        self['users'].append( _id )
        
        
class Itinerary(dict):
    def __init__(self,kontext=None):
        if( kontext==None):
            kontext = Kontext()
            
        self['inCommands'] = []
        self['outCommands'] = []
        self['kontext'] = kontext
    def get_inCommands(self):
        return self['inCommands']
    def get_outCommands(self):
        return self['outCommands']
    def addInCommand(self,command):
        self['inCommands'].append(command)
    def addOutCommand(self,command):
        self['outCommands'].append(command)
    def get_Kontext(self):
        return self['kontext']
    def set_KontextVal(self,key,val):
        """set kontext key value pair"""
        self['kontext']['key'] = val
    def get_KontextVal(self,key):
        """retrieve kontext value"""
        if(key in self['kontext']):
            return self['kontext'][key]
        else:
            raise error.KeyNotFoundException("no key found for %s".format(key))
    
    kontext = property(get_Kontext)  
    inCommands = property(get_inCommands)
    outCommands = property(get_outCommands)

class ReturnEnvelope(object):
    """deprecated use itinerary instead"""
    def __init__(self):
        self.commands=[]
        self.TimeStamp = str(Utils().Timestamp())

    def add(self,cmd):
        self.commands.append(cmd)
    def toJSON(self):
        s = ""
        s += "{"
        s += "'time':'{0}',".format(self.TimeStamp)
        s += "'commands':["
        
        for c in self.commands:
            s += c.JSON
            s += ","
        
        s = s[:-1]
            
        s += "]"
        
       
        s += "}"
        
        return s
 
class TreeNode_v1(object):
    def __init__(self,_index):
        self.children = []
        self.parent = None
        self.depth = -1
        self.index = _index
        
    def _hasChildren(self):
        ret = False
        if self.children.__len__() > 0:
            ret = False
        else:
            ret = True
            
        return ret

    def addNode(self,node):
        node.parent = self
        self.children.append(node)
    
    def getNumberChildren(self):
        return len(self.children)
    
    childCount = property(getNumberChildren)
    hasChildren = property(_hasChildren)
    
    
        
    
        
    