from typing import List

import math

from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

from casebased.components.casebase.casebase import CaseBase
from casebased.components.casebase.query_case import QueryCase
from casebased.components.similarity_measure.similarity import SimilarityMeasure
from casebased.components.vocabulary import Vocabulary
from casebased.config import Configuration


class Retriever:
    def __init__(self, config: Configuration):
        self.__config = config
        self.__model: KNeighborsClassifier | KNeighborsRegressor | None = None

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, config: Configuration):
        self.__config = config

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model

    def fit(self):
        if self.__model is None:
            self._fit_classifier()

    def _fit_classifier(self, case_base: CaseBase, vocabulary: Vocabulary):
        k = self.__config.k
        algorithm = self.__config.similarity_measure_metric
        weights = self.__config.feature_weights
        p = self.__config.minkowski_p

        x = case_base.cases[vocabulary.feature_names].values
        y = case_base.cases[vocabulary.targets].values.reshape(-1)

        if k == "auto" or k is None or k == 0 or weights == "auto" or weights is None:
            param_grid = {
                "n_neighbors": range(1, int(math.sqrt(len(case_base.cases.index)))),
                "weights": ["uniform", "distance"],
            }
            grid_search = GridSearchCV(KNeighborsClassifier(), param_grid)
            grid_search.fit(x, y)
            if k == "auto" or k is None or k == 0:
                k = grid_search.best_params_["n_neighbors"]
            if weights == "auto" or weights is None:
                weights = grid_search.best_params_["weights"]

        self.model = KNeighborsClassifier(
            n_neighbors=k, algorithm=algorithm, weights=weights, n_jobs=-1, p=p
        )
        self.model.fit(x, y)

    def predict(self, queries: List[QueryCase]):
        if self.model is None:
            raise ValueError("Classifier not fitted")
        return self.model.predict([q.feature_values for q in queries])

    def retrieve(
        self,
        query: QueryCase,
        case_base: CaseBase,
        vocabulary: Vocabulary,
        similarity_measure: SimilarityMeasure,
    ):
        if self.model is None:
            self._fit_classifier(case_base, vocabulary)
        return self.model.kneighbors(
            query.get_2d_feature_array(), return_distance=False
        )
