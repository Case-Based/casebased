from enum import Enum


class CBTypes(Enum):
    DF = "df"
    KD_TREE = "kd_tree"


class Extensions(Enum):
    SQL = ".sql"
    CSV = ".csv"
    EXCEL = ".xlsx"
    JSON = ".json"
    XML = ".xml"
