
import sys
#from <pathToDBfunction> import connectDB, getDB
from util.startLog import startLog
from methods.prompts import Prompts
from prog_functions.process import processMappingAndInserts
from outputProtocol import outputProtocol
from util.args import getArgs


def main():

    args = getArgs()
    getPrompts = Prompts(args)
    getPrompts.compilePrompsWithAppProp() # this function was primarily called after the connection with DB.
    startLog(getPrompts) 

    #connectDB(getDB())
    # you need to connect own DB.

    getProtocol = processMappingAndInserts(getPrompts)

    outputProtocol(getProtocol, getPrompts)

sys.modules[__name__] = main