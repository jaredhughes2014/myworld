
from test.db.testcase import DbTestCase
from app.db.functions.auth import delete_user, create_user, authenticate
from app.db.data import User, Auth


class DeleteUserTestCase(DbTestCase):
    """
    Tests the behavior of the delete user database function
    """

    def setUp(self):
        super(DeleteUserTestCase, self).setUp()
        self.email = 'test@gmail.com'
        self.pw = 'testPassword'

    def get_user(self):
        """
        Shortcut to get the user document created by the test data
        """
        return self.get_document(User, email=self.email, pw=self.pw)

    def test_standard_behavior(self):
        """
        Tests the behavior of the function under normal conditions
        """
        create_user(self.email, self.pw)
        response = delete_user(self.email, self.pw)

        self.assert_not_contains(User, email=self.email, pw=self.pw)
        self.assertTrue(response, 'Successful deletes should return True')

    def test_with_auth(self):
        """
        Tests the behavior of the function when the user is currently authenticated
        """
        create_user(self.email, self.pw)
        key = authenticate(self.email, self.pw)
        response = delete_user(self.email, self.pw)

        self.assert_not_contains(User, email=self.email, pw=self.pw)
        self.assert_not_contains(Auth, key=key)
        self.assertTrue(response, 'Successful deletes should return True')

    def test_wrong_password(self):
        """
        Tests the behavior of the function when an incorrect password is provided
        """
        create_user(email=self.email, pw=self.pw)
        response = delete_user(self.email, self.pw + 'wrongPassword')

        self.assert_contains_one(User, email=self.email, pw=self.pw)
        self.assertFalse(response, 'Unsuccessful deletes should return false')

    def test_wrong_password_with_auth(self):
        """
        Tests the behavior of the function when an incorrect password is provided
        and the user is authenticated
        """
        create_user(self.email, self.pw)
        key = authenticate(self.email, self.pw)
        response = delete_user(self.email, self.pw + 'wrongPassword')

        self.assert_contains_one(User, email=self.email, pw=self.pw)
        self.assert_contains_one(Auth, key=key)
        self.assertFalse(response, 'Unsuccessful deletes should return false')

    def test_email_does_not_exist(self):
        """
        Tests the behavior of the function when the provided email does not exist
        """
        create_user(self.email, self.pw)
        response = delete_user('wrongEmail' + self.email, self.pw)

        self.assert_contains_one(User, email=self.email, pw=self.pw)
        self.assertFalse(response, 'Unsuccessful deletes should return false')

    def test_no_users(self):
        """
        Tests the behavior of the function when there are no users in the database
        """
        response = delete_user(self.email, self.pw)

        self.assert_not_contains(User, email=self.email, pw=self.pw)
        self.assertFalse(response, 'Unsuccessful deletes should return false')

    def test_non_email(self):
        """
        Tests the behavior of the function when the user provides a non-email string
        as an email
        """
        response = delete_user(self.email + '..notEmail', self.pw)

        self.assertFalse(response, 'Response should be false for invalid emails')


if __name__ == '__main__':
    DbTestCase.main()
