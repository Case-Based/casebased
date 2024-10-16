import os
from pathlib import Path
import pandas as pd

# Short description: This class is the main class for the case base. It is responsible for storing the cases and managing them.
# Data is being stored in a pandas dataframe. The class provides methods to add and remove cases from the case base.
from constants import CBTypes, Extensions

# from casebased.components.knowledge_containers.case_base.constants import (
#     CBTypes,
#     Extensions,
# )


class CaseBase:

    def __init__(self, data=None, cb_type=None, source=None):

        self.data = data
        self.cb_type = cb_type
        self.source: Path = source

        # TODO for later: implement KNN

        if cb_type == CBTypes.DF.value or cb_type == CBTypes.DF and self.data is None:
            extension = os.path.splitext(source)[-1]

            if extension == Extensions.CSV.value:
                self.data = pd.read_csv(source)
                self._create_util_row()
            elif extension == Extensions.EXCEL.value:
                self.data = pd.read_excel(source)
                self._create_util_row()
            elif extension == Extensions.JSON.value:
                self.data = pd.read_json(source)
                self._create_util_row()
            elif extension == Extensions.XML.value:
                self.data = pd.read_xml(source)
                self._create_util_row()
            elif extension == Extensions.SQL.value:
                self.data = pd.read_sql(source)
                self._create_util_row()
            else:
                raise ValueError("No valid file extension")
        elif cb_type == CBTypes.KD_TREE:
            pass

    def _create_util_row(self) -> pd.DataFrame:
        self.data["utils"] = 0
        return self.data
    
    def _increase_util(self, case_index: int) -> bool:
        pass

    def verfiy_case_structure(self, case: dict) -> bool:

        if set(case.keys()) == set(self.data.columns):
            return True
        else:
            return False

    def get_index_of_case(self, value: int):

        indexes = []
        for column in self.data.columns:
            column_indexes = self.data.index[self.data[column] == value].tolist()
            indexes.extend(column_indexes)
        return sorted(set(indexes))

    def add_case(self, case: dict):
        if set(self.data) != set(case):
            raise ValueError("Case structure does not match dataframe structure")

        single_case = pd.DataFrame(case, index=[0])
        self.data = self.data._append(single_case, ignore_index=True)
        return self.data

    def delete_case_by_index(df: pd.DataFrame, index: int) -> pd.DataFrame:

        if index not in df.index:
            raise ValueError(f"Index {index} not found in DataFrame")

        df = df.drop(index)
        return df.reset_index(drop=True)

    def update_case(self, case_index: int, updated_case: dict):
        try:
            # Validate index range
            if case_index < 0 or case_index >= len(self.data):
                raise IndexError(f"Case with index {case_index} not found")

            # Uncomment if this method exists and should verify the structure
            # if not self.verify_case_structure(updated_case):
            #     raise ValueError(f"Updated case structure is invalid")

            # Update the case
            for key, value in updated_case.items():
                if key in self.data.columns:
                    self.data.at[case_index, key] = value
                else:
                    raise KeyError(f"Column {key} does not exist in the dataframe")

            return True

        except IndexError as e:
            print(f"Error updating case: {e}")
            return False
        except KeyError as e:
            print(f"Error updating case: {e}")
            return False
        except ValueError as e:
            print(f"Error updating case: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred while updating case: {e}")
            return False

    def remove_cases_with_missing_values(self):
        for column in self.data.columns:
            if self.data is None:
                self.data.dropna(inplace=True)

        return self.data

    def drop_duplicate_cases(self, dataToIgnore: list):
        columns = self.data.columns
        dataToConsider = [element for element in columns if element not in dataToIgnore]
        self.data = self.data.drop_duplicates(
            subset=dataToConsider, keep="first", inplace=False, ignore_index=False
        )
        return

    def fill_missing_values_with_zero(self):
        df_filled = self.data.fillna(0)
        return df_filled

    def get_case_base(self):
        return self.data
