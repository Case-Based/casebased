from pathlib import Path
from casebase import CaseBase
from constants import CBTypes

# Path to the CSV file
csv_file_path = Path('test_data/regen.csv')

# Instantiate the CaseBase class
case_base_instance = CaseBase(cb_type=CBTypes.DF.value, source=csv_file_path)

# Optional: Print the data to verify the content
print(case_base_instance.data)