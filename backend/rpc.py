from backend.rpcserver import rpc_method

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
