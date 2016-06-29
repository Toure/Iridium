__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"
"""
This will be the standard location for all test that are separated via component name, which will allow
for flexible test execution, instead of a all or nothing approach.
"""

class TestRepo(object):

    def list_test(self):
        """
        List test will walk the test repo and return the information to the requester.
        """
        pass

    def find_test(self, test_name):
        """
        Find test will walk the test repo for a specific key value.
        """
        pass

