from typing import Protocol, Optional
from casebased.components.vocabulary import Case


class CaseBaseAdapter(Protocol):
    """
    The case base is the storage for all cases in the CBR system. It can be implemented in different ways, e.g. as a list, a database, or a file.
    Since we're not in position to define which technologies you have to use, we provide you an interface to implement your own case base.
    For the library to properly work you have to implement the following functions.
    """
    def get_all_cases(self) -> list[Case]: 
        """
        This function returns all cases in the case base. It's used by the retriever to compare the given case with all cases in the case base.
        Be aware of the return type and adjust your implementation to fit the requirements.
        """
        ...
    def create_case(self, case: Case) -> Optional[bool]: 
        """
        This function is used to add new cases to the case base storage.
        It takes in a case with the Case class as data type and returns a boolean value or None.
        The resulting boolean value should inform the CBR system whether the case was successfully added to the case base.
        If you don't want to give information about that, you can return None, and the system will assume that the case was added.
        """
        ...
    def change_utility(self, case: Case, utility: int) -> Optional[bool]: 
        """
        Optionally a case can have a utility value. 
        This value provides information on how often the particular case was used, 
        which gives information about its knowledge value for the CBR system.
        """
        ...
