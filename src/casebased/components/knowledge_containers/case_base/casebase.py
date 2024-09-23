from typing import Optional

import os
from pathlib import Path

import pandas as pd

from casebased.components.knowledge_containers.case_base.constants import (
    CBTypes,
    Extensions,
)
from casebased.components.knowledge_containers.ontology.attribute import (
    FeatureAttribute,
)
from casebased.components.knowledge_containers.ontology.vocabulary import Vocabulary


class CaseBase:
    """
    Case Base is a collection of cases.
    We create a case base from a file or from a list of cases.
    Then this is transformed into a dataframe and the rows are used to create cases.
    This case based can then be stored in a file and used for case based reasoning.
    """

    def __init__(self, df=None, path=None):
        self.df = df.copy()
        self.path: Path = path
        # add utility column and set it to 0 for all cases
        self.df["utility"] = 0

    def set_utility(self, row: int, utility: int):
        if row < 0 or row > len(self.df):
            raise ValueError("Row index out of bounds")
        if utility < 0:
            raise ValueError("Utility must be greater than 0")
        if not isinstance(utility, int):
            raise ValueError("Utility must be of type int")
        self.df.iloc[row]["utility"] = utility

    def clean_unused_cases(self):
        self.df = self.df[self.df["utility"] > 0]

    def add_case(self, case):
        self.df = self.df.append(case, ignore_index=True)

    def remove_case(self, case):
        pass

    def get_case(self, query):
        pass
