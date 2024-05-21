from typing import AnyStr

import logging

import numpy as np
import pandas as pd
from plotnine import *
from scipy.optimize import fmin, fmin_cg, minimize
from sklearn.datasets import load_breast_cancer, make_blobs, make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    hinge_loss,
    log_loss,
    roc_auc_score,
)
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.preprocessing import LabelEncoder

from ..case_base.casebase import CaseBase
from ..ontology.vocabulary import Vocabulary

# TODO: Alter das wird komplizierter als ich dachte... Wie berechnet man die ähnlichkeit von 2 Wörtern??
#  Wir müssen dann auch unbedigt einen weg finden, dass
#  Nutzer typisieren müssen im vocabulary (Word, Sentence, Text, Number, ...)
#  Auch noch wichtig dass wir hier noch weights berücksichtigen


class SimilarityMeasure:
    def __init__(self, case_base: CaseBase, vocabulary: Vocabulary):
        self.case_base = case_base
        self.vocabulary = vocabulary

    def get_k_similar(self, **kwargs):
        k = kwargs.get("k")
        algorithm = kwargs.get("algorithm")
        weights = kwargs.get("weights")
        case = kwargs.get("case")

        neigh = KNeighborsClassifier(
            n_neighbors=k, algorithm=algorithm, weights=weights, n_jobs=-1, p=2
        )
        neigh.fit(
            self.case_base.data[self.vocabulary.features].values,
            self.case_base.data[self.vocabulary.targets].values.reshape(
                -1,
            ),
        )
        return neigh.predict(case.values.reshape(1, -1))
        # return NearestNeighbors(n_neighbors=k, algorithm=algorithm).fit(cb)

    def get_global_similarity(self, case, compare_case):
        """
        Compute the global similarity between two cases
        """
        pass

    def get_local_similarity(
        self, new_case_feature: AnyStr, compare_case_feature: AnyStr
    ):
        """
        Compute the similarity between two local features
        """
        pass

    def get_word_similarity(
        self, new_case_feature: AnyStr, compare_case_feature: AnyStr
    ):
        """
        Compute the similarity between two words
        """
        pass

    def get_text_similarity(
        self, new_case_feature: AnyStr, compare_case_feature: AnyStr
    ):
        """
        Compute the similarity between two pieces of text
        """
        pass
