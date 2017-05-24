

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

    @staticmethod
    def create_document(collection, **kwargs):
        """
        Creates a document in the given collection type using the given keyword arguments
        
        :param collection: The collection to insert a document into
        :param kwargs: Keys used to create a document
        :return: The created document
        """
        doc = collection(**kwargs)
        doc.save()
        return doc

    @staticmethod
    def get_document(collection, **kwargs):
        """
        Gets the first document from the given collection with the given properties
        
        :param collection: The collection to search through
        :param kwargs: Set of keyword arguments representing properties on a document
        :return: The document if it exists, otherwise None
        """
        return collection.objects(**kwargs).first()

    @staticmethod
    def get_documents(collection, **kwargs):
        """
        Gets all documents from the given collection with the given properties

        :param collection: The collection to search through
        :param kwargs: Set of keyword arguments representing properties on a document
        :return: List of all documents with the given keys
        """
        return [x for x in collection.objects(**kwargs)]

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

    def assert_not_contains(self, collection, **kwargs):
        """
        Asserts that the given collection does not contain any documents with the given properties
        
        :param collection: Collection to search through
        :param kwargs: Data to use as a query
        """
        count = collection.objects(**kwargs).count()
        self.assertEqual(0, count, 'Collection contains elements with the given properties')
