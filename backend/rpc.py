from backend.rpcserver import rpc_method

## example methods

@rpc_method
def add(a, b):
    """
    Add two numbers together
    """
    return a+b


@rpc_method
def subtract(a, b):
    """
    Subtract two numbers together
    """
    return a-b


@rpc_method
def divide(a, b):
    """
    Divide a by b
    """
    return a/b

@rpc_method
def noparam():
    return "Got no parameters"

@rpc_method
def getProjects():
    # TODO populate this response from database
    testprojects = [
        { 'id': 40, 'name': 'test project'},
        { 'id': 21, 'name': 'test project'},
        { 'id': 89, 'name': 'test project'},
        { 'id': 38, 'name': 'test project'},
    ]
    return testprojects