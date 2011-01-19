import unittest

import unittests_core
import unittests_persistence
import unittests_commands



def addTestSuite(suiteClass):
    suite = unittest.TestSuite()
    testSuite = unittest.makeSuite(suiteClass)
    suite.addTest(testSuite)
    return suite

def runTests():
    
    #old_stdout = sys.stdout
    #sys.stdout = stdout = StringIO()

    unittest.TextTestRunner(verbosity=2).run(addTestSuite(unittests_core.TestCoreComponents))
    unittest.TextTestRunner(verbosity=2).run(addTestSuite(unittests_commands.CommandTests))
    unittest.TextTestRunner(verbosity=2).run(addTestSuite(unittests_persistence.TestDBfunctions))

    #s = old_stdout
    #s = old_stdout
    

runTests()