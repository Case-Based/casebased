from typing import Callable, Optional

import csv
import os
from pathlib import Path

import pandas as pd
from casebased.components.casebase.casebase import CaseBase


class DataSourceAdapter:

    def __init__(self, file_path: str):
        """
        Initialize the DataSourceAdapter with a CaseBase instance

        Parameters:
        path to the file that needs to be read
        """

        self.path = file_path

        self.supported_extensions = {
            ".csv": self._read_csv_file,
            ".json": self._read_json_file,
            ".xlsx": self._read_excel_file,
            ".xls": self._read_excel_file,
        }

    def read_file(self) -> Optional[pd.DataFrame]:
        """
        Public function to read a file based on its extension


        Returns:
        Optional[pd.DataFrame]: DataFrame containing the file data or None if reading fails

        Raises:
        ValueError: If the file extension is not supported
        """
        try:
            # Get the file extension (including the dot)
            _, file_extension = os.path.splitext(self.path.lower())

            # Check if the file exists
            if not os.path.exists(self.path):
                print(f"Error: File {self.path} not found")
                return None

            # Check if we support this file type
            if file_extension not in self.supported_extensions:
                supported_formats = ", ".join(self.supported_extensions.keys())
                raise ValueError(
                    f"Unsupported file format: {file_extension}. "
                    f"Supported formats are: {supported_formats}"
                )

            # Call the appropriate read function
            read_function = self.supported_extensions[file_extension]
            return read_function(self.path)

        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return None

    # Private Functions

    def _read_csv_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Public function to read a CSV file and populate the case base with the data

        Parameters:
        file_path (str): The path to the CSV file

        Returns:
        Optional[pd.DataFrame]: DataFrame with the CSV data or None if file not found
        """
        try:
            dataframe = pd.read_csv(file_path)
            return dataframe
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
            return None
        except pd.errors.EmptyDataError:
            print(f"Error: File {file_path} is empty")
            return None
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            return None

    def _read_json_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Public function to read a JSON file and populate the case base with the data

        Parameters:
        file_path (str): The path to the JSON file

        Returns:
        Optional[pd.DataFrame]: DataFrame with the JSON data or None if file not found
        """
        try:
            dataframe = pd.read_json(file_path)
            return dataframe
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
            return None
        except ValueError:
            print(f"Error: Invalid JSON format in file {file_path}")
            return None
        except Exception as e:
            print(f"Error reading JSON file: {str(e)}")
            return None

    def _read_excel_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Public function to read an Excel file and populate the case base with the data

        Parameters:
        file_path (str): The path to the Excel file

        Returns:
        Optional[pd.DataFrame]: DataFrame with the Excel data or None if file not found
        """
        try:
            dataframe = pd.read_excel(file_path)
            return dataframe
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
            return None
        except Exception as e:
            print(f"Error reading Excel file: {str(e)}")
            return None

    def add_utility_column(self):
        """
        Public function to add a utility column to the datasource itself (e.g. a csv file)

        Structure:
        Column1 | Column2 | ... | utility
        Value1  | Value2  | ... | 0
        Value1  | Value2  | ... | 0

        Paraemters:

        """

        try:

            with open(self.path, "a") as file:

                file.write("utility\n")
                file.write("0\n")

                file.close()

        except (FileExistsError, FileNotFoundError):

            print(
                "Enteres file path could not be found. Modify the location and try again!"
            )
            raise (FileExistsError, FileNotFoundError)

    def update_data_source(self, case_base: CaseBase) -> None:
        """
        Updates the original data source file with the current state of the case base.

        Parameters:
        case_base (CaseBase): The case base instance containing the modified data.
        """
        if not isinstance(case_base, CaseBase):
            raise ValueError("Provided object is not an instance of CaseBase")

        # Get the current state of the case base
        updated_cases = case_base.cases

        # Write the updated cases back to the file
        _, file_extension = os.path.splitext(self.path.lower())
        if file_extension == ".csv":
            updated_cases.to_csv(self.path, index=False)
        elif file_extension in [".xlsx", ".xls"]:
            updated_cases.to_excel(self.path, index=False)
        elif file_extension == ".json":
            updated_cases.to_json(self.path, orient="records", lines=True)
        else:
            raise ValueError(
                f"Unsupported file format for writing: {file_extension}. "
                "Supported formats are: .csv, .json, .xlsx, .xls"
            )
