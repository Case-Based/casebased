import pandas as pd

from casebased.actors.adapter import Adapter
from casebased.actors.retriever import Retriever
from casebased.components.attribute import FeatureAttribute
from casebased.components.casebase import CaseBase
from casebased.components.constants import CBTypes
from casebased.components.similarity_measure import SimilarityMeasure
from casebased.components.vocabulary import Vocabulary

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

    vocab.compile_weights(case_base, method="korr")
    # print(vocab.weights)

    # get closest k cases to new case
    case = test[vocab.feature_names]
    case = case.to_frame().T

    sim_measure = SimilarityMeasure(case_base, vocab)

    retriever = Retriever(case_base, sim_measure, vocab)
    distances, kSimilarCases = retriever.retrieve(
        query=case, k=5, algorithm="auto", weighted=True, return_distance=True
    )
    # print(kSimilarCases)
    # print(case_base.data.iloc[kSimilarCases[0]])
    # print(distances)

    adapter = Adapter(case_base, vocab)
    solution = adapter.adapt(case, kSimilarCases)
    print(solution)

    ### FLOW BASED DEVELOPMENT

    # Import Data
    data = pd.read_csv("../test_data/diabetes.csv")
    # Create CaseBase
    case_base = CaseBase(data)
    # Create Vocabulary
    feature_labels = [c for c in data.columns if c not in ["Outcome"]]
    target_labels = ["Outcome"]

    features = [FeatureAttribute.from_name_string(f) for f in feature_labels]
    targets = [FeatureAttribute.from_name_string(t) for t in target_labels]

    vocab = Vocabulary(features, targets, weights)
    # Learn Weights
    vocab.compile_weights(case_base, method="korr")

    # Learn Adaptation Rules

    # Accept New Case

    # Retrieve Similar Cases

    # Adapt Solution

    # Explain Solution

    # Return Solution

    # Store Case
