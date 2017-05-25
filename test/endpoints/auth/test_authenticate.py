
from test.endpoints.testcase import EndpointTestCase
from app.endpoints.auth import authenticate
import app.db.functions.auth as db

from uuid import uuid4


class LogInTestCase(EndpointTestCase):
    """
    Tests the behavior of the log in endpoint
    """

    def setUp(self):
        self.email = 'test@gmail.com'
        self.pw = 'testPassword'
        self.mount_endpoint(authenticate, email=self.email, pw=self.pw)

    def test_standard_behavior(self):
        """
        Tests the behavior of the endpoint following the standard flow
        """
        op = self.start_endpoint()

        # First Operation. Send true to indicate that the given credentials are valid
        self.assert_execute_correct(op, db.user_exists, self.email, self.pw)
        op = self.advance_endpoint(True)

        # Second Operation. Send an authentication key for use
        self.assert_execute_correct(op, db.get_auth_key, self.email, True)
        auth_key = str(uuid4())
        op = self.advance_endpoint(auth_key)

        # Third operation. Adds a new authentication token to the database
        self.assert_execute_correct(op, db.validate_auth, auth_key, self.email)
        op = self.advance_endpoint(None)

        self.assert_respond_correct(op, key=auth_key)

    def test_invalid_login(self):
        """
        Tests the behavior of the endpoint when invalid login data is provided
        """
        op = self.start_endpoint()

        # First Operation. Send false to indicate the user provided invalid credentials
        self.assert_execute_correct(op, db.get_auth_key, self.email, self.pw)
        op = self.advance_endpoint(False)

        self.assert_error_response(op)

if __name__ == '__main__':
    EndpointTestCase.main()
