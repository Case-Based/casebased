from src.config import Configuration
from src.system import CaseBaseSystem


def test__system_init():
    cbr_system = CaseBaseSystem()
    assert cbr_system.configuration is None


def test__configuration_change():
    TEST_CONFIG = Configuration()
    cbr_system = CaseBaseSystem()
    cbr_system.change_config(TEST_CONFIG)
    assert cbr_system.configuration is not None
    assert cbr_system.configuration.k is None
    assert cbr_system.configuration.similarity_measure_algorithm is None
    assert cbr_system.configuration.k_algorithm is None
