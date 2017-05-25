from test.db.testcase import DbTestCase
from app.db.functions.auth import log_out, create_user, authenticate
from app.db.data import User, Auth

from mongoengine.errors import ValidationError


class LogOutTestCase(DbTestCase):
    """
    Tests the behavior of the log out database function
    """

    def setUp(self):
        super(LogOutTestCase, self).setUp()
        self.email = 'test@gmail.com'
        self.pw = 'testPassword'

    def init_user(self):
        """
        Initializes a user and returns their authentication key

        :return: The test user's authentication key
        """
        create_user(self.email, self.pw)
        return authenticate(self.email, self.pw)

    def get_user(self, email):
        """
        Shortcut to get the document with the given email address
        
        :param email: The user's email address
        :return: User document with the given email
        """
        return self.get_document(User, email=email)

    def test_standard_flow(self):
        """
        Tests the method under standard conditions
        """
        self.init_user()
        response = log_out(self.email)

        self.assert_not_contains(Auth, user=self.get_user(self.email))
        self.assertTrue(response, 'Successful clears should return True')

    def test_not_email(self):
        """
        Tests the method using an email that does not exist
        """
        self.init_user()
        response = log_out('wrongEmail' + self.email)

        self.assert_contains_one(Auth, user=self.get_user(self.email))
        self.assertFalse(response, 'Unsuccessful clears should return False')

    def test_no_auths(self):
        """
        Tests the method against an empty collection
        """
        response = log_out(self.email)

        self.assert_not_contains(Auth, user=self.get_user(self.email))
        self.assertFalse(response, 'Method should always return false when collection is empty')

    def test_non_email(self):
        """
        Tests the method using a non-email formatted email address
        """
        with self.assertRaises(ValidationError):
            log_out(self.email + '..notAnEmail')


if __name__ == '__main__':
    DbTestCase.main()