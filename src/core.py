import sys
import config
import error

def printList(list):
    for item in list:
        print item
 
    
def ParseMacroDict(macro):
    cmd = Command(macro['name'])
    for param in macro['parameters']:
        cmd.addParameter(param['name'], param['value'])
    return cmd

def pack(what):
    import urllib
    s = what.encode('base64','strict')
    return urllib.quote(s)

def unpack(what):
    import urllib
    s = urllib.unquote(what)
    return s.decode('base64','strict')
      
def log(s):
    
    return

    import os.path 
    
    logfile = None
    
    dt = Utils().Timestamp()
    
    
    if not os.path.exists(config.LogPath): 
        try:
            os.makedirs(config.LogPath)
        except:
            print "Unexpected dir creation error:" % list(sys.exc_info())
            raise
             

        
    #openMode = 'a'
    
    if( os.path.isfile(config.LogFile) == False ):
        try:
            logfile = open(config.LogFile,'w') 
        except IOError as (errno, strerror):
            print "I/O error W ({0}): {1}".format(errno, strerror)
            return
        except:
            print "Unexpected file open W error: %s" % list(sys.exc_info())
            return
    else:
        try:
            logfile = open(config.LogFile,'a') 
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

     
# http://code.activestate.com/recipes/576750-pretty-print-xml/   
prettyPrint = lambda dom: '\n'.join([line for line in dom.toprettyxml(indent=' '*2).split('\n') if line.strip()])


def ConvertDictToString(d):
    #from pprint import pprint 
    #pprint(d)
    return ''.join(["'%s':%s\r\n" % item for item in d.iteritems()])


def info(object, spacing=10, collapse=1):
    """Print methods and doc strings.
    
    Takes module, class, list, dictionary, or string."""
    methodList = [e for e in dir(object) if callable(getattr(object, e))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print "\n".join(["%s %s" %
                     (method.ljust(spacing),
                      processFunc(str(getattr(object, method).__doc__)))
                     for method in methodList])

def processCommand(cmd,commandCoreTuple = None):
    """ processess a Command dynamically """
    moduleID = None
    klassID = None
    
    if(commandCoreTuple == None):
        moduleID = config.commandCoreTuple[0]
        klassID =  config.commandCoreTuple[1] + cmd.name
    else:
        moduleID = commandCoreTuple[0]
        klassID =  commandCoreTuple[1] + cmd.name
    
    
    #log("LOAD Python Class -- %s.%s" % (moduleID,klassID))

    ret = None
    
    try:
        mod = __import__(moduleID, globals(), locals(), [klassID]) 
        klass = getattr(mod, klassID) 
        c = klass()
        ret = c.executeCommand(cmd)
        log("Finished Executing command {0}".format(cmd.name))
    except AttributeError as ae:
        logMsg = "It's MostLikely this command {0} was not found.{1}".format(cmd.name,list(sys.exc_info()))
        
        log(logMsg)
        raise error.CommandNotFoundException(logMsg)
        
    except:
        log("Error loading %s %s" % (klassID,list(sys.exc_info())))
        raise
        
    return ret


class Utils(object):

    def Ping(self,n):
        return n /3
     
    def getRandom(self):
        import random
        return random.random()   
        
    def Timestamp(self):
        import datetime
        import string
        d = datetime.datetime.now()
        #return '{:%Y-%m-%d %H:%M:%S}'.format(d)
        return d
    
class Command(object):
    def __init__(self, commandName):
        self._name = commandName
        self._parameterList = []
        self._preScript = config.onCommandLoad64
        self._postScript = config.onCommandUnload64

    def get_name(self):
        return self._name
        
    def get_params(self):
        return self._parameterList
    
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

    onload_JScript = property(get_preScript,set_preScript)
    onblur_JScript = property(get_postScript,set_postScript)
    
    
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
            s += "'value':\"%s\"" % (p.val)
            s += "},"
        
        s = s[:-1] #snip last char
        s += "],"
        s += "'preJS64':'{0}',".format(self.onload_JScript)
        s += "'postJS64':'{0}',".format(self.onblur_JScript)
        s += "'UserCurrentTxID':'%s'" % ('not_set_yeti')
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

class ReturnEnvelope(object):
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
    
    
        
    
        
    