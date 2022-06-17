
def readInputStringIndivDef(inputString: str) -> tuple[bool, list[dict] or str]:
    '''
    Read the string and seperate characters. Returns 'bool' and 'inputDataRead' a list of dict or 'errorMsg'.
    All characters which have in the end separator ?= became key in dictionary. 
    All other characters will be separated if they have at the end ?+ and add to the list of the key (characters with ?= in the end).
    One dictionary with values in list is complited when the last set of characters have at the end: != 

    Separators:
    ?= (key)
    ?+ (values added in list)
    != (end of statement or one order)

    Examples:
    <fieldName>?=<fieldNameValue>?+<wantedValue>?+<newDestinationFieldName>!=
    or
    <fieldDestination>?=<fieldWishToUseValue>?+<fieldWishToUseValue>?^<modifyParam>!=
    or with more statements:
    <fieldName>?=<fieldNameValue>?+<wantedValue>?+<newDestinationFieldName>!=<fieldName>?=<fieldNameValue>?+<wantedValue>?+<newDestinationFieldName>!=<fieldName>?=...

    IMPORTANT! Always needs to be at the end of the indivual wish/statement "!=" signs, even if there are no further statements.
    WARNING! Input field accepts only 2000 characters.
    '''
    errorMsg = [
            'The input params are wrong. Cannot read: "{}". Try: " <fieldName>?=<fieldNameValue>?+<wantedValue>?+<newDestinationFieldName>!= " \
            or try: " <fieldDestination>?=<fieldWishToUseValue>?+<fieldWishToUseValue>?^<modifyParam>!= ".'
        ]

    sepChar: list = ['?','=','+','!'] # allowed, but not allowed in combination with ? (e.g. ?+). Also not allowed: != but allowed ?!. 
    oldChar: str = ''
    checkedInputChar: str = ''
    inputDataRead: list = []
    newKey: dict = {}
    keyName: str = ''
    try:
        for char in inputString:
            if char in sepChar:
                if oldChar not in sepChar:
                    oldChar = char
                    checkedInputChar = checkedInputChar + char
                elif (sepChar[0] == oldChar) and (sepChar[1] == char):
                    oldChar = char            
                    keyName = checkedInputChar[:-1]
                    newKey[checkedInputChar[:-1]] = []
                    checkedInputChar = ''
                elif (sepChar[0] == oldChar) and (sepChar[2] == char):
                    oldChar = char
                    newKey[keyName] += [checkedInputChar[:-1]]
                    checkedInputChar = ''
                elif (sepChar[3] == oldChar) and (sepChar[1] == char):
                    oldChar = char
                    newKey[keyName] += [checkedInputChar[:-1]]
                    inputDataRead.append(newKey)
                    newKey = {}
                    keyName = ''
                    checkedInputChar = ''
            else:
                oldChar = char
                checkedInputChar = checkedInputChar + char
        if checkedInputChar:
            return False, errorMsg[0].format(inputString)
        return True, inputDataRead
    except:
        return False, errorMsg[0].format(inputString)