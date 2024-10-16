from src.casebased.casebaseMaintainer import CaseBaseMaintainer
from src.casebased.components.knowledge_containers.case_base import CaseBase

class TestCaseBaseMaintainer:

    def test_add_data(self):

        maintainer = CaseBaseMaintainer()
        createCaseBase = CaseBase() 
        
        # Fallnummer,Luftfeuchtigkeit,Luftdruck,Windgeschwindigkeit,Laengengrad,Breitengrad,Regen?

        new_data = {
            "Fallnummer": 7,
            "Luftfeuchtigkeit": 0.6,
            "Luftdruck": 0.8,
            "Windgeschwindigkeit": 0.4, 
            "Laengengrad": 0.5,
            "Breitengrad": 0.6,
            "Regen?": 0
        }

        maintainer.add_data(createCaseBase, new_data) 


    def test_update_utils(self):
        pass

    def test_prune(self):
        pass

    def test_get_current_casebase(self):
        pass