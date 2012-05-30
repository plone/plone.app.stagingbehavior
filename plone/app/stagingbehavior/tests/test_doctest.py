from plone.testing import layered

from plone.app.stagingbehavior.tests.base import FUNCTIONAL_TESTING

import doctest
import unittest

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('../stagingbehavior.txt', optionflags = doctest.ELLIPSIS), 
                layer = FUNCTIONAL_TESTING),
        layered(doctest.DocFileSuite('regressiontests.txt', optionflags = doctest.ELLIPSIS), 
                layer = FUNCTIONAL_TESTING),
    ])
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
