import time

import pandas as pd

from src.casebased.components.knowledge_containers.case_base.casebase import CaseBase
from src.casebased.components.knowledge_containers.case_base.constants import CBTypes
from src.casebased.components.knowledge_containers.ontology.vocabulary import Vocabulary
from src.casebased.components.knowledge_containers.similarity_measure.similarity_measure import (
    SimilarityMeasure,
)

new_case_idx = 125
data = pd.read_csv("../test_data/diabetes.csv")

test = data.drop([0, 1, 2, 3, 4], axis=0)

columns = data.columns
targets = ["Outcome"]
features = [c for c in columns if c not in targets]
weights = [1 for _ in features]

# Create Vocab
vocab = Vocabulary(features, targets, weights)

print(vocab.features)
print(vocab.targets)
print(vocab.weights)
# Create Case Base
case_base = CaseBase(
    cb_type=CBTypes.DF, source="../test_data/diabetes.csv"
)  # from source


# get closest k cases to new case
case = test.iloc[new_case_idx][vocab.features]

sim_measure = SimilarityMeasure(case_base, vocab)

start = time.time()
prediction = sim_measure.get_k_similar(
    case=case, algorithm="auto", k=3, weights="distance"
)
knn_runtime = time.time() - start


print("#### TEST DATA ####")
print(test.head())
print("#### CASE BASE ####")
print(case_base.data.head())
print(case)
print(prediction)
print("#" * 50)
print("Actual Outcome: ", case_base.data.iloc[new_case_idx]["Outcome"])
print("Predicted Outcome: ", prediction)
print("KNN Runtime: ", knn_runtime, " seconds")
print("#" * 50)
