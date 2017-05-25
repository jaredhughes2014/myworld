from test.db.testcase import DbTestCase
from app.db.functions.auth import create_user, user_exists
from app.db.data import User, Auth
from mongoengine.errors import ValidationError


class UserExistsTestCase(DbTestCase):
    """
    Tests the behavior of the user exists database function
    """

    def setUp(self):
        super(UserExistsTestCase, self).setUp()
        self.email = 'test@gmail.com'
        self.pw = 'testPassword'

    def test_user_does_exist(self):
        """
        Tests the behavior of the function when the user does exist
        """
        create_user(self.email, self.pw)
        self.assertTrue(user_exists(self.email), 'Query should return true if the user does exist')

    def test_user_does_not_exist(self):
        """
        Tests the behavior of the function when the user does not exist
        """
        create_user(self.email, self.pw)
        self.assertTrue(user_exists('wrongEmail' + self.email), 'Query should return true if the user does exist')

    def test_non_email(self):
        """
        Tests the behavior of the function when a non email address is used
        """
        with self.assertRaises(ValidationError):
            user_exists(self.email + '..invalidEmail')
