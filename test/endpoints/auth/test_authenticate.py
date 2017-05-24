
from test.endpoints.testcase import EndpointTestCase
from app.endpoints.auth import authenticate
import app.db.functions.auth as db

from uuid import uuid4


class AuthenticateTestCase(EndpointTestCase):
    """
    Tests the behavior of the authenticate endpoint
    """

    def setUp(self):
        self.auth_key = str(uuid4())
        self.email = 'test@gmail.com'
        self.mount_endpoint(authenticate, key=self.auth_key, email=self.email)

    def test_standard_behavior(self):
        """
        Tests the behavior of the authenticate endpoint using standard flow
        """
        op = self.start_endpoint()

        # First operation. Send true to indicate the auth key was updated successfully
        self.assert_execute_correct(op, db.authenticate, self.auth_key, self.email)
        op = self.advance_endpoint(True)

        self.assert_success_response(op, True)

    def test_invalid_auth_key(self):
        """
        Tests the behavior of the authenticate endpoint when the provided auth key is not valid
        """
        op = self.start_endpoint()

        # First operation. Send false to indicate the auth key is invalid
        self.assert_execute_correct(op, db.authenticate, self.auth_key, self.email)
        op = self.advance_endpoint(False)

        self.assert_error_response(op)

if __name__ == '__main__':
    EndpointTestCase.main()
