import pandas as pd

from src.casebased.components.knowledge_containers.case_base.casebase import CaseBase
from src.casebased.components.knowledge_containers.case_base.constants import CBTypes
from src.casebased.components.knowledge_containers.ontology.vocabulary import Vocabulary
from src.casebased.components.knowledge_containers.similarity_measure.similarity_measure import (
    SimilarityMeasure,
)

data = pd.read_csv("regen.csv")
columns = data.columns
targets = ["Regen?"]
features = [c for c in columns if c not in targets]
weights = [1 for _ in features]

# Create Vocab
vocab = Vocabulary(features, targets, weights)

print(vocab.features)
print(vocab.targets)
print(vocab.weights)
# Create Case Base
case_base = CaseBase(cb_type=CBTypes.DF, source="regen.csv")  # from source

print(case_base.data.head())

# get closest k cases to new case
k = 3
case = case_base.data.iloc[1]
print(case)

sim_measure = SimilarityMeasure()
knn = sim_measure.kNN(case, vocab, "auto", k, case_base.data.values)

print(knn.kneighbors(case.values.reshape(1, -1), return_distance=False))
