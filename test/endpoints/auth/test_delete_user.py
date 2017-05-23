

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
        self.mount_endpoint(db.delete_user, email=self.email, pw=self.pw)

    def test_standard_behavior(self):
        """
        Tests the behavior of the delete user endpoint following the standard flow
        """
        op = self.start_endpoint()

        # First operation. Send true to indicate the user's authentication was cleared successfully
        self.execute_operation_test(op, db.clear_auth, self.email)
        op = self.continue_endpoint(True)

        # Second operation. Send true to indicate the user was deleted successfully
        self.execute_operation_test(op, db.delete_user, self.email, self.pw)
        op = self.continue_endpoint(True)

        self.success_response_test(op, True)

    def test_no_authentication(self):
        """
        Test the behavior of the delete user endpoint if the user is not authenticated. This should
        behave the same as if the user did exist
        """
        op = self.start_endpoint()

        # First operation. Send false to indicate the user is not authenticated
        self.execute_operation_test(op, db.clear_auth, self.email)
        op = self.continue_endpoint(False)

        # Second operation. Send true to indicate the user was deleted successfully
        self.execute_operation_test(op, db.delete_user, self.email, self.pw)
        op = self.continue_endpoint(True)

        self.success_response_test(op, True)

    def test_no_user(self):
        """
        Tests the behavior of the delete user endpoint if the user does not exist or the
        given password is incorrect
        """
        op = self.start_endpoint()

        # First operation. Send true to indicate the user is not authenticated
        self.execute_operation_test(op, db.clear_auth, self.email)
        op = self.continue_endpoint(False)

        # Second operation. Send false to indicate the user does not exist
        self.execute_operation_test(op, db.delete_user, self.email, self.pw)
        op = self.continue_endpoint(False)

        self.error_response_test(op)
