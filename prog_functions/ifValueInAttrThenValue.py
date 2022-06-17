
from classes.readCreate import ReadAndInitCSVdata, ReadAndInitCSVdataWithoutHeader
from util.readInputStringIndivDef import readInputStringIndivDef
from util.startLog import getLog


def ifValueInAttrThenValue(data: ReadAndInitCSVdata or ReadAndInitCSVdataWithoutHeader, inputString: str) -> tuple[bool, None or str]:
    '''
    Returns 'bool' and 'None' or 'errorMsg'. The 'data' object update without return it.

    Read and replace the data according to the individual wishes. 
    First param is key and the attribute (<fieldName>) which will be inspected with his value which is given 
    second param (<fieldNameValue>).
    When key and value appear in the object class "if statement", then the value from third param (<wantedValue>) will be inserted 
    into the attribute given in the fourth and last param (<newDestinationFieldName>).

    One input param/statement contains ALWAYS four 'params' separate with ?= and ?+ characters: 
    <fieldName>?=<fieldNameValue>?+<wantedValue>?+<newDestinationFieldName>!=
    Any new statement you write after already give statement: <fieldName>?=<fieldNameValue>?+<wantedValue>?+<newDestinationFieldName>!=<fieldName>?=...
    If you want to use the value from another attribute to give it into destination attribute (<newDestinationFieldName>), 
    then write with {{attr}} like:
    <fieldName>?=<fieldNameValue>?+<{{wantedFieldsValue}}>?+<newDestinationFieldName>!=
    When using values from other attributes, you can add new characters if you want. E.g. <possibleTextFront{{wantedFieldsValue}}orTextBack>

    IMPORTANT! Always needs to be at the end of the indivual wish/statement "!=" signs, even if there are no further statements.
    IMPORTANT! You can only use values from the 'data' attributes.
    WARNING! Input field accepts only 2000 characters.
    '''
    errorMsg = [
            'No value in input data attribute: {}. The value and attribut of {} was not initialised.',
            'The input data was not read correctly, cannot proceed further. Try to correct params: " {} ".',
            'The key/field: {}, needs three values, has: {}. Wrong params: {}'
        ]
    
    log = getLog(__name__)

    inputDataRead = readInputStringIndivDef(inputString)
    if not inputDataRead[0]:
        return False, inputDataRead[1]

    noneValue = 'None'
    sepChar: list = ['{{','}','{'] # new separate char
    for keys in inputDataRead[1]:
        try:
            for key, value in keys.items():
                if not len(value) == 3:
                    log.error(errorMsg[3].format(key, len(value), inputString))
                    return False, errorMsg[3].format(key, len(value), inputString)
                if hasattr(data, key) and (str(getattr(data, key)) == value[0]):
                    if not sepChar[0] in value[1] and noneValue != value[1]:
                        setattr(data, value[2], value[1])
                    elif not sepChar[0] in value[1] and noneValue == value[1]:
                        setattr(data, value[2], '')
                    else:
                        searchField: str = value[1]
                        extensionValueBack: str = ''
                        extensionValueFront: str = ''
                        if ((value[1].rfind(sepChar[1]) + 1) != len(value[1])):
                            extensionValueBack = value[1]
                            extensionValueBack = extensionValueBack[value[1].rfind(sepChar[1]) + 1:]
                            searchField = searchField[:value[1].rfind(sepChar[1]) - 1]
                        else:
                            searchField = searchField.replace(sepChar[1], '')
                        if (value[1].rfind(sepChar[2]) != 1):
                            extensionValueFront = value[1]
                            extensionValueFront = extensionValueFront[:value[1].rfind(sepChar[2]) - 1]
                            searchField = searchField[value[1].rfind(sepChar[2]) + 1:]
                        else:
                            searchField = searchField.replace(sepChar[2], '')

                        if hasattr(data, searchField) and getattr(data, searchField):
                            if not extensionValueFront and not extensionValueBack:
                                setattr(data, value[2], getattr(data, searchField))
                            else:
                                setattr(
                                    data, 
                                    value[2], 
                                    (extensionValueFront + str(getattr(data, searchField)) + extensionValueBack)
                                    )
                        else:
                            log.error(errorMsg[0].format(searchField, value[2]))
                            return False, errorMsg[0].format(searchField, value[2])
        except:
            log.error(errorMsg[1].format(inputString))
            return False, errorMsg[1].format(inputString)
    return True, None