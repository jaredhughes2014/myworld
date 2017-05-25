
from test.db.testcase import DbTestCase
from app.db.functions.auth import clear_auth, create_user, authenticate
from app.db.data import User, Auth

from uuid import uuid4


class ClearAuthTestCase(DbTestCase):
    """
    Tests the behavior of the clear auth database function
    """

    def setUp(self):
        super(ClearAuthTestCase, self).setUp()
        self.email = 'test@gmail.com'
        self.pw = 'testPassword'

    def init_user(self):
        """
        Initializes a user and returns their authentication key
        
        :return: The test user's authentication key
        """
        create_user(self.email, self.pw)
        return authenticate(self.email, self.pw)

    def test_standard_flow(self):
        """
        Tests the method under standard conditions
        """
        key = self.init_user()

        response = clear_auth(key)

        self.assert_not_contains(Auth, key=key)
        self.assertTrue(response, 'Successful clears should return True')

    def test_no_auth_key(self):
        """
        Tests the method using an auth key that does not exist
        """
        key = self.init_user()
        response = clear_auth(str(uuid4()))

        self.assert_contains_one(Auth, key=key)
        self.assertFalse(response, 'Unsuccessful clears should return False')

    def test_no_auths(self):
        """
        Tests the method against an empty collection
        """
        key = str(uuid4())
        response = clear_auth(key)

        self.assert_not_contains(Auth, key=key)
        self.assertFalse(response, 'Method should always return false when collection is empty')


if __name__ == '__main__':
    DbTestCase.main()