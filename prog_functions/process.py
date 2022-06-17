
from methods.prompts import Prompts
from prog_functions.returnFunc import returnFunc
from prog_functions.modifyFileData import modifyFileData
from prog_functions.initConvAndValidTablesForInsert import initConvAndValidTablesForInsert
from classes.readCreate import ReadAndInitCSVdata, ReadAndInitCSVdataWithoutHeader
from util.buildUpPropCheck import buildUpPropCheck
from db.updateInsert_db import updateInsertDB
from util.open_read_file import openAndReadCsvAndCreateRowList


def processMappingAndInserts(prop: Prompts) -> returnFunc:
    '''
    The main processes in the program will be here executed and in subfunctions.

    The data from file will be read and modified according to the properties.
    From the modified data the classes as a copy of the DB (database) tables will be created.
    The properties for the creation of any db table is defined in a dictionary.
    After validation and initialisation the tables will be updated or inserted into the DB.
    Some tables are update/inserted via REST-API. 
    '''
    getFileData = openAndReadCsvAndCreateRowList(
        prop.importFile, 
        prop.dictReader,
        prop.csvSeperator
        )
    if not getFileData[0]:
        return returnFunc(False, getFileData[1], prop)

    collectedDataForInsert: list = []
    for row in getFileData[1]:
        
        getHeaderProp = buildUpPropCheck(prop)
        if not getHeaderProp[0]:
            return returnFunc(False, getHeaderProp[1], prop)
        
        if prop.dictReader: # with headline  # read and creates a class with the wished data (renamedCsvContent)
            csvData = ReadAndInitCSVdata(
                row, 
                getHeaderProp[1],
                getHeaderProp[2]
                )
        else:   # without headline
            csvData = ReadAndInitCSVdataWithoutHeader(
                row, 
                getHeaderProp[2]
                )

        successful = modifyFileData(csvData, prop)  # if the input data from file needs to be modified
        if not successful[0]:
            return returnFunc(False, successful[1], prop)

        if not prop.db_tables:
            return returnFunc(False, 'No db_tables were defined.', prop)
        else:
            getTablesWithFileData = initConvAndValidTablesForInsert(
                csvData, 
                prop.db_tables,
                prop
                )
            if not getTablesWithFileData[0]:
                return returnFunc(False, getTablesWithFileData[1], prop)

            collectedDataForInsert.append(getTablesWithFileData[1])
                
    if collectedDataForInsert:
        successful = updateInsertDB(
            collectedDataForInsert, 
            prop.db_tables,
            prop
            )
        if not successful:
            return returnFunc(False, None, prop)
    
    return returnFunc(True, collectedDataForInsert, prop)
        
