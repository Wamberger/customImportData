
import os
from methods.prompts import Prompts
from util.startLog import getLog

def outputProtocol(protocol: list[dict], prop: Prompts):
    '''
    Edit data for the ouput protocol.
    '''
    # entirely different from original.

    log = getLog(__name__)

    pathToOutputFile = os.path.join(os.getcwd(), 'output.txt')
    with open(pathToOutputFile, "w") as file:
        for p in protocol:
            for key, value in p.items():
                file.write(f'{key} : {value}')
                file.write('\n')
            file.write('\n')
        file.close()

    for p in protocol:
        print(p)

    log.info('End of program.')
    exit()
