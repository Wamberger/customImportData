
from util.startLog import getLog


warningMsg = [
    'Not in the csvContent list: {} - {}',
    'Did not map the whole input data! The length of the list with titles: <{}>, may not be equal to the data length: <{}>.',
]


log = getLog(__name__)


class ReadAndInitCSVdata:
    '''
    Creates a class with wishing column names in 
    renamedCsvContent from csvContent label names. 
    Both list and data must be the same length.
    '''
    def __init__(
        self, 
        row: dict, 
        csvContent: list[str], 
        renamedCsvContent: list[str]
        ):
        
        for key, value in row.items():
            try:
                if key in csvContent:
                    for num, title in enumerate(csvContent):
                        if key == title.strip():
                            valueNewName = renamedCsvContent[num].strip().replace(' ', '_') # in case of title with space
                            setattr(self, valueNewName.lower(), value.strip())  # lower case for easier writting and reading
                            break
                else:
                    log.warning(warningMsg[0].format(key, value))
            except:
                log.warning(warningMsg[1].format(len(csvContent), len(row)))
                break


class ReadAndInitCSVdataWithoutHeader: 
    '''
    create a class with wished names according to the column.
    The renamedCsvContent list contains the label names of the columns.
    '''
    def __init__(self, row: list[str], renamedCsvContent: list[str]):
        for num, value in enumerate(row):
            try:
                valueNewName = renamedCsvContent[num].strip().replace(' ', '_') # in case of title with space
                setattr(self, valueNewName.lower(), value.strip()) # lower case for easier writting and reading
            except:
                log.warning(warningMsg[1].format(len(renamedCsvContent), len(row)))
                break  