from shared.domain.bases.collection import Collection
from shared.domain.bases.entity import MockEntity


class TestCollection:
    def test_get_created_before_returns_only_entities_created_before_given_timestamp(
        self, entities: list[MockEntity]
    ):
        timestamp = entities[0].created_at
        expected = [entity for entity in entities if entity.created_at < timestamp]

        collection = Collection(entities)
        filtered = collection.get_created_before(timestamp)

        assert len(filtered) == len(expected)
        assert all(entity.created_at < timestamp for entity in filtered)

    def test_get_created_after_returns_only_entities_created_after_given_timestamp(
        self, entities: list[MockEntity]
    ):
        timestamp = entities[0].created_at
        expected = [entity for entity in entities if entity.created_at > timestamp]

        collection = Collection(entities)
        filtered = collection.get_created_after(timestamp)

        assert len(filtered) == len(expected)
        assert all(entity.created_at > timestamp for entity in filtered)

    def test_sort_by_created_at_returns_entities_sorted_by_created_at(
        self, entities: list[MockEntity]
    ):
        collection = Collection(entities)
        sorted_ = collection.sort_by_created_at()

        assert sorted_ == sorted(entities, key=lambda entity: entity.created_at)
