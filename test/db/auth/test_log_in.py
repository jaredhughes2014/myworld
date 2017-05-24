
from test.db.testcase import DbTestCase
from app.db.functions.auth import delete_user, create_user, log_in
from app.db.data import User, Auth
from mongoengine.errors import ValidationError


class LogInTestCase(DbTestCase):
    """
    Tests the behavior of the log in database function
    """

    def setUp(self):
        super(LogInTestCase, self).setUp()
        self.email = 'test@gmail.com'
        self.pw = 'testPassword'
        self.user = self.get_document(User, email=self.email)

    def test_standard_flow(self):
        """
        Tests the behavior of the method under normal conditions
        """
        create_user(self.email, self.pw)
        response = log_in(self.email, self.pw)

        user = self.get_document(User, email=self.email)
        self.assert_email_key_exist(user, response)

    def test_auth_already_exists(self):
        """
        Tests the behavior of the method when the user is already authenticated
        """
        create_user(self.email, self.pw)

        r1 = log_in(self.email, self.pw)
        r2 = log_in(self.email, self.pw)

        self.assertEqual(r1, r2, 'Logging in while already authenticated returns different auth keys')
        self.assert_email_key_exist(self.user, r2)

    def test_wrong_password(self):
        """
        Tests the behavior of the method when the user uses the wrong password
        """
        create_user(self.email, self.pw)
        response = log_in(self.email, self.pw + 'wrongPassword')

        self.assert_not_contains(Auth, key=response, user=self.user)
        self.assertIsNone(response, 'Unsuccessful login attempts should return None')

    def test_user_does_not_exist(self):
        """
        Tests the behavior of the method when the user does not exist
        """
        create_user(self.email, self.pw)
        email = 'wrongEmail' + self.email

        response = log_in(email, self.pw)

        self.assertIsNone(response, 'Unsuccessful login attempts should return None')
        self.assert_not_contains(Auth, user=self.user)

    def test_no_users(self):
        """
        Tests the behavior of the method when the user does not exist
        """
        response = log_in(self.email, self.pw)

        self.assertIsNone(response, 'Unsuccessful login attempts should return None')
        self.assert_not_contains(Auth, user=self.user)

    def test_non_email(self):
        """
        Tests the behavior of the method when the user uses a non-email string as an email
        """
        create_user(self.email, self.pw)
        with self.assertRaises(ValidationError):
            log_in(self.email + '..notAnEmailAddress', self.pw)

    def assert_email_key_exist(self, user, key):
        """
        Shortcut assertion to make sure the given email and key exist on the same document
        
        :param user: The user document that should be tied to the authentication
        :param key: Authentication key associated with a session
        """
        d1 = self.get_document(Auth, user=user)
        d2 = self.get_document(Auth, key=key)
        d3 = self.get_document(Auth, user=user, key=key)

        self.assert_contains_one(Auth, user=user)
        self.assert_contains_one(Auth, key=key)
        self.assert_contains_one(Auth, user=user, key=key)

        self.assertEqual(d1, d2, 'Authentication record is different for user and key')
        self.assertEqual(d1, d3, 'Authentication record is different for user and both user and key')


if __name__ == '__main__':
    DbTestCase.main()
