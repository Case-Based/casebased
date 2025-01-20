from pathlib import Path

import pandas as pd

# TODO Room for improvements
"""
Some potential improvements or considerations:

Duplicate Case Handling: 
The _drop_duplicate_cases method could be improved to handle cases where the list of columns to ignore (dataToIgnore) is empty or not provided.


Error Handling: 
The update_case method could be further improved by handling additional exceptions and providing more detailed error messages.


Serialization and Deserialization: 
The class could benefit from methods to save and load the case base to/from a file, which would improve persistence and portability.


Extensibility: 
The class could be designed to be more extensible, e.g., by allowing custom case structures or providing hooks for adding new functionality.
"""


class CaseBase:
    """
    Case Base is a collection of cases.
    We create a case base from a file or from a list of cases.
    Then this is transformed into a dataframe and the rows are used to create cases.
    This case based can then be stored in a file and used for case based reasoning.
    """

    def __init__(self, cases=pd.DataFrame(), path=None):
        if cases is None:
            raise ValueError("Case base cannot be None")
        self.cases = cases.copy()
        self.path: Path = path
        if "utility" not in self.cases or self.cases["utility"] is None:
            self.cases["utility"] = 0

    def add_case(self, case: dict) -> None:
        """
        Public function
        Adds a case to the case base

        Parameters:
        case: dict - the case to be added to the case base
        """

        if "utility" not in case or case["utility"] is None:
            case["utility"] = 0

        if not self._verify_case_structure(case):
            raise ValueError("Case structure does not match dataframe structure")

        single_case = pd.DataFrame(case, index=[0])
        self.cases = self.cases._append(single_case, ignore_index=True)

    def add_list_of_cases(self, cases: list) -> None:
        """
        Public function
        Adds a list of cases to the case base

        Parameters:
        cases: list - the list of cases to be added to the case base
        """
        for case in cases:
            if "utility" not in case or case["utility"] is None:
                case["utility"] = 0

            if not self._verify_case_structure(case):
                raise ValueError("Case structure does not match dataframe structure")

            single_case = pd.DataFrame(case, index=[0])
            self.cases = self.cases._append(single_case, ignore_index=True)

    def update_case(self, case_index: int, updated_case: dict):
        """
        Public function
        Updates a case in the case base.

        Parameters:
        case_index: int - the index of the case to be updated
        updated_case: dict - the updated case

        Returns:
        bool - True if the update was successful, False otherwise
        """

        try:
            # Check if index is within valid range
            if not (0 <= case_index < len(self.cases)):
                raise IndexError(
                    f"Case with index {case_index} not found. Valid indices are from 0 to {len(self.cases) - 1}."
                )

            # Verify that the structure of the updated case is correct
            if not self._verify_case_structure(updated_case):
                raise ValueError(
                    "The updated case structure is invalid and does not match the case base structure."
                )

            # Update case values
            for key, value in updated_case.items():
                if key not in self.cases.columns:
                    raise KeyError(f"Column '{key}' does not exist in the case base.")
                self.cases.at[case_index, key] = value

            return True

        except IndexError as e:
            print(f"Index Error: {e}")
            return False
        except KeyError as e:
            print(f"Key Error: {e}")
            return False
        except ValueError as e:
            print(f"Value Error: {e}")
            return False
        except TypeError as e:
            print(
                f"Type Error: {e} - Ensure 'case_index' is an integer and 'updated_case' is a dictionary."
            )
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def prune(self, threshold: int) -> None:
        """
        Public function
        Prunes the case base by removing cases with a utility below the threshold

        Parameters:
        threshold: int - the utility threshold
        """
        self.cases = self.cases[self.cases["utility"] >= threshold]

    def get_current_casebase(self):
        """
        Public function
        Returns the current case base
        """
        return self.cases

    def remove_case_by_index(self, index: int) -> None:
        """
        Public function
        Removes a case from the case base by index.

        Parameters:
        index: int - the index of the case to be removed

        Raises:
        ValueError: If the index is not valid for the current case base.
        TypeError: If the index is not an integer.
        """

        # Check if the index is an integer
        if not isinstance(index, int):
            raise TypeError("Index must be an integer")

        # Check if the index exists in the DataFrame
        if index not in self.cases.index:
            raise ValueError(f"Index {index} not found in the case base")

        # Drop the specified index and reset the index in-place
        self.cases.drop(index=index, inplace=True)
        self.cases.reset_index(drop=True, inplace=True)

    def remove_case_by_case(self, case: dict) -> None:
        """
        Public function
        Removes a case from the case base

        Parameters:
        case: dict - the case to be removed
        """

        mask = True
        for key, value in case.items():
            if key in self.cases.columns:
                mask = mask & (self.cases[key] == value)

        self.cases = self.cases[~mask].reset_index(drop=True)

    def clean_up_casebase(self, col_to_ignore: list = None) -> None:
        """
        Public functin

        Removes cases with missing as well as drops duplicate cases fromt the case base

        Params:
        List of coloumns that need to be ignored when identifying duplicates
        """

        if col_to_ignore is None:
            col_to_ignore = []
        elif not isinstance(col_to_ignore, list):
            raise ValueError("col_to_ignore must be a list")

        # Perform the cleanup operations
        self._drop_duplicate_cases(col_to_ignore)
        self._remove_cases_with_missing_values()

        self.cases.reset_index(drop=True, inplace=True)

    # Private functions

    def _get_index_of_case(self, case: dict) -> int:
        """
        Private function
        Gets the index of a case in the case base

        Parameters:
        case: dict - the case to find

        Returns:
        int - the index of the case
        """
        mask = True
        for key, value in case.items():
            if key in self.cases.columns:
                mask = mask & (self.cases[key] == value)
        matching_indices = self.cases[mask].index
        if len(matching_indices) > 0:
            return matching_indices[0]
        raise ValueError("Case not found in case base")

    def _set_utility(self, row: int, utility: int):
        # Should we really do this manually or should this functio be called inside the retriever component

        if row < 0 or row > len(self.cases):
            raise ValueError("Row index out of bounds")
        if utility < 0:
            raise ValueError("Utility must be greater than 0")
        if not isinstance(utility, int):
            raise ValueError("Utility must be of type int")
        self.cases.iloc[row]["utility"] = utility

    def _verify_case_structure(self, case: dict) -> bool:
        """
        Private function
        Verifies the structure of a case

        Parameters:
        case: dict - the case to be verified
        """

        if set(case.keys()) == set(self.cases.columns):
            return True
        else:
            return False

    def _get_index_of_case(self, value: int):
        """
        Private function
        Returns the index of a case with a specific value

        Parameters:
        value: int - the value to search for
        """

        indexes = []
        for column in self.cases.columns:
            column_indexes = self.cases.index[self.cases[column] == value].tolist()
            indexes.extend(column_indexes)
        return sorted(set(indexes))

    def _remove_cases_with_missing_values(self):
        """
        Private function
        Removes cases with missing values
        """

        self.cases.dropna(inplace=True)
        return self.cases

    def _raise_error_if_casebase_is_None(self):
        """
        Private function
        Raises an error if the case base is None
        """
        if self.cases is None:
            raise ValueError("DataError: Case base is None")
        return

    def _drop_duplicate_cases(self, dataToIgnore: list = None) -> None:
        """
        Private function
        Drops duplicate cases from the case base.

        Parameters:
        dataToIgnore: list - List of columns to ignore when identifying duplicates.
                            If None or empty, all columns are considered.
        """

        if dataToIgnore is None:
            dataToIgnore = []

        columns = self.cases.columns
        dataToConsider = (
            [col for col in columns if col not in dataToIgnore]
            if dataToIgnore
            else columns
        )

        self.cases = self.cases.drop_duplicates(
            subset=dataToConsider, keep="first", inplace=False, ignore_index=True
        )

    def _fill_missing_values_with_zero(self):
        """
        Private function
        Fills missing (NaN) values in the case base with 0.
        """
        self.cases.fillna(0, inplace=True)
        return self.cases
