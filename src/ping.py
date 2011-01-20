from Http import *

import sys
#add module path search info to this module
sys.path.append('C:\inetpub\wwwroot\\net4\pyInetPub\site\src2\AgentIdea\src')

def Request():
    import core
    Header("Content-type: text/html")
    ute = core.Utils()
    d = ute.Timestamp()

        
    msg = "calling core time time %s" % (d)
    
    core.log(msg)

    Write(msg)