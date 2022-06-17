
def findDateFormat(date: str) -> str:
    '''
    Try to find the right format for datetime convert.
    '''
    characters: str = '.-/'
    formatType: str = ''
    numPos: list = []
    for char in date:
        numPos.append(char)
    for c in characters:
        if c in date:
            if len(date) == 10:
                if (numPos[2] == c) and (numPos[5] == c):
                    formatType = '%d' + c + '%m' + c + '%Y'
                elif (numPos[5] == c) and (numPos[7] == c):
                    formatType = '%Y' + c + '%m' + c + '%d'
                break
            if len(date) == 7:
                if (numPos[2] == c):
                    formatType = '%m' + c + '%Y'
                elif (numPos[4] == c):
                    formatType = '%Y' + c + '%m'
                break
        if len(date) == 8: # only until 2099
            if (numPos[0] == '2') and (numPos[1] == '0'):
                formatType = '%Y%m%d'
            if (numPos[4] == '2') and (numPos[5] == '0'):
                formatType = '%d%m%Y'
            break
    return formatType