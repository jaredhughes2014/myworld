

from .operation import *


def execute_endpoint(endpoint, data=None):
    """
    Executes an endpoint function. Endpoint functions are generators which should yield one
    or more operations. This function will terminate when the endpoint yields a Respond operation
    
    :param endpoint: Generator function which yields operations
    :param data: Optional data to provide to the endpoint
    :return: Dictionary containing data to send as a response
    """
    try:
        gen = endpoint(**data) if data is not None else endpoint()
        op = next(gen)

        while isinstance(op, Execute):
            data = op.method(*op.args)
            op = gen.send(data)

        if isinstance(op, Respond):
            return op.data

        # This only occurs if there is an error with the endpoint format, so it should be an exception
        else:
            raise Exception('Invalid operation type: {}'.format(type(op)))

    # Handles requests that are missing parameters
    except KeyError:
        return Respond.error_response('Error. One or more required data items are missing').data
