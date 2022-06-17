
from classes.readCreate import ReadAndInitCSVdata, ReadAndInitCSVdataWithoutHeader
from classes.util_classes import CollectedTables
from methods.create_modify_tables import CreateAndModifyTable
from db.db_table_names import db_tables
from methods.prompts import Prompts


def initConvAndValidTablesForInsert(
    insertData: ReadAndInitCSVdataWithoutHeader or ReadAndInitCSVdata, 
    insert_db_tables: str, 
    prop: Prompts
    ) -> tuple[bool, CollectedTables or str]:
    '''
    Creates a class with classes/objects.
    Each subclass is one table from the DB with the table attributes (columns).
    If some tables are connected, the child tables will receive the primary key 
    or other key from their parent table in order to have the right data for the validation. 
    '''
    collectedTables = CollectedTables()
    primaryKeysForChildTables: dict = {}
    for table in insert_db_tables.split(','):
        if table in db_tables:
            tableProp = db_tables[table]

            getTable = CreateAndModifyTable(
                tableProp=tableProp,
                insertData=insertData
                )
            
            successful = getTable.getEncryptedPassword(table)
            if not successful:
                return False, None
            
            if prop.childTables.strip() and table in prop.childTables.split(','):
                    successful = getTable.getIDfromParentTable(
                        table, 
                        db_tables, 
                        primaryKeysForChildTables
                        )
                    if not successful:
                        return False, 'Code corruption, cannot save primary key.'

            # This function needs additional coding
            #successful = getTable.convertAndValidData(table, prop.times, prop.ignoreFieldValid)
            #if not successful[0]:
            #    return False, successful[1]
            
            #if not prop.notInitDBvalues:
            #    successful = getTable.initEmptyAttrWithValuesFromDB(table, tableProp)
            #    if not successful[0]:
            #        return False, successful[1]

            newPrimaryKeysForChildTables = getTable.getPrimaryKeysFromDB(table, db_tables)
            primaryKeysForChildTables.update(newPrimaryKeysForChildTables)

            setattr(collectedTables, table, getTable)

    if collectedTables.__dict__:
        return True, collectedTables
    else:
        return False, 'Data cannot be read. Wrong db_tables?'