
from util.startLog import getLog

def returnFunc(*args) -> list[dict]:
    '''
    Return function edit the returno data for the output.
    '''
    log = getLog(__name__)
    
    protocol: list = []
    if type(args[1]) != list and not args[0]:
        if not args[1]: #is None
            returnMsg = 'The program was stopped. Look at log file for more information.'
        else:
            returnMsg = args[1]
        protocol = [
            {   
                'Error_Message': returnMsg,
            }
        ]
        return protocol
    elif type(args[1]) == list and args[0]:
        for e in args[1]:
            creatingOneProtocol: dict = {}
            for table, attr in e.__dict__.items():
                for col, value in attr.__dict__.items():
                    creatingOneProtocol.update({table + '_' + col : value})
            protocol.append(creatingOneProtocol)
        return protocol
    else:
        log.error('Data error: cannot create protocol.')