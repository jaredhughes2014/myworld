import unittest
from app.engine.operation import *


class EndpointTestCase(unittest.TestCase):
    """
    Utility class designed for testing endpoint generator functions
    """

    def mount_endpoint(self, endpoint, **data):
        """
        Mounts an endpoint
        
        :param endpoint: The endpoint function
        :param data: The optional data to provide as an argument
        :return: None
        """
        self.gen = endpoint(**data) if len(data) > 0 else endpoint()

    def start_endpoint(self):
        """
        Starts the endpoint generator and returns the first output from it
        
        :return: The first yielded output from the generator
        """
        return next(self.gen)

    def continue_endpoint(self, data):
        """
        Continues to the next yielded value from the endpoint generator.
        
        :param data: Data to send back to the generator
        :return: The next yielded output from the generator
        """
        return self.gen.send(data)

    def execute_operation_test(self, op, expected_method, *args):
        """
        Utility function used to test an output execute operation. This will verify the output
        is actually an Execute operation
        
        :param op: The yielded value from the generator
        :param expected_method: The method expected to be in the execute operation
        :param args: The arguments expected to be in the operation
        """
        self.assertIsInstance(op, Execute, 'Operation is not an Execute operation')
        self.assertEqual(expected_method, op.method, 'Operation does not have the expected method')
        self.assertEqual(len(args), len(op.args), 'Operation does not have the expected number of arguments')

        for i in range(0, len(args)):
            self.assertEqual(args[i], op.args[i], 'Argument {} is not matching'.format(i))

    def respond_operation_test(self, op, **kwargs):
        """
        Utility function used to test an output respond operation. This will verify the output
        is actually a Respond operation. If any argument has a value of None, it is assumed that
        the value of the argument does not matter
        
        :param op: The respond operation
        :param kwargs: Data to check for in the Respond object
        """
        self.assertIsInstance(op, Respond, 'Operation is not a Respond operation')

        for key, value in kwargs.items():
            self.assertIn(key, op.data, 'Respond operation missing expected key: {}'.format(key))

            if value is not None:
                self.assertEqual(value, op.data[key], 'Data for {} is not the expected value'.format(key))

    def respond_operation_test_with_null(self, op, **kwargs):
        """
        Utility function used to test an output respond operation. This will verify the output
        is actually a Respond operation. None values will be explicitly checked to be None

        :param op: The respond operation
        :param kwargs: Data to check for in the Respond object
        """
        self.assertIsInstance(op, Respond, 'Operation is not a Respond operation')

        for key, value in kwargs.items():
            self.assertIn(key, op.data, 'Respond operation missing expected key: {}'.format(key))
            self.assertEqual(value, op.data[key], 'Data for {} is not the expected value'.format(key))

    def success_response_test(self, op, success):
        """
        Shortcut command to test if an operation is a success response
        
        :param op: Operation to test
        :param success: True if the success outcome should be true, false otherwise
        """
        self.respond_operation_test(op, success=success)

    def warning_response_test(self, op, message=None):
        """
        Shortcut command to test if an operation is a warning message response. 
        
        :param op: Operation to test
        :param message: The expected warning message. Do not provide a message to ignore the contents of the message
        """
        self.respond_operation_test(op, warning=message)

    def error_response_test(self, op, message=None):
        """
        Shortcut command to test if an operation is an error message response. 

        :param op: Operation to test
        :param message: The expected error message. Do not provide a message to ignore the contents of the message
        """
        self.respond_operation_test(op, error=message)


    @staticmethod
    def main():
        """
        Execute when running a test case as a script to begin testing
        
        :return: None
        """
        unittest.main()
