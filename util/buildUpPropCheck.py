
from methods.prompts import Prompts


def buildUpPropCheck(prop: Prompts) -> tuple[bool, list[str] or None, list[str] or str]:
    '''
    Check header prop. 
    '''

    if prop.dictReader and prop.csvContent.strip() and prop.renamedCsvContent.strip():
        csvContent = prop.csvContent.split(';')
        renamedCsvContent = prop.renamedCsvContent.split(';')
    elif not prop.dictReader and not prop.csvContent.strip() and prop.renamedCsvContent.strip():
        csvContent = None
        renamedCsvContent = prop.renamedCsvContent.split(';')
        return True, csvContent, renamedCsvContent
    else:
        return False, 'No headers were defined.'
        
    return True, csvContent, renamedCsvContent
