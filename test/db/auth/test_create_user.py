
from test.db.testcase import DbTestCase
from app.db.functions.auth import create_user
from app.db.data import User


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
        create_user(self.email, self.pw)
        self.assert_contains_one(User, email=self.email, pw=self.pw)


if __name__ == '__main__':
    DbTestCase.main()
