

from test.endpoints.testcase import EndpointTestCase
from app.endpoints.auth import delete_user
import app.db.functions.auth as db


class DeleteUserTestCase(EndpointTestCase):
    """
    Tests the behavior of the delete user endpoint
    """

    def setUp(self):
        self.email = 'test@gmail.com'
        self.pw = 'testPassword'
        self.mount_endpoint(delete_user, email=self.email, pw=self.pw)

    def test_standard_behavior(self):
        """
        Tests the behavior of the delete user endpoint following the standard flow
        """
        op = self.start_endpoint()

        # First operation. Send true to indicate the user's authentication was cleared successfully
        self.assert_execute_correct(op, db.clear_auth, self.email)
        op = self.advance_endpoint(True)

        # Second operation. Send true to indicate the user was deleted successfully
        self.assert_execute_correct(op, db.delete_user, self.email, self.pw)
        op = self.advance_endpoint(True)

        self.assert_success_response(op, True)

    def test_no_authentication(self):
        """
        Test the behavior of the delete user endpoint if the user is not authenticated. This should
        behave the same as if the user did exist
        """
        op = self.start_endpoint()

        # First operation. Send false to indicate the user is not authenticated
        self.assert_execute_correct(op, db.clear_auth, self.email)
        op = self.advance_endpoint(False)

        # Second operation. Send true to indicate the user was deleted successfully
        self.assert_execute_correct(op, db.delete_user, self.email, self.pw)
        op = self.advance_endpoint(True)

        self.assert_success_response(op, True)

    def test_no_user(self):
        """
        Tests the behavior of the delete user endpoint if the user does not exist or the
        given password is incorrect
        """
        op = self.start_endpoint()

        # First operation. Send true to indicate the user is not authenticated
        self.assert_execute_correct(op, db.clear_auth, self.email)
        op = self.advance_endpoint(False)

        # Second operation. Send false to indicate the user does not exist
        self.assert_execute_correct(op, db.delete_user, self.email, self.pw)
        op = self.advance_endpoint(False)

        self.assert_error_response(op)

if __name__ == '__main__':
    EndpointTestCase.main()
