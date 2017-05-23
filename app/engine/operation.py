

class Execute:
    """
    Execute operations are used to execute a single method. Execute operations will be performed by
    the driver and the output of the method will be sent back to the endpoint when it is finished
    """

    def __init__(self, method, *args):
        """
        Creates a new Execute operation
        
        :param method: The method to be executed
        :param args: The arguments to provide to the method
        """
        self.method = method
        self.args = args


class Respond:
    """
    Respond operations are used to tell the driver that the execution is complete and to provide
    the given data as a response object
    """

    def __init__(self, **kwargs):
        """
        Creates a new Respond object
        
        :param kwargs: Arbitrary data to provide as a response
        """
        self.data = kwargs

    @staticmethod
    def success_response(success):
        """
        Utility function used to generate a success or failure response object

        :param success: True if successful, false otherwise
        :return: Dictionary representing a response object
        """
        return Respond(success=success)

    @staticmethod
    def warning_response(message):
        """
        Utility function used to generate a warning response object

        :param message: The warning message to send
        :return: The warning response
        """
        return Respond(warning=message)

    @staticmethod
    def error_response(message):
        """
        Utility function used to generate an error response object

        :param message: The error message to send
        :return: The error response
        """
        return Respond(error=message)