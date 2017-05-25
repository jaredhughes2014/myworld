from test.db.testcase import DbTestCase
from app.db.functions.auth import create_user, authenticate, get_auth_key
from app.db.data import User, Auth
from mongoengine.errors import ValidationError

from uuid import uuid4


class GetAuthKeyTestCase(DbTestCase):
    """
    Tests the behavior of the get auth key database function
    """

    def setUp(self):
        super(GetAuthKeyTestCase, self).setUp()
        self.email = 'test@gmail.com'
        self.pw = 'testPassword'

    def test_standard_generate(self):
        """
        Tests the standard flow of the method while generating a key
        """
        create_user(self.email, self.pw)
        key = get_auth_key(self.email, True)

        self.assertIsNotNone(key, 'Key should never be none with generating')
        self.assertIsInstance(key, str, 'Keys should be strings')

    def test_standard_no_generate(self):
        """
        Tests the standard flow of the method without generating a key
        """
        create_user(self.email, self.pw)
        expected = authenticate(self.email, self.pw)

        actual = get_auth_key(self.email, False)

        self.assertIsNotNone(actual, 'Key should not be none if user is authenticated')
        self.assertEqual(expected, actual, 'The returned auth key should be the same as the actual key')

    def test_non_email_generate(self):
        """
        Tests the behavior of the method when using a non-email string and generating
        a key
        """
        create_user(self.email, self.pw)

        with self.assertRaises(ValidationError):
            get_auth_key(self.email + '..invalidEmail', True)

    def test_non_email_no_generate(self):
        """
        Tests the behavior of the method when using a non-email string and not generating
        a key
        """
        create_user(self.email, self.pw)

        with self.assertRaises(ValidationError):
            get_auth_key(self.email + '..invalidEmail', False)

    def test_generate_already_authenticated(self):
        """
        Tests the behavior of the generate variant of the method when the user is already authenticated
        """
        create_user(self.email, self.pw)
        expected = authenticate(self.email, self.pw)
        actual = get_auth_key(self.email, True)

        self.assertIsNotNone(actual, 'Generating key function should never return None')
        self.assertEqual(expected, actual, 'New key should never be generated if user is already authenticated')

    def test_no_generate_no_auth(self):
        """
        Tests the behavior of the no generate variant when the user is not authenticated
        """
        key = get_auth_key(self.email, False)
        self.assertIsNone(key, 'Key should be none if not generating and user does not exist')
