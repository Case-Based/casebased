from pathlib import Path

import pandas as pd


class CaseBase:
    """
    Case Base is a collection of cases.
    We create a case base from a file or from a list of cases.
    Then this is transformed into a dataframe and the rows are used to create cases.
    This case based can then be stored in a file and used for case based reasoning.
    """

    def __init__(self, cases=pd.DataFrame(), path=None):
        self.cases = cases.copy()
        self.path: Path = path
        # add utility column and set it to 0 for all cases
        self.cases["utility"] = 0

    def set_utility(self, row: int, utility: int):
        if row < 0 or row > len(self.cases):
            raise ValueError("Row index out of bounds")
        if utility < 0:
            raise ValueError("Utility must be greater than 0")
        if not isinstance(utility, int):
            raise ValueError("Utility must be of type int")
        self.cases.iloc[row]["utility"] = utility

    def clean_unused_cases(self):
        self.cases = self.cases[self.cases["utility"] > 0]

    def add_case(self, case):
        self.cases = self.cases.append(case, ignore_index=True)

    def remove_case(self, case):
        pass

    def get_case(self, query):
        pass
