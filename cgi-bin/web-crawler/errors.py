# General
class ArgumentError(Exception): pass

# Persistence
class PersistenceError(Exception):
    def __init__(self, code=1, msg='Unknown'):
        self.code = code
        self.msg = msg

    def __str__(self):
        return 'ERR: CODE: %s ; MSG: %s' %(self.code, self.msg)
class PersistenceExecuteError(PersistenceError): pass
class PersistenceConnectionError(PersistenceError): pass
