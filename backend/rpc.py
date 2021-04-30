from backend.rpcserver import rpc_method

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
