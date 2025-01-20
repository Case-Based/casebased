import unittest

from casebased.components.similarity_measure.functions import (
    LinearInterval,
    SquaredDistance,
)
from casebased.components.similarity_measure.schema import SimilaritySchema
from casebased.components.vocabulary import (
    Condition,
    ConditionType,
    FeatureAttribute,
    TargetAttribute,
    Vocabulary,
)


class TestSimilaritySchema(unittest.TestCase):
    def test_build_similarity_schema(self):
        similarity_schema = SimilaritySchema(
            vocabulary=Vocabulary(
                features=[
                    FeatureAttribute(
                        name="size",
                        data_type=float,
                        weight=2.0,
                        conditions=[
                            Condition(
                                con_type=ConditionType.GREATER_THAN_EQUALS,
                                check_val=0.0,
                            )
                        ],
                    )
                ],
                targets=[
                    TargetAttribute(
                        name="price",
                        data_type=float,
                        conditions=[
                            Condition(
                                con_type=ConditionType.GREATER_THAN_EQUALS,
                                check_val=0.0,
                            )
                        ],
                    )
                ],
            ),
            attributes={
                "price": SquaredDistance(),
                "size": LinearInterval(50, 100),
            },
        )

        self.assertEqual(len(similarity_schema.attributes), 2)
