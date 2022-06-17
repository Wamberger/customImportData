
import hashlib
#from unidecode import unidecode
#from pony.orm import select, db_session
from methods.prompts import Prompts
#from <path> import getDB
from datetime import datetime
#from <pathToEntity> import Tables
#from <pathToOwnDateformats> import Date, Time, Timespan
from classes.util_classes import DataTypes
from util.findDateFormat import findDateFormat
from util.lists_of_data_labels import tablesWithUser
from util.startLog import getLog


log = getLog(__name__)

errorMsg = [
    'Field: {} in table {} is primary key, it cannot be < {} >.',
    'Field: {} is primary key, it cannot be None. Look at log file for more information.',
    'Field: {} in the table {} is required. It cannot be < {} >.',
    'Field: {} is required, it cannot be None. Look at log file for more information.',
    'Field: {} has more than {} char or numbers - Not allowed.',
    'The Datatype for column/field: {} is wrong. Look at log file for more information.',
    'The Datatype for column/field: {} in table {} is wrong. The value < {} > is not < {} >, but < {} >.',
    'Cannot initiate values from DB. Invalid SQL select: < {} >',
    'Cannot initiate values from DB. Invalid primary key. Look at log file for more information.'
    ]


class CreateAndModifyTable():
    def __init__(self, tableProp: list, insertData: object):
        '''
        creates a class according to the DB table.
        '''
        attr_withTableName = tableProp[0]
        attr_noTableName = tableProp[1]
        attr_defaultValues = tableProp[2]
        for i, attr in enumerate(attr_withTableName):
            if hasattr(insertData, attr) and getattr(insertData, attr):
                setattr(self , attr_noTableName[i], getattr(insertData, attr))
            else:
                setattr(self , attr_noTableName[i], attr_defaultValues[i])

    def getIDfromParentTable(self, table: str, db_tables: dict[list], parentPrimKey: dict[dict]) -> bool:
        '''
        Get primary key or other keys from parent table.
        '''
        parentTable = db_tables[table]
        for parTable, v in parentTable[5].items():
            for parentCol, insToCol in v.items():
                if parTable in parentPrimKey and parentCol in parentPrimKey[parTable]:
                    for key, value in parentPrimKey[parTable].items():
                        if parentCol == key:
                            setattr(self, insToCol, value)
                else:
                    return False
        return True

    def getEncryptedPassword(self, table: str) -> bool:

        if table in tablesWithUser:
            if hasattr(self, 'password'):
                try:
                    #cleanPassword = unidecode(getattr(self, 'password')) # remove 'strange' letters.
                    # original above
                    cleanPassword = getattr(self, 'password') 
                    h = hashlib.sha1()
                    h.update(bytearray(cleanPassword.encode()))
                    shDigest = h.digest()
                    encryptedPassword: str = ''
                    for i in range(h.digest_size):
                        valueByte = shDigest[i].to_bytes(byteorder='little', length=1)
                        valueInt = int.from_bytes(valueByte, byteorder='little', signed=True)
                        encryptedPassword += '@' + str(valueInt) + '#'

                    setattr(self, 'password', encryptedPassword)
                except:
                    log.error('Cannot encrypt the password: < {} >.'.format(getattr(self, 'password')))
                    return False
        return True

    def getQueryAllSelect(self, table: str, tableProp: list[list]) -> str:
        '''
        Creates SQL 'search' select.
        '''

        if tableProp[4]: #if seq in the table, then sometimes seq is the id, so other fields for search
            fieldsForSearch = tableProp[6]
        else:
            fieldsForSearch = tableProp[3]

        primaryKeys: str = ''
        for primary in fieldsForSearch:
            if primaryKeys:
                primaryKeys = primaryKeys + ' and '
            if isinstance(getattr(self, primary), int) or isinstance(getattr(self, primary), float):
                if getattr(self, primary):
                    primaryKeys = primaryKeys + primary + ' = ' + str(getattr(self, primary))
                elif isinstance(getattr(self, primary), int):
                    primaryKeys = primaryKeys + primary + ' = ' + '0'
                else:
                    primaryKeys = primaryKeys + primary + ' = ' + '0.0'
            elif isinstance(getattr(self, primary), str):
                if getattr(self, primary):
                    primaryKeys = primaryKeys + primary + ' = ' + "'" + str(getattr(self, primary)) + "'"
                else:
                    primaryKeys = primaryKeys + primary + ' = ' + "' '"
        
        stmt = 'select * from ' + table + ' where ' + primaryKeys
        return stmt

    def getPrimaryKeysFromDB(self, table: str, db_tables: dict[list], ignoreError: bool = True) -> dict:
        '''
        Get primary key from DB or from the input data.
        '''
        primaryKeys: dict = {}
        tableProp = db_tables[table]
        stmt = self.getQueryAllSelect(table, tableProp)
        try:
            # with db_session:
            #     getValues = getDB().select(stmt)
            #     if getValues and len(getValues) == 1:
            #         primaryKeys[table] = {}
            #         for primary in tableProp[3]:
            #             for elem in getValues:
            #                 if hasattr(self, primary):
            #                     primaryKeys[table].update({primary : getattr(elem, primary.upper())})
            #                 else:
            #                     log.error('No such primary key (< {} >) in the table or corrupted data. Look at table properties.'.format(primary))
            #     else:
            if not ignoreError:
                log.error(f'No data was found. Primary key was not able to add. Query: < {stmt} >')    
            if ignoreError:
                primaryKeys[table] = {}
                for primary in tableProp[3]:
                    if hasattr(self, primary):
                        primaryKeys[table].update({primary : getattr(self, primary)})
                    else:
                        log.error(f'No such primary key (< {primary} >) in the table or corrupted data. Look at table properties.')
        except:
            log.error(f'Query is incorrect: < {stmt} >')
        return primaryKeys
    
    def initEmptyAttrWithValuesFromDB(self, table: str, tableProp: list[list]) -> tuple[bool, None or str]:
        '''
        If the primary key from input data already exist in the DB, 
        the empty attributes will receive the values from the DB.
        '''
        stmt = self.getQueryAllSelect(table, tableProp)
        try:
            with db_session:
                getValues = getDB().select(stmt)
        except:
            log.error(errorMsg[7].format(stmt))
            return False, errorMsg[8]
        if getValues and len(getValues) == 1: #should be only one
            for key, value in self.__dict__.items():
                if not value or value == ' ': # for not Null
                    for item in getValues:
                        if hasattr(item, key.upper()) and getattr(item, key.upper()):
                            setattr(self, key, getattr(item, key.upper()))
                            break
        else:
            log.info(f'No init of values from the DB. Query: < {stmt} >')
        
        return True, None

    def getAvailableUser(self, table: str) -> bool:
        '''
        Check if the user name already exist. If it does, the number will be add.
        '''
        stmt = 'select * from ' + table + ' where '
        if hasattr(self, 'user'):
            stmt1 =  stmt + 'user = '
            # try:
            #     for i in range(20): #up to 20 users with same name
            #         changeableStmt = stmt1 + "'" + str(getattr(self, 'user')) + str(i) + "'"
            #         if i == 0:
            #             changeableStmt = stmt1 + "'" + str(getattr(self, 'user')) + "'"
            #         with db_session:
            #             checkUser1 = getDB().select(changeableStmt)
            #         if checkUser1:
            #             continue
            #         elif len(str(getattr(self, 'user')) + str(i)) <= 10 and i > 0:
            #             setattr(self, 'user', str(getattr(self, 'user')) + str(i))
            #             break
            #         elif len(str(getattr(self, 'user')) + str(i)) > 10 and i > 0:
            #             return False
            #         elif i == 0:
            #             break
            # except:
            #     log.error(f'Cannot search for user. Wrong select: < {changeableStmt} >.')
            #     return False
        if hasattr(self, 'loginuser'):
            stmt2 =  stmt + 'loginuser = '
            # try:
            #     for i in range(20): #up to 20 users with same name
            #         changeableStmt = stmt2 + "'" + str(getattr(self, 'loginuser')) + str(i) + "'"
            #         if i == 0:
            #             changeableStmt = stmt2 + "'" + str(getattr(self, 'loginuser')) + "'"
            #         with db_session:
            #             checkUser2 = getDB().select(changeableStmt)
            #         if checkUser2:
            #             continue
            #         elif len(str(getattr(self, 'loginuser')) + str(i)) <= 64 and i > 0:
            #             setattr(self, 'loginuser', str(getattr(self, 'loginuser')) + str(i))
            #             break
            #         elif len(str(getattr(self, 'loginuser')) + str(i)) > 64 and i > 0:
            #             return False
            #         elif i == 0:
            #             break
            # except:
            #     log.error(f'Cannot search for loginuser. Wrong select: < {changeableStmt} >.')
            #     return False
        return True


    def convertAndValidData(self, table: str, timeFormats: Prompts, ignoreFieldValid: str) -> tuple[bool, None or str]:
        """
        Converts input data into right datatypes and valid the fields for the DB insert. 
        """
        with db_session:
            getValiData = select(
                v for v in Tables 
                if v.tables == table
                )[:]

        for validField in getValiData:
            for key, value in self.__dict__.items():
                if (validField.field == key):
                    try:
                        if validField.primarykey == 'J' and not value:
                            if ignoreFieldValid.strip() and key in ignoreFieldValid.split(','):
                                pass
                            else:
                                log.error(errorMsg[0].format(key,table,value))
                                return False, errorMsg[1].format(key)
                        elif validField.required == 'J' and not value:
                            if ignoreFieldValid.strip() and key in ignoreFieldValid.split(','):
                                pass
                            else:
                                log.error(errorMsg[2].format(key,table,value))
                                return False, errorMsg[3].format(key)
                        elif not validField.nullvalue and not value:
                            break

                        if (validField.type == DataTypes.INTEGER.value):
                            dataType = DataTypes.INTEGER.name
                            self.__dict__[key] = int(value)
                        elif validField.type == DataTypes.DATUM.value:
                            dataType = DataTypes.DATUM.name
                            if not value:
                                self.__dict__[key] = 0
                            else:
                                self.__dict__[key] = int(
                                    Date(datetime.strptime(
                                        value, 
                                        timeFormats.csvDateFormat
                                        )
                                    ))
                        elif validField.type == DataTypes.TIME.value:
                            dataType = DataTypes.TIME.name
                            if not value:
                                self.__dict__[key] = 0
                            else:
                                self.__dict__[key] = int(
                                    Time(datetime.strptime(
                                        value, 
                                        timeFormats.csvTimeFormat
                                        )
                                    ))
                        elif validField.type == DataTypes.TIMESPAN.value:
                            dataType = DataTypes.TIMESPAN.name
                            if not value:
                                self.__dict__[key] = 0
                            else:
                                self.__dict__[key] = int(
                                    Timespan(datetime.strptime(
                                        value, 
                                        timeFormats.csvTimeFormat
                                        )
                                    ))
                        elif validField.type == DataTypes.FLOAT.value:
                            dataType = DataTypes.FLOAT.name
                            if not value:
                                self.__dict__[key] = 0.0
                            else:
                                self.__dict__[key] = float(value)
                        elif validField.type == DataTypes.STRING.value:
                            if not value:
                                self.__dict__[key] = ' '

                        if len(str(self.__dict__[key])) > validField.length:
                            return False, errorMsg[4].format(key, validField.length)

                        break
                    except:
                        log.error(errorMsg[5].format(
                            key,
                            table,
                            value,
                            dataType,
                            type(value)
                            ))
                        return False, errorMsg[6].format(key)
        return True, None