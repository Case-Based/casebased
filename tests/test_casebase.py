# from src.casebased.components.knowledge_containers.case_base import casebase
from casebased.components.knowledge_containers.case_base.casebase import CaseBase
case_base = CaseBase()
# import unittest
import pytest 
import pandas as pd
from io import StringIO
from pathlib import Path
import tempfile
from pandas._typing import FilePath
from casebased.components.knowledge_containers.case_base.constants import CBTypes, Extensions



class TestCaseBase:

    csv_file_path_setup = Path('test_data/regenSetup.csv')
    csv_file_path = Path('test_data/regen.csv')
    csv_file_path_duplicate = Path('test_data/regenDuplicate.csv')

    def test_setUp(self):

        
        data = { 
            'Fallnummer': [1, 2, 3, 4],
            'Temperatur': [22.5, 20.0, 25.0, 30.0],
            'Luftfeuchtigkeit': [85, 60, 90, 50],
            'Luftdruck': [1012, 1015, 1009, 1010],
            'Windgeschwindigkeit': [15, 10, 20, 5],
            'Laengengrad': [13.404954, 11.581981, 9.993682, 8.682127],
            'Breitengrad': [52.520008, 48.135125, 53.551086, 50.110924],
            'Regen': [1, 0, 1, 0]
        }
        
        case_base1 = CaseBase(cb_type=CBTypes.DF.value, source=self.csv_file_path_setup)
        case_base2 = pd.DataFrame(data=data)        

        self.assertTrue(case_base2.equals(case_base1.data))

    def test_verify_case_structure(self):

        case_base = CaseBase(cb_type=CBTypes.DF.value, source=self.csv_file_path_setup)

        case1 = {
            'Fallnummer': 1,
            'Temperatur': 22.5,
            'Luftfeuchtigkeit': 85,
            'Luftdruck': 1012,
            'Windgeschwindigkeit': 15,
            'Laengengrad': 13.404954,
            'Breitengrad': 52.520008,
            'Regen': 1
        }

        case2 = {
            'Temperatur': 22.5,
            'Luftfeuchtigkeit': 85,
            'Luftdruck': 1012,
            'Windgeschwindigkeit': 15,
            'Laengengrad': 13.404954,
            'Breitengrad': 52.520008,
            'Regen': 1
        }

        result1 = case_base.verfiy_case_structure(case1)
        result2 = case_base.verfiy_case_structure(case2) 
        self.assertTrue(result1)
        self.assertFalse(result2)

    def test_get_index_case(self):

        case_base = CaseBase(cb_type=CBTypes.DF.value, source=self.csv_file_path_setup)

        value_to_find = 20.0
        positions = case_base.get_index_of_case(value_to_find)
        self.assertEqual(positions, [1, 2])

    def test_add_case(self):
        
        case_base = CaseBase(cb_type=CBTypes.DF.value, source=self.csv_file_path_setup)
        new_case = {
            "Fallnummer": 5, 
            "Temperatur": 20.0, 
            "Luftfeuchtigkeit": 1, 
            "Luftdruck": 1,
            "Windgeschwindigkeit": 1, 
            "Laengengrad": 1, 
            "Breitengrad": 1, 
            "Regen": 1
        }
        
        case_base.add_case(new_case)

        last_row = case_base.data.iloc[-1]

        expected_values = {
            "Fallnummer": 5, 
            "Temperatur": 20.0, 
            "Luftfeuchtigkeit": 1, 
            "Luftdruck": 1,
            "Windgeschwindigkeit": 1, 
            "Laengengrad": 1, 
            "Breitengrad": 1, 
            "Regen": 1
        }

        for column, expected_value in expected_values.items():
            self.assertEqual(last_row[column], expected_value)

    def test_remove_case_with_missing_value(self): 

        case_base = CaseBase(cb_type=CBTypes.DF.value, source=self.csv_file_path_setup)

        expected_values = { 
            "Fallnummer": 4, 
            "Temperatur": 30.0,
            "Luftfeuchtigkeit": 50,
            "Luftdruck": 1010,
            "Windgeschwindigkeit": 5,
            "Laengengrad": 8.682127,
            "Breitengrad": 50.110924,
            "Regen": 0
        }

        last_row = case_base.data.iloc[-1]

        case_base.remove_cases_with_missing_values()

        for column, expected_value in expected_values.items():
            self.assertEqual(last_row[column], expected_value)

    def test_update_case(self):

        case_base = CaseBase(cb_type=CBTypes.DF.value, source=self.csv_file_path_setup)

        case_base.update_case(1, {"Temperatur": 50.0})

        expeceted_values = {
            "Fallnummer": 2, 
            "Temperatur": 50.0,
            "Luftfeuchtigkeit": 60,
            "Luftdruck": 1015,
            "Windgeschwindigkeit": 10,
            "Laengengrad": 11.581981,
            "Breitengrad": 48.135125,
            "Regen": 0
        }

        second_row = case_base.data.iloc[1]

        for column, expected_value in expeceted_values.items():
            self.assertEqual(second_row[column], expected_value)


    def test_remove_duplicate_cases(self): 

        case_base = CaseBase(cb_type=CBTypes.DF.value, source=self.csv_file_path_duplicate)
        
        expected_value = {
            "Fallnummer": 5, 
            "Temperatur": 28.0, 
            "Luftfeuchtigkeit": 40,
            "Luftdruck": 1310,
            "Windgeschwindigkeit": 9,
            "Laengengrad": 8.482127,
            "Breitengrad": 40.110924,
            "Regen": 1
        }

        case_base.drop_duplicate_cases(["Fallnummer"])

        last_row = case_base.data.iloc[-1]

        for column, expected_value in expected_value.items(): 
            self.assertEqual(last_row[column], expected_value) 