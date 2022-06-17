
from classes.readCreate import ReadAndInitCSVdata, ReadAndInitCSVdataWithoutHeader
from methods.prompts import Prompts
from util.lists_of_data_labels import whoFirstModifyList
from prog_functions.modifyAttrValueWithOther import modifyAttrValueWithOtherAttrValues
from prog_functions.ifValueInAttrThenValue import ifValueInAttrThenValue


def modifyFileData(csvData: ReadAndInitCSVdata or ReadAndInitCSVdataWithoutHeader, prop: Prompts) -> tuple[bool, None or str]:

        if not prop.whoFirstModify.strip(): # choose which function should happen first
            prop.whoFirstModify = whoFirstModifyList[0]
        count: int = 0
        while count <= 1:
            if (prop.whoFirstModify == whoFirstModifyList[0]) and prop.modifyAttrValueWithOtherAttrValues.strip():
                successful = modifyAttrValueWithOtherAttrValues( # give into fields values or edit the values in fields
                    data=csvData,
                    inputString=prop.modifyAttrValueWithOtherAttrValues
                    )
                if not successful[0]:
                    return False, successful[1]
                elif prop.ifValueInAttrThenValue.strip():
                    prop.whoFirstModify = whoFirstModifyList[1]
                    count += 1
                else:
                    count += 2
            elif (prop.whoFirstModify == whoFirstModifyList[1]) and prop.ifValueInAttrThenValue.strip():
                successful = ifValueInAttrThenValue( # If some value is in the field, what should happen with the value in another or same field. 
                    data=csvData,
                    inputString=prop.ifValueInAttrThenValue
                    )
                if not successful[0]:
                    return False, successful[1]
                elif prop.modifyAttrValueWithOtherAttrValues.strip():
                    prop.whoFirstModify = whoFirstModifyList[0]
                    count += 1
                else:
                    count += 2
            else:
                count += 1
        
        return True, None