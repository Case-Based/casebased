from casebased.components.similarity_measure.functions import (
    LinearInterval,
    SquaredDistance,
)
from casebased.components.similarity_measure.schema import SimilaritySchema


def test_build_similarity_schema():
    similarity_schema = SimilaritySchema(
        attributes={
            "price": SquaredDistance(),
            "size": LinearInterval(50, 100),
        },
        threshold=5,
        limit=10,
    )

    assert len(similarity_schema.attributes) == 2
    assert similarity_schema.threshold == 5
    assert similarity_schema.limit == 10
