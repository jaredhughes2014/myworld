
from app.endpoints.auth import create_user
import app.db.functions.auth as db
from test.endpoints.testcase import EndpointTestCase


class CreateUserTestCase(EndpointTestCase):
    """
    Tests the behavior of the create user endpoint
    """

    def setUp(self):
        self.email = 'test@gmail.com'
        self.pw = 'testPassword'

        self.mount_endpoint(create_user, email=self.email, pw=self.pw)

    def test_standard(self):
        """
        Tests the behavior of the create user endpoint under normal conditions
        """
        op = self.start_endpoint()

        # First operation. Send false to determine the user already exists
        self.execute_operation_test(op, db.user_exists, self.email)
        op = self.continue_endpoint(False)

        # Second Operation. Send true to determine a user was created successfully
        self.execute_operation_test(op, db.create_user, self.email, self.pw)
        op = self.continue_endpoint(True)

        # The operation should be successful
        self.success_response_test(op, True)

    def test_user_exists(self):
        """
        Tests the behavior of the create user endpoint when a user already exists
        """
        op = self.start_endpoint()

        # First operation. Send true to indicate a user already exists
        self.execute_operation_test(op, db.user_exists, self.email)
        op = self.continue_endpoint(True)

        # The operation should yield a warning response
        self.warning_response_test(op)


if __name__ == '__main__':
    EndpointTestCase.main()
