
from util.startLog import getLog
from classes.util_classes import CollectedTables
from methods.prompts import Prompts
from requests import Session
#from <path> import (
#    environ_loginPassword, 
#    environ_loginUser,
#    environ_url
#    )


def restCall(tableProp: list[dict or list], insertTables: CollectedTables, prop: Prompts) -> tuple[bool, dict or None]:
    '''
    REST-API: from defined properties creates headers and string based on json format for post.
    '''

    log = getLog(__name__)
    restProp = tableProp[7]

    tablesForInsert: list = []
    for getTable in restProp:
        if getTable != 'rest-api':
            tablesForInsert.append(getTable)

    restApiProp = restProp['rest-api']
    #try:
    #    loginUrl = environ_url + restApiProp['loginUrl']
    #    headerLogin = restApiProp['headerLogin']
    #    url = environ_url +  restApiProp['url']
    #    header = restApiProp['header']
    #    loginData = {
    #        restApiProp['loginUsername']: environ_loginUser,
    #        restApiProp['loginPassword']: environ_loginPassword
    #        }
    #except:
    #    log.error('Rest-Api: environment variables or properties are wrong.')
    #    return False, None

    collectData: dict = {}
    try:
        for table in tablesForInsert:
            getDict = insertTables.__dict__[table]
            for field in restProp[table]:
                if field == 'all':
                    collectData.update(getDict.__dict__)
                else:
                    collectData.update({field : getDict.__dict__[field]})
    except:
        log.error('Rest-Api: Cannot create dict of data.')
        return False, None

    jsonData: str = '{'
    for key, value in collectData.items():
        if len(jsonData) > 1:
            jsonData = jsonData + ', '
        jsonData = jsonData + '"' + key + '": ' 
        if key == restApiProp['special']:
            jsonData = jsonData + '[' + str(value) + ']'
        elif isinstance(value, float) or isinstance(value, int):
            jsonData = jsonData + str(value)
        else:
            jsonData = jsonData + '"' + str(value) + '"'
    jsonData = jsonData + '}'

    session = Session()
    #response = session.post(
    #    loginUrl, 
    #    headers=headerLogin,
    #    allow_redirects=True, 
    #    params=loginData
    #    )
    #if response.status_code != 200:
    #    log.error('Rest-Api: login was NOT successful. Wrong params: loginUrl < {} >, headerLogin < {} >, loginData < {} >.'.format(
    #        loginUrl,
    #        headerLogin,
    #        loginData
    #        )
    #    )   

    if not prop.testRun:
        response = session.post(
            url, 
            data=jsonData, 
            headers=header
            )
        if response.status_code == 200:
            log.error('Rest-Api: update/Insert was successful. Wrong params: jsonData < {} >, header < {} >.'.format(
                jsonData,
                header
                )
            )
            return True, restProp
        else:
            log.error('Rest-Api: update/Insert was NOT successful. Update data: < {} >'.format(jsonData))
            return False, None
    else:
        log.info('#Test run# Rest-Api: update/Insert would be carried out. Params: < {} >'.format(jsonData))
        return True, restProp