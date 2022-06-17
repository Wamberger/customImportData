
from db.db_table_names import db_tables
from methods.create_modify_tables import CreateAndModifyTable


def createUpdateQuery(insertObject: CreateAndModifyTable, table: str) -> str: 

    updateTableProp = db_tables[table]  
    
    setValues: str = ''
    for attr in updateTableProp[1]:
        if not attr in updateTableProp[3]: 
            if setValues:
                setValues = setValues + ', '
            if isinstance(getattr(insertObject, attr), int) or isinstance(getattr(insertObject, attr), float):    
                setValues = setValues + attr + ' = ' + str(getattr(insertObject, attr))
            elif isinstance(getattr(insertObject, attr), str):
                setValues = setValues + attr + ' = ' + "'" + getattr(insertObject, attr) + "'"
    
    primaryKeys: str = ''
    for primary in updateTableProp[3]:
        if primaryKeys:
            primaryKeys = primaryKeys + ' and '
        if isinstance(getattr(insertObject, primary), int) or isinstance(getattr(insertObject, attr), float):
            primaryKeys = primaryKeys + primary + ' = ' + str(getattr(insertObject, primary))
        elif isinstance(getattr(insertObject, primary), str):
            primaryKeys = primaryKeys + primary + ' = ' + "'" + getattr(insertObject, primary) + "'"

    stmt = 'update ' + table + ' set ' + setValues + ' where ' + primaryKeys
    return stmt


def createInsertQuery(insertObject: CreateAndModifyTable, table: str) -> str:
    
    insertTableProp = db_tables[table]  
    
    setValues: str = ''
    for attr in insertTableProp[1]:
        if setValues:
            setValues = setValues + ', '
        if attr in insertTableProp[4]:
            seq = insertTableProp[4]
            setValues = setValues + seq[attr]
        elif isinstance(getattr(insertObject, attr), int) or isinstance(getattr(insertObject, attr), float):    
            setValues = setValues + str(getattr(insertObject, attr))
        elif isinstance(getattr(insertObject, attr), str):
            setValues = setValues + "'" + getattr(insertObject, attr) + "'"

    stmt = 'insert into ' + table + ' values (' + setValues + ')'
    return stmt

