

import unittest
from mongoengine import connect


class DbTestCase(unittest.TestCase):
    """
    Base class for a database function test case. This class provides mock database connectivity
    and utility functions for testing database values
    """

    def setUp(self):
        connect('myworldtest', host='mongomock://localhost')

    @staticmethod
    def main():
        """
        Reference pass to the unittest main() function
        """
        unittest.main()

    def assert_contains(self, collection, count, **kwargs):
        """
        Asserts that the given collection contains the given count of documents with the given keys
        
        :param collection: The collection to search through
        :param count: The number of documents expected
        :param kwargs: The keys used to query the document with
        """
        actual = collection.objects(**kwargs).count()
        self.assertEqual(count, actual, 'Collection contains incorrect number of documents')

    def assert_contains_one(self, collection, **kwargs):
        """
        Asserts that the given collection contains exactly one document with the given keys
        
        :param collection: The collection to search through
        :param kwargs: The keys used to query the document
        """
        self.assert_contains(collection, 1, **kwargs)
