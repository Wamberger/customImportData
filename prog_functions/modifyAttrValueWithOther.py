
import re
#from unidecode import unidecode
from datetime import datetime
from classes.readCreate import ReadAndInitCSVdata, ReadAndInitCSVdataWithoutHeader
from util.readInputStringIndivDef import readInputStringIndivDef
from util.findDateFormat import findDateFormat
from util.startLog import getLog


def modifyAttrValueWithOtherAttrValues(data: ReadAndInitCSVdataWithoutHeader or ReadAndInitCSVdata, inputString: str) -> tuple[bool, None or str]:
    '''
    Returns 'bool' and 'None' or 'errorMsg'. The 'data' object update without return it.

    Read and fill the given fields/attributes with the individual wishes.
    One input param/statement is separate with ?= and ?+ characters and always needs to end with !=: 
    <fieldDestination>?=<fieldWishToUseValue>?+<fieldWishToUseValue>?^<modifyParam>!=

    The first param (<fieldDestination>) is the attribute to which we want to put the value from 
    other attributes/fields (<fieldWishToUseValue>). One or more attributes follow with addition operator. 
    If you want 'space', you need to enter 'space' as own value (e.g. "...?+ ?+...").

    The values of the used attributes (<fieldWishToUseValue>) can be modified with additional params which 
    are separated with ?^ (<fieldWishToUseValue>?^<modifyParam>). 
    With modification parameter (<modifyParam>) you can slice the string (digits, e.g. 2 gives you first two characters), 
    change date formats written in string (datetime rules, e.g. %Y-%m-%d) or make letter to be 'upper', 'lower' or 'title'.
    You can also unidecode characters (ß = ss, ä = a, č = c, ň = n, etc.) or use Python functions: replace() or sub().
    IMPORTANT! It can be only used one <modifyParam> per value. 

    IMPORTANT! Always needs to be at the end of the indivual wish/statement "!=" signs, even if there are no further statements.
    IMPORTANT! You can only modify the values from the 'data' attributes.
    WARNING! Input field accepts only 2000 characters.
    '''
    errorMsg = [
        'Wrong params. " {} " is no allowed modifier parameter (?^). Error with value: {} . Try: " ?^<numberSlice> " or " ?^<datetimeFormat> ".',
        'The attribute: {}, does not exist. Because it was not read from the input file. Look the params.',
        'Entirely wrong params! The error input: {}',
        'No or wrong params definition for key\field: {}'
    ]

    log = getLog(__name__)

    inputDataRead = readInputStringIndivDef(inputString)
    if not inputDataRead[0]:
        return False, inputDataRead[1]

    sepChar = ['?^','(',',',')']
    replaceModification: list = ['replace','sub']
    letterModification: list = ['upper','lower','title']
    modifyChar: list = ['unidecode']
    for fields in inputDataRead[1]:
        for key, value in fields.items():
            compileValues: str = ''
            for v in value:
                if hasattr(data, v) and getattr(data, v):
                    compileValues = compileValues + str(getattr(data, v))
                elif hasattr(data, v) and not getattr(data, v):
                    compileValues = compileValues + ''
                elif sepChar[0] in v:
                    modifyRule = v[v.rfind(sepChar[0]) + 2:]
                    newValue = v[:v.rfind(sepChar[0])]
                    if hasattr(data, newValue) and not getattr(data, newValue): # can also have no value: ''
                        compileValues = compileValues + ''
                    elif hasattr(data, newValue) and getattr(data, newValue):
                        tmpValue = getattr(data, newValue)
                        if modifyRule.isdigit():
                            compileValues = compileValues + tmpValue[:int(modifyRule)]
                        elif not modifyRule.isdigit() \
                        and not modifyRule[:modifyRule.rfind(sepChar[1])] in replaceModification \
                        and not modifyRule in modifyChar \
                        and modifyRule in letterModification:
                            if modifyRule == letterModification[0]:
                                compileValues = compileValues + tmpValue.upper()
                            elif modifyRule == letterModification[1]:
                                compileValues = compileValues + tmpValue.lower()
                            elif modifyRule == letterModification[2]:
                                compileValues = compileValues + tmpValue.title()
                        elif not modifyRule.isdigit()\
                        and not modifyRule in letterModification\
                        and not modifyRule in modifyChar \
                        and modifyRule[:modifyRule.rfind(sepChar[1])] in replaceModification:
                            removeValue = modifyRule[modifyRule.rfind(sepChar[1]) + 1 : modifyRule.rfind(sepChar[2])]
                            replaceValue = modifyRule[modifyRule.rfind(sepChar[2]) + 1 : modifyRule.rfind(sepChar[3])]
                            if modifyRule[:modifyRule.rfind(sepChar[1])] == replaceModification[0]:
                                compileValues = compileValues + tmpValue.replace(removeValue, replaceValue)
                            elif modifyRule[:modifyRule.rfind(sepChar[1])] == replaceModification[1]:
                                compileValues = compileValues + re.sub(removeValue, replaceValue, tmpValue)
                        elif not modifyRule.isdigit() \
                        and not modifyRule[:modifyRule.rfind(sepChar[1])] in replaceModification \
                        and not modifyRule in letterModification \
                        and modifyRule in modifyChar:
                            #compileValues = compileValues + unidecode(tmpValue) #original
                            compileValues = compileValues + tmpValue
                        elif not modifyRule.isdigit() \
                        and not modifyRule[:modifyRule.rfind(sepChar[1])] in replaceModification \
                        and not modifyRule in modifyChar \
                        and not modifyRule in letterModification: # Date can also be 01.01.2022 what is not digit
                            try:
                                getFormatType = findDateFormat(tmpValue)
                                tmpValue = datetime.strptime(tmpValue, getFormatType)
                                compileValues = compileValues + tmpValue.strftime(modifyRule)
                            except:
                                log.error(errorMsg[0].format(modifyRule, v))
                                return False, errorMsg[0].format(modifyRule, v)
                        else:
                            log.error(errorMsg[0].format(modifyRule, v))
                            return False, errorMsg[0].format(modifyRule, v)
                    else:
                        log.error(errorMsg[2].format(v))
                        return False, errorMsg[2].format(v)
                else:
                    compileValues = compileValues + v
            if compileValues:
                setattr(data, key, compileValues)
            else:
                for v in value:  # for empty values: ''
                    newV: str = v
                    if sepChar[0] in v:
                        newV = v[:v.rfind(sepChar[0])]
                    if hasattr(data, newV) and not getattr(data, newV):
                        setattr(data, key, '')
                    else:
                        log.error(errorMsg[3].format(key))
                        return False, errorMsg[3].format(key)
    return True, None