
from classes.util_classes import CollectedTables
from db.db_table_names import db_tables
from db.create_queries_update_insert import createUpdateQuery, createInsertQuery
from rest_api.rest_call import restCall
from util.lists_of_data_labels import tablesWithUser
#from pony.orm import db_session, rollback
from methods.prompts import Prompts
#from <path> import getDB
from util.startLog import getLog


def updateInsertDB(insertData: list[CollectedTables], insert_db_tables: str, prop: Prompts) -> bool:
    '''
    For each data it will firstly try to do an update, if fails then insert will be done.
    Some tables have sequence id which is primary key, therefore their child tables 
    can get the primary key (id) after the update/insert.
    Some tables are individual or in combination with more tables updated or inserted via REST-API.
    '''

    log = getLog(__name__)

    for insertTables in insertData:
        primaryKeysForChildTables: dict = {}
        apiTables: dict = {}
        for table in insert_db_tables.split(','):
            if table in db_tables and table in insertTables.__dict__:

                if table in tablesWithUser:
                    t = getattr(insertTables, table)
                    successful = t.getAvailableUser(table)
                    if not successful:
                        return False

                if prop.childTables.strip() and table in prop.childTables.split(','):
                    t = getattr(insertTables, table)
                    successful = t.getIDfromParentTable(
                        table, 
                        db_tables, 
                        primaryKeysForChildTables
                        )
                    if not successful:
                        return False

                checkRest = db_tables[table]
                if checkRest[7] and not table in apiTables:
                    successful = restCall(
                            db_tables[table],
                            insertTables,
                            prop
                        )
                    if not successful[0]:
                        return False
                    else:
                        apiTables.update(successful[1])
                elif not table in apiTables:
                    getUpdateQuery = createUpdateQuery(
                        getattr(insertTables, table), 
                        table
                        )
                    try:
                        if not prop.testRun:
                            with db_session:
                                successful = getDB().execute(getUpdateQuery)
                                if successful.rowcount != 1:
                                    rollback()
                                    raise # goes in exception
                        else:   
                            log.info(f'#Test run# Update would be carried out: < {getUpdateQuery} >.')
                    except:
                        getInsertQuery = createInsertQuery(
                            getattr(insertTables, table), 
                            table
                            )
                        try:
                            with db_session:
                                successful = getDB().execute(getInsertQuery)
                                if successful.rowcount != 1:
                                    rollback()
                                    raise
                        except:
                            log.error(f'Update not possible with the select and data: < {getUpdateQuery} >')
                            log.error(f'Insert not possible with the select and data: < {getInsertQuery} >')
                            return False
                
                log.info(f'Update/Insert successfully: table < {table} >,')
                 
                t = getattr(insertTables, table)
                if prop.testRun:
                    ignoreError = True
                else:
                    ignoreError = False
                newPrimaryKeysForChildTables = t.getPrimaryKeysFromDB(table, db_tables, ignoreError=ignoreError)
                primaryKeysForChildTables.update(newPrimaryKeysForChildTables)
                if not primaryKeysForChildTables:
                    return False

    return True
