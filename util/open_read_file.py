
import csv
from io import BufferedReader
import os.path
import chardet
from util.lists_of_data_labels import encodeList
from util.startLog import getLog

log = getLog(__name__)


def readingFile(file: BufferedReader, dictReader: bool, seperator: str) -> list:
    
    if dictReader: # either is with or without header
        readerObject = csv.DictReader(
            file, 
            delimiter=seperator
            )
    else:
        readerObject = csv.reader(
            file, 
            delimiter=seperator
            )
    fileData: list = []
    for row in readerObject:
        fileData += [row]
    
    return fileData


def predictEncoding(file: str, nLines=10) -> str:

    with open(file, 'rb') as f:
        rawData = b''.join([f.readline() for _ in range(nLines)])
    return chardet.detect(rawData)['encoding']


def openAndReadCsvAndCreateRowList(file: str, dictReader: bool, seperator: str) -> tuple[bool, list or str]:

    if not os.path.isfile(file):
        msg = 'In path: {} is no file to read.'.format(file)
        log.error(msg)
        return False, msg 
    else:
        encod = predictEncoding(file)
        try:
            with open(file, encoding=encod) as f:
                fileData = readingFile(f, dictReader, seperator) 
                return True, fileData
        except:
            fileData: list = []
            for enco in encodeList:
                try:
                    with open(file, encoding=enco) as f:
                        fileData = readingFile(f, dictReader, seperator)
                        if fileData:
                            break
                except:
                    log.warning(f'Cannot encode with ({enco}) the file: {file}')
            if not fileData:
                return False, 'Cannot encode the file: {}'.format(file)
            else:
                return True, fileData