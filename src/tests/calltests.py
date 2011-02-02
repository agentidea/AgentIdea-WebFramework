from Http import *

import unittest
import consoleRunTests as crt

import sys
#add module path search info to this module
#sys.path.append('C:\inetpub\wwwroot\\net4\pyInetPub\site\src2\AgentIdea\src')

def Request():
    import core
    Header("Content-type: text/html")
    ute = core.Utils()
    d = ute.Timestamp()

        
    msg = "calling core time time %s" % (d)
    
    crt.runTests()
    
    core.log(msg)
    Write(msg)