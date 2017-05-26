
from test.db.testcase import DbTestCase
from app.db.functions.auth import create_user, authenticate, validate_auth
from app.db.data import Auth

from uuid import uuid4
import time


class ValidateAuthTestCase(DbTestCase):
    """
    Tests the behavior of the validate auth database function
    """

    def setUp(self):
        super(ValidateAuthTestCase, self).setUp()

        self.email = 'test@gmail.com'
        self.pw = 'testPassword'
        self.auth_key = str(uuid4())

    def init_user(self):
        """
        Creates and authenticates a new user
        
        :return: The authentication key of the created user
        """
        create_user(self.email, self.pw)
        return authenticate(self.email, self.pw)

    def get_auth(self, key):
        """
        Shortcut to get an authentication document with the given key
        
        :param key: The authentication to use
        :return: Auth document with the given authentication key
        """
        return self.get_document(Auth, key=key)

    def test_standard_flow(self):
        """
        Tests the behavior of the function under normal conditions
        """
        key = self.init_user()
        prev = self.get_auth(key)

        time.sleep(.1)

        response = validate_auth(key, self.email)
        current = self.get_auth(key)

        self.assert_contains_one(Auth, key=key)
        self.assertTrue(response, 'Successful updates should return true')
        self.assertGreater(current.expire_time, prev.expire_time, 'Successful updates should increase expire time')

    def test_invalid_auth_key(self):
        """
        Tests the behavior of the function when an invalid auth key is used
        """
        key = self.init_user()
        prev = self.get_auth(key)

        time.sleep(.1)

        response = validate_auth(str(uuid4()), self.email)
        current = self.get_auth(key)

        self.assert_contains_one(Auth, key=key)
        self.assertFalse(response, 'Unsuccessful updates should return false')
        self.assertEqual(prev.expire_time, current.expire_time, 'Failed refreshes should not change the expire time')

    def test_invalid_email(self):
        """
        Tests the behavior of the function when an invalid email is used
        """
        key = self.init_user()
        prev = self.get_auth(key)

        time.sleep(.1)

        response = validate_auth(key, 'wrongEmail' + self.email)
        current = self.get_auth(key)

        self.assert_contains_one(Auth, key=key)
        self.assertFalse(response, 'Unsuccessful updates should return false')
        self.assertEqual(prev.expire_time, current.expire_time, 'Failed refreshes should not change the expire time')

    def test_non_email(self):
        """
        Tests the behavior of the function when a non-email string is provided
        """
        key = self.init_user()
        self.get_auth(key)

        time.sleep(.1)

        response = validate_auth(key, self.email + '..invalidEmail')
        self.assertFalse(response, 'Invalid email addresses should always return false')

    def test_no_authentication(self):
        """
        Tests the behavior of the function when no documents exist in authentication
        """
        response = validate_auth(self.auth_key, self.email)

        self.assertFalse(response, 'Response should always be false with an empty collection')
        self.assert_not_contains(Auth, key=self.auth_key)


if __name__ == '__main__':
    DbTestCase.main()
