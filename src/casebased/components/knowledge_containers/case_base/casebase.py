import os
from pathlib import Path

import pandas as pd
from pandas._typing import FilePath

from casebased.components.knowledge_containers.case_base.constants import (
    CBTypes,
    Extensions,
)


class CaseBase:
    def __init__(self, data=None, cb_type=None, source: FilePath = None):
        self.data = data
        self.cb_type = cb_type
        self.source: Path = source

        # Hier würde ich sagen fangen wir erstmal mit Dataframes an
        # Dann können wir später noch KD-Trees implementieren
        if cb_type == CBTypes.DF.value or cb_type == CBTypes.DF and self.data is None:
            extension = os.path.splitext(source)[-1]
            if extension == Extensions.CSV.value:
                self.data = pd.read_csv(source)
            elif extension == Extensions.EXCEL.value:
                self.data = pd.read_excel(source)
            elif extension == Extensions.JSON.value:
                self.data = pd.read_json(source)
            elif extension == Extensions.XML.value:
                self.data = pd.read_xml(source)
            elif extension == Extensions.SQL.value:
                self.data = pd.read_sql(source)
            else:
                raise ValueError("No valid file extension")
        elif cb_type == CBTypes.KD_TREE:
            pass

    def clean_unused_cases(self):
        pass

    def add_case(self, case):
        pass

    def remove_case(self, case):
        pass

    def get_case(self, query):
        pass
