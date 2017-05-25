
from test.endpoints.testcase import EndpointTestCase
from app.endpoints.auth import log_out
import app.db.functions.auth as db

from uuid import uuid4


class LogOutTestCase(EndpointTestCase):
    """
    Tests the behavior of the logout endpoint
    """

    def setUp(self):
        self.auth_key = str(uuid4())
        self.mount_endpoint(log_out, key=self.auth_key)

    def test_standard_behavior(self):
        """
        Tests the behavior of the endpoint under the standard flow
        """
        op = self.start_endpoint()

        # First operation. Send true to indicate the user's auth key was deactivated successfully
        self.assert_execute_correct(op, db.clear_auth, self.auth_key)
        op = self.advance_endpoint(True)

        self.assert_success_response(op, True)

    def test_no_auth(self):
        """
        Tests the behavior of the endpoint when there is no authentication token for the user
        """
        op = self.start_endpoint()

        # First operation. Send false to indicate the user's auth key was not deactivated
        self.assert_execute_correct(op, db.clear_auth, self.auth_key)
        op = self.advance_endpoint(False)

        self.assert_error_response(op)

if __name__ == '__main__':
    EndpointTestCase.main()
