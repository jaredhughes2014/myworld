
from test.db.testcase import DbTestCase
from app.db.functions.auth import create_user
from app.db.data import User
from mongoengine.errors import ValidationError


class CreateUserTestCase(DbTestCase):
    """
    Tests the behavior of the create user database function
    """

    def setUp(self):
        super(CreateUserTestCase, self).setUp()
        self.email = 'test@gmail.com'
        self.pw = 'testPassword'

    def test_standard(self):
        """
        Tests the behavior of the create user database function under normal conditions
        """
        response = create_user(self.email, self.pw)

        self.assert_contains_one(User, email=self.email, pw=self.pw)
        self.assertTrue(response, 'Response should be true when a user is created successfully')

    def test_non_email(self):
        """
        Tests the behavior of the create user function when the user uses a non-email string for an email
        """
        with self.assertRaises(ValidationError):
            create_user(self.email + '..com', self.pw)


if __name__ == '__main__':
    DbTestCase.main()
