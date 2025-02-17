from typing import Optional

from dataclasses import dataclass

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from casebased import CaseBaseAdapter
from casebased.components.similarity_measure import SimilaritySchema
from casebased.components.vocabulary import Case


class Counter:
    def __init__(self, total_elements: int):
        self.count = 0
        self.total_elements = total_elements

    def increment(self):
        self.count += 1

    def get_count(self):
        return self.count, self.total_elements


@dataclass()
class Retriever:
    """
    The retriever component is used to calculate similarities using the provided similarity schema
    and retrieve the k most similar cases from the case base.
    """

    similarity_schema: SimilaritySchema
    """
    Used to define how similarity is calculated between cases.
    """
    case_base: CaseBaseAdapter
    """
    Used to get all cases from the case base.
    """
    k: int
    """
    How many cases should be returned.
    """

    def get_least_similar(self, cases: list[tuple[Case, float]]) -> Optional[Case]:
        """
        Get the least similar case in a list of cases with their respective similarity value.

        Args:
            cases: A dictionary with cases as keys and their similarity value as values.

        Returns:
            The least similar case or None.
        """
        least_similar = None

        if len(cases) == 0:
            return least_similar

        for idx, (key, val) in enumerate(cases):
            if least_similar is None:
                least_similar = idx
            elif val < cases[idx][1]:
                least_similar = idx

        return least_similar

    def train(self, feature_attribute_keys: list[str]):
        """
        Train the retriever component.
        """
        cases: list[Case] = self.case_base.get_all_cases()

        X = np.array([self.__case_to_ndarray(c, feature_attribute_keys) for c in cases])

        # For labels, we can use dummy indices (since we only need distances)
        y = np.arange(len(cases))

        def custom_distance_metric(
            a: np.ndarray, b: np.ndarray, progress_counter: Counter
        ) -> float:
            """
            Convert arrays back to Cases and calculate distance as 1.0 - similarity.
            """
            progress_counter.increment()
            count, total = progress_counter.get_count()
            if count % 1000 == 0:
                print(f"Progress: {count}/{total} ({round(count/total * 100, 2)}%)")
            case_a = self.__ndarray_to_case(a, feature_attribute_keys)
            case_b = self.__ndarray_to_case(b, feature_attribute_keys)
            similarity = self.similarity_schema.calculate(case_a, case_b)
            # sklearn requires a distance metric, so we convert similarity to distance
            distance = 1.0 - similarity
            return distance

        progress_counter = Counter(len(X) * 6)

        knn = KNeighborsClassifier(
            n_neighbors=self.k,
            metric=custom_distance_metric,
            metric_params={
                "progress_counter": progress_counter,
            },
        )

        knn.fit(X, y)

        self._knn = knn

    def __case_to_ndarray(self, case: Case, feature_order: list[str]) -> np.ndarray:
        """
        Convert a Case object into an ndarray representation.

        Args:
            case: The Case object to convert.
            feature_order: List of feature keys in a specific order.

        Returns:
            A numpy array representing the case.
        """
        feature_values = []

        for key in feature_order:
            value = case.feature_attributes.get(key, 0)  # Default to 0 if missing

            # Convert categorical values to numerical encoding
            if isinstance(value, str):
                value = hash(value) % 1000  # Simple hashing for consistency

            feature_values.append(value)

        return np.array(feature_values, dtype=np.float32)

    def __ndarray_to_case(self, array: np.ndarray, feature_order: list[str]) -> Case:
        """
        Convert an ndarray representation back into a Case object.

        Args:
            array: The numpy array to convert.
            feature_order: List of feature keys in the same order used for encoding.

        Returns:
            A Case object reconstructed from the array.
        """
        feature_attributes = {key: array[i] for i, key in enumerate(feature_order)}

        return Case(feature_attributes=feature_attributes, target_attributes={})

    def retrieve(self, case: Case) -> list[tuple[Case, float]]:
        """
        Simply retrieve the k most similar cases to the provided case.

        Args:
            case: The case for which to retrieve the k most similar cases.

        Returns:
            A list of tuples where each tuple contains one of the k most similar Cases
            and the similarity value.
        """
        cases: list[Case] = self.case_base.get_all_cases()

        knn_instance = self._knn

        query_array = self.__case_to_ndarray(case, case.feature_attributes.keys())

        distances, indices = knn_instance.kneighbors([query_array], n_neighbors=self.k)

        retrieved_cases: list[tuple[Case, float]] = []
        for dist, idx in zip(distances[0], indices[0]):
            sim = 1.0 - dist
            retrieved_cases.append((cases[idx], sim))

        return retrieved_cases
