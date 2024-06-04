import time

import pandas as pd

from casebased.actors.adapter.adapter import Adapter
from casebased.actors.retriever.retriever import Retriever
from casebased.components.knowledge_containers.case_base.casebase import CaseBase
from casebased.components.knowledge_containers.case_base.constants import CBTypes
from casebased.components.knowledge_containers.ontology.vocabulary import Vocabulary
from casebased.components.knowledge_containers.similarity_measure.similarity_measure import (
    SimilarityMeasure,
)

if __name__ == "__main__":
    new_case_idx = 0
    data = pd.read_csv("../test_data/diabetes.csv")

    test = data.iloc[new_case_idx]
    print(test)

    columns = data.columns
    targets = ["Outcome"]
    features = [c for c in columns if c not in targets]
    weights = [1 for _ in features]
    print(features, targets, weights)
    vocab = Vocabulary(features, targets, weights)

    case_base = CaseBase(cb_type=CBTypes.DF, source="../test_data/diabetes.csv")

    case_base.data.drop([new_case_idx], inplace=True, axis=0)
    case_base.data.reset_index(drop=True, inplace=True)

    # get closest k cases to new case
    case = test[vocab.features]
    case = case.to_frame().T

    sim_measure = SimilarityMeasure(case_base, vocab)

    retriever = Retriever(case_base, sim_measure, vocab)
    distances, kSimilarCases = retriever.retrieve(
        query=case, k=5, algorithm="auto", weights="auto", return_distance=True
    )
    print(kSimilarCases)
    print(case_base.data.iloc[kSimilarCases[0]])
    print(distances)

    adapter = Adapter(case_base, vocab)
    solution = adapter.adapt(case, kSimilarCases)
    print(solution)
