from typing import AnyStr

from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors

from ...case.querycase import QueryCase
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
        self.classifier = None
        self.Regressor = None

    def fit(self, **kwargs):
        if kwargs.get("model"):
            if kwargs.get("model") == "knn":
                self._fit_classifier(**kwargs)
        self._fit_classifier(**kwargs)

    def _fit_classifier(self, **kwargs):
        k = kwargs.get("k")
        algorithm = kwargs.get("algorithm")
        weights = kwargs.get("weights")
        query = kwargs.get("query")

        x = self.case_base.data[self.vocabulary.feature_names].values
        y = self.case_base.data[self.vocabulary.targets].values.reshape(-1)

        if k == "auto" or k is None or k == 0 or weights == "auto" or weights is None:
            param_grid = {
                "n_neighbors": range(1, 50),
                "weights": ["uniform", "distance"],
            }
            grid_search = GridSearchCV(KNeighborsClassifier(), param_grid)
            grid_search.fit(x, y)
            if k == "auto" or k is None or k == 0:
                k = grid_search.best_params_["n_neighbors"]
            if weights == "auto" or weights is None:
                weights = grid_search.best_params_["weights"]

        self.classifier = KNeighborsClassifier(
            n_neighbors=k, algorithm=algorithm, weights=weights, n_jobs=-1, p=2
        )

        self.classifier.fit(x, y)

    def classify(self, query):
        return self.classifier.predict(query)

    def get_k_similar_cases(
        self,
        query: QueryCase,
        k,
        return_distance=False,
        algorithm="auto",
        weighted=False,
    ):
        """
        Get the k most similar cases to a given case
        """
        try:
            x = self.case_base.data[self.vocabulary.feature_names].values
        except KeyError:
            x = self.case_base.data[self.vocabulary.feature_names].values

        if weighted:
            neighbors = NearestNeighbors(
                n_neighbors=k,
                algorithm=algorithm,
                metric="minkowski",
                metric_params={"w": self.vocabulary.weights},
            ).fit(x)
        else:
            neighbors = NearestNeighbors(n_neighbors=k, algorithm=algorithm).fit(x)
        if return_distance:
            distances, indices = neighbors.kneighbors(query, return_distance=True)
            return distances, indices
        indices = neighbors.kneighbors(
            query.get_2d_feature_array(), return_distance=False
        )
        return indices

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
