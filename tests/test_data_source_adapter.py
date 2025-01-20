import os

import pandas as pd
from casebased.components.casebase.casebase import CaseBase
from casebased.components.casebase.data_source_adapter import DataSourceAdapter


class TestDataSourceAdapter:

    def test_read_file(self):

        path_to_csv = "test_data/regen.csv"

        data_source_adapter = DataSourceAdapter(path_to_csv)

        regen_dataframe = data_source_adapter.read_file()

        expected_case_base = [
            {
                "Fallnummer": 1,
                "Temperatur": 22.5,
                "Luftfeuchtigkeit": 85,
                "Luftdruck": 1012,
                "Windgeschwindigkeit": 15,
                "Laengengrad": 13.404954,
                "Breitengrad": 52.520008,
                "Regen?": 1,
            },
            {
                "Fallnummer": 2,
                "Temperatur": 25.0,
                "Luftfeuchtigkeit": 60,
                "Luftdruck": 1015,
                "Windgeschwindigkeit": 10,
                "Laengengrad": 11.581981,
                "Breitengrad": 48.135125,
                "Regen?": 0,
            },
            {
                "Fallnummer": 3,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 90,
                "Luftdruck": 1009,
                "Windgeschwindigkeit": 20,
                "Laengengrad": 9.993682,
                "Breitengrad": 53.551086,
                "Regen?": 1,
            },
            {
                "Fallnummer": 4,
                "Temperatur": 30.0,
                "Luftfeuchtigkeit": 50,
                "Luftdruck": 1010,
                "Windgeschwindigkeit": 5,
                "Laengengrad": 8.682127,
                "Breitengrad": 50.110924,
                "Regen?": 0,
            },
        ]

        expected_case_base_df = pd.DataFrame(expected_case_base)

        pd.testing.assert_frame_equal(
            regen_dataframe, pd.DataFrame(expected_case_base_df)
        )

    def test_read_file_invalid_path(self):

        path_to_csv = "test_data/invalid.csv"

        data_source_adapter = DataSourceAdapter(path_to_csv)

        regen_dataframe = data_source_adapter.read_file()

        assert regen_dataframe is None

    def test_read_file_invalid_format(self):

        path_to_csv = "test_data/invalid_format.csv"

        data_source_adapter = DataSourceAdapter(path_to_csv)

        regen_dataframe = data_source_adapter.read_file()

        assert regen_dataframe is None

    def test_read_file_empty(self):

        path_to_csv = "test_data/empty.csv"

        data_source_adapter = DataSourceAdapter(path_to_csv)

        regen_dataframe = data_source_adapter.read_file()

        assert regen_dataframe is None

    def test_add_utility_column_to_csv(self):

        path_to_csv = "test_data/regen.csv"

        data_source_adapter = DataSourceAdapter(path_to_csv)

        regen_dataframe = data_source_adapter.read_file()

        # works
        # regen_dataframe = data_source_adapter.add_utility_column_csv()

        expected_case_base = [
            {
                "Fallnummer": 1,
                "Temperatur": 22.5,
                "Luftfeuchtigkeit": 85,
                "Luftdruck": 1012,
                "Windgeschwindigkeit": 15,
                "Laengengrad": 13.404954,
                "Breitengrad": 52.520008,
                "Regen?": 1,
            },
            {
                "Fallnummer": 2,
                "Temperatur": 25.0,
                "Luftfeuchtigkeit": 60,
                "Luftdruck": 1015,
                "Windgeschwindigkeit": 10,
                "Laengengrad": 11.581981,
                "Breitengrad": 48.135125,
                "Regen?": 0,
            },
            {
                "Fallnummer": 3,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 90,
                "Luftdruck": 1009,
                "Windgeschwindigkeit": 20,
                "Laengengrad": 9.993682,
                "Breitengrad": 53.551086,
                "Regen?": 1,
            },
            {
                "Fallnummer": 4,
                "Temperatur": 30.0,
                "Luftfeuchtigkeit": 50,
                "Luftdruck": 1010,
                "Windgeschwindigkeit": 5,
                "Laengengrad": 8.682127,
                "Breitengrad": 50.110924,
                "Regen?": 0,
            },
        ]

        expected_case_base_df = pd.DataFrame(expected_case_base)

        pd.testing.assert_frame_equal(expected_case_base_df, regen_dataframe)

    def test_update_data_source(self):

        path_to_update_csv = "test_data/update_csv.csv"

        initial_data = [
            {
                "Fallnummer": 1,
                "Temperatur": 22.5,
                "Luftfeuchtigkeit": 85,
                "Luftdruck": 1012,
                "Windgeschwindigkeit": 15,
                "Laengengrad": 13.404954,
                "Breitengrad": 52.520008,
                "Regen?": 1,
                "utility": 30,
            },
            {
                "Fallnummer": 2,
                "Temperatur": 25.0,
                "Luftfeuchtigkeit": 60,
                "Luftdruck": 1015,
                "Windgeschwindigkeit": 10,
                "Laengengrad": 11.581981,
                "Breitengrad": 48.135125,
                "Regen?": 0,
                "utility": 55,
            },
            {
                "Fallnummer": 3,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 90,
                "Luftdruck": 1009,
                "Windgeschwindigkeit": 20,
                "Laengengrad": 9.993682,
                "Breitengrad": 53.551086,
                "Regen?": 1,
                "utility": 70,
            },
            {
                "Fallnummer": 4,
                "Temperatur": 30.0,
                "Luftfeuchtigkeit": 50,
                "Luftdruck": 1010,
                "Windgeschwindigkeit": 5,
                "Laengengrad": 8.682127,
                "Breitengrad": 50.110924,
                "Regen?": 0,
                "utility": 40,
            },
        ]

        with open("test_data/update_csv.csv", "w") as f:
            f.write(
                "Fallnummer,Temperatur,Luftfeuchtigkeit,Luftdruck,Windgeschwindigkeit,Laengengrad,Breitengrad,Regen?,utility\n"
            )
            for row in initial_data:
                f.write(
                    f"{row['Fallnummer']},{row['Temperatur']},{row['Luftfeuchtigkeit']},{row['Luftdruck']},{row['Windgeschwindigkeit']},{row['Laengengrad']},{row['Breitengrad']},{row['Regen?']},{row['utility']}\n"
                )

        data_source_adapter = DataSourceAdapter(path_to_update_csv)
        initial_dataframe = data_source_adapter.read_file()
        case_base = CaseBase(cases=initial_dataframe)

        # Step 3: Perform modifications in the CaseBase (e.g., prune based on utility threshold)
        case_base.prune(threshold=50)

        # Step 4: Update the data source with the pruned data
        data_source_adapter.update_data_source(case_base)

        # Step 5: Read the updated data source and validate its content
        updated_dataframe = data_source_adapter.read_file()

        # Expected pruned data
        expected_data = [
            {
                "Fallnummer": 2,
                "Temperatur": 25.0,
                "Luftfeuchtigkeit": 60,
                "Luftdruck": 1015,
                "Windgeschwindigkeit": 10,
                "Laengengrad": 11.581981,
                "Breitengrad": 48.135125,
                "Regen?": 0,
                "utility": 55,
            },
            {
                "Fallnummer": 3,
                "Temperatur": 20.0,
                "Luftfeuchtigkeit": 90,
                "Luftdruck": 1009,
                "Windgeschwindigkeit": 20,
                "Laengengrad": 9.993682,
                "Breitengrad": 53.551086,
                "Regen?": 1,
                "utility": 70,
            },
        ]

        expected_dataframe = pd.DataFrame(expected_data)

        # Assert that the updated data matches the expected pruned data
        pd.testing.assert_frame_equal(expected_dataframe, updated_dataframe)

        # Cleanup: Remove the test CSV file
        os.remove(path_to_update_csv)
