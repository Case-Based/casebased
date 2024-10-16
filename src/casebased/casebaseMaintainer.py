import pandas as pd 
from casebased.components.casebase import CaseBase as CB 


# get_current_casebase()

# Returns the current case base to the user, so the user can update it in their datasource
# Returns: list of cases

class CaseBaseMaintainer: 

    def add_data(self, data: list, validate: bool, fill_empty: bool): 
        '''
        Add a case to the case base.
        Validate it's structure and fill emtpy values if necessary.
        Params: 
        data: list of dicts(cases)
        validate (boolean)
        fill_empty (boolean)
        '''
        if validate: 
            if CB.validate_data(data): 
                CB.verify_case_structue(data) 
                CB.fill_missing_values_with_zero()
                data_to_be_added = pd.DataFrame(data)
                CB.add_data(data_to_be_added)
                return 
        else: 
            data_to_be_added = pd.DataFrame(data)
            CB.add_data(data_to_be_added)  
            return 
        
    def update_utils(self, case: list) -> None: 
        '''
        Increase the utils count for (retrieved) cases used to solve problem.
        Params: case: list of dicts 
        '''
        # update_utils()

        # case base -> feature -> wenn index genommen wird 
        # überall wo fall genommen wird, utility erhöhen 
        # pandas documentation -> save dataframe 
        # utility mitspeichern 

        # Increase the utils count for the specific case
        # The utils count increases whenever the case was used to solve another case
        # This means that the util count is a performance measurement for a case
        # Params: case
        # Returns: None 
        # check retainer if case was used to get solution 
        # increase the util number of the cases being used 
        # after ~ 100 iterations of the program, remove cases with lower util score than 3
        return 

    def prune(threshold: int) -> None: 
        
        ''''
        Removes cases from the case base that aren't used often enough. 
        Params: threshold (int)
        '''

        case_base = CB.get_case_base()
        for element in case_base: 
            if (element['util'] < 3): 
                case_base.remove(element)

        # Removes cases from the case base that meet a specific criteria (e.g. util score)
        # Params: threshold (int)
        # Returns: None
        return
    
    def get_current_casebase(): 
        case_base = CB.get_case_base()
        return case_base
