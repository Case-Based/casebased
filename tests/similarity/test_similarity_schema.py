import unittest

from casebased.components.similarity_measure.functions import (
    LinearInterval,
    SquaredDistance,
)
from casebased.components.similarity_measure.schema import SimilaritySchema


class TestSimilaritySchema(unittest.TestCase):
    def test_build_similarity_schema(self):
        similarity_schema = SimilaritySchema(
            attributes={
                "price": SquaredDistance(),
                "size": LinearInterval(50, 100),
            },
        )

        self.assertEqual(len(similarity_schema.attributes), 2)
