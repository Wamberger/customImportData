
from enum import Enum


class CollectedTables():
    def __init__(self) -> None:
        pass


class DataTypes(Enum):
    INTEGER = 'I'
    FLOAT = 'F'
    DATUM  = 'D'
    TIME = 'T'
    TIMESPAN = 'H'
    STRING = 'C'