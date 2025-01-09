import pandas as pd
from ..casebased.system import CBR
from ..casebased import components
from ..casebased import actors


def test__system():
    system = CBR()
    cases = pd.read_csv("../test_data/diabetes.csv")
    system.case_base = components.CaseBase(cases)
    cols = system.case_base.cases.columns
    
    system.similarity_measure = components.similarity.similarity_measure(
        types={
            int: components.similarity.numbers.linear(max=9999999),
            float: components.similarity.numbers.linear(max=9999999),
        },
        aggregator=components.similarity.aggregator("mean"),
    )

    retriever = actors.retriever.build(system.similarity_measure, limit=10)
    res = actors.retriever.retrieve(system.case_base, retriever, cols[0], 0)
    
    print(res)
    ## test with one case
    # 6,148,72,35,0,33.6,0.627,50,1

test__system()