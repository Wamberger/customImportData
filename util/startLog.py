
import os
import logging
from methods.prompts import Prompts
from util.lists_of_data_labels import propNames

def getLog(scriptName: str) -> logging:

    pathToLogFile = os.path.join(os.getcwd(), 'logFile.log')
    formatLog = '[%(process)d] %(asctime)s [%(levelname)s] [%(filename)s] %(funcName)s (%(lineno)d): %(message)s'

    logging.basicConfig(
        filename=pathToLogFile,
        format=formatLog
        )

    log = logging.getLogger(scriptName)
    log.setLevel(logging.DEBUG)
    return log


def startLog(prompts: Prompts) -> None:
    '''
    Writes in log file the start of program with args.
    '''
    # different from original

    log = getLog(__name__)

    mainHeader = f'Start of program. Args: {prompts.importFile}. Prop: '

    args: str = ''
    for promp in propNames:
        args = args + '{}, '.format(getattr(prompts, promp))

    outPut = mainHeader + args

    log.info(outPut)