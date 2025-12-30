# pylint: disable=protected-access
import pytest

from spotify_rag.domain import EnrichedTrack
from spotify_rag.infrastructure import VectorDBRepository


def test_client_lazy_loading(
    vectordb_repository: VectorDBRepository,
) -> None:
    assert vectordb_repository._client is None
    client = vectordb_repository.client
    assert vectordb_repository._client is client


def test_collection_creation(
    vectordb_repository: VectorDBRepository,
) -> None:
    collection = vectordb_repository.collection
    assert collection.name == "tracks"


@pytest.mark.vcr
def test_add_track_with_vibe_description(
    vectordb_repository: VectorDBRepository,
    enriched_track_with_vibe: EnrichedTrack,
) -> None:
    initial_count = vectordb_repository.collection.count()
    vectordb_repository.add_track(enriched_track_with_vibe)

    assert vectordb_repository.collection.count() == initial_count + 1
    result = vectordb_repository.collection.get(ids=[enriched_track_with_vibe.track_id])
    assert len(result["ids"]) == 1
    assert result["ids"][0] == enriched_track_with_vibe.track_id
    assert result["metadatas"][0]["track_id"] == enriched_track_with_vibe.track_id


def test_add_track_without_vibe_skips(
    vectordb_repository: VectorDBRepository,
    enriched_track_without_vibe: EnrichedTrack,
) -> None:
    initial_count = vectordb_repository.collection.count()
    vectordb_repository.add_track(enriched_track_without_vibe)

    assert vectordb_repository.collection.count() == initial_count


@pytest.mark.vcr
def test_add_tracks_batch(
    vectordb_repository: VectorDBRepository,
    enriched_tracks_batch: list[EnrichedTrack],
) -> None:
    initial_count = vectordb_repository.collection.count()
    vectordb_repository.add_tracks(enriched_tracks_batch)
    assert vectordb_repository.collection.count() == initial_count + 2


def test_delete_tracks(
    vectordb_repository: VectorDBRepository,
    enriched_track_with_vibe: EnrichedTrack,
) -> None:
    vectordb_repository.add_track(enriched_track_with_vibe)
    result = vectordb_repository.collection.get(ids=[enriched_track_with_vibe.track_id])
    assert len(result["ids"]) == 1

    vectordb_repository.delete_tracks([enriched_track_with_vibe.track_id])
    result = vectordb_repository.collection.get(ids=[enriched_track_with_vibe.track_id])
    assert len(result["ids"]) == 0


def test_delete_multiple_tracks(
    vectordb_repository: VectorDBRepository,
    enriched_tracks_batch: list[EnrichedTrack],
) -> None:
    vectordb_repository.add_tracks(enriched_tracks_batch)
    track_ids = [
        track.track_id for track in enriched_tracks_batch if track.vibe_description
    ]

    vectordb_repository.delete_tracks(track_ids)
    result = vectordb_repository.collection.get(ids=track_ids)

    assert len(result["ids"]) == 0
