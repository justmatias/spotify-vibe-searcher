import pytest

from vibra.domain import EnrichedTrack, SearchResults
from vibra.infrastructure import VectorDBRepository


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_add_track_with_vibe_description(
    vectordb_repository: VectorDBRepository,
    enriched_track_with_vibe: EnrichedTrack,
) -> None:
    initial_count = vectordb_repository.collection.count()
    await vectordb_repository.add(enriched_track_with_vibe)

    assert vectordb_repository.collection.count() == initial_count + 1
    result = vectordb_repository.collection.get(ids=[enriched_track_with_vibe.track_id])
    assert len(result["ids"]) == 1
    assert result["ids"][0] == enriched_track_with_vibe.track_id
    assert result["metadatas"][0]["track_id"] == enriched_track_with_vibe.track_id


@pytest.mark.asyncio
async def test_add_track_without_vibe_skips(
    vectordb_repository: VectorDBRepository,
    enriched_track_without_vibe: EnrichedTrack,
) -> None:
    initial_count = vectordb_repository.collection.count()
    await vectordb_repository.add(enriched_track_without_vibe)

    assert vectordb_repository.collection.count() == initial_count


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_add_tracks_batch(
    vectordb_repository: VectorDBRepository,
    enriched_tracks_batch: list[EnrichedTrack],
) -> None:
    initial_count = vectordb_repository.collection.count()
    await vectordb_repository.add_many(enriched_tracks_batch)
    assert vectordb_repository.collection.count() == initial_count + 2


@pytest.mark.asyncio
@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_single_track")
async def test_delete_tracks(
    vectordb_repository: VectorDBRepository,
    enriched_track_with_vibe: EnrichedTrack,
) -> None:
    result = vectordb_repository.collection.get(ids=[enriched_track_with_vibe.track_id])
    assert len(result["ids"]) == 1

    await vectordb_repository.delete([enriched_track_with_vibe.track_id])
    result = vectordb_repository.collection.get(ids=[enriched_track_with_vibe.track_id])
    assert len(result["ids"]) == 0


@pytest.mark.asyncio
@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_batch")
async def test_delete_multiple_tracks(
    vectordb_repository: VectorDBRepository,
    enriched_tracks_batch: list[EnrichedTrack],
) -> None:
    track_ids = [
        track.track_id for track in enriched_tracks_batch if track.vibe_description
    ]

    await vectordb_repository.delete(track_ids)
    result = vectordb_repository.collection.get(ids=track_ids)

    assert len(result["ids"]) == 0


@pytest.mark.asyncio
@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_search_tracks")
async def test_search_by_vibe_finds_matching_tracks(
    vectordb_repository: VectorDBRepository,
) -> None:
    results = await vectordb_repository.search(
        "sad songs about heartbreak", n_results=3
    )

    assert isinstance(results, SearchResults)
    assert results.total_results > 0
    assert len(results.results) > 0


@pytest.mark.asyncio
@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_search_tracks")
async def test_search_by_vibe_returns_correct_number_of_results(
    vectordb_repository: VectorDBRepository,
) -> None:
    results = await vectordb_repository.search("energetic music", n_results=2)

    assert results.total_results <= 2


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_search_by_vibe_empty_collection(
    vectordb_repository: VectorDBRepository,
) -> None:
    results = await vectordb_repository.search("any query", n_results=10)

    assert isinstance(results, SearchResults)
    assert results.total_results == 0


@pytest.mark.asyncio
@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_search_tracks")
async def test_search_by_vibe_returns_metadata(
    vectordb_repository: VectorDBRepository,
) -> None:
    results = await vectordb_repository.search("happy upbeat songs", n_results=3)

    if results.total_results > 0:
        first = results.results[0]
        assert first.track_id
        assert first.track_name is not None
        assert first.artist_names is not None
        assert first.album_name is not None


@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_batch")
def test_get_all_tracks(
    vectordb_repository: VectorDBRepository,
) -> None:
    results = vectordb_repository.get_all_tracks()
    assert len(results["ids"]) > 0


@pytest.mark.asyncio
@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_batch")
async def test_count_tracks(
    vectordb_repository: VectorDBRepository,
) -> None:
    count = await vectordb_repository.count()
    assert count > 0


@pytest.mark.asyncio
async def test_count_tracks_empty(
    vectordb_repository: VectorDBRepository,
) -> None:
    count = await vectordb_repository.count()
    assert count == 0


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_track_exists(
    vectordb_repository: VectorDBRepository,
    enriched_track_with_vibe: EnrichedTrack,
) -> None:
    assert not await vectordb_repository.track_exists(enriched_track_with_vibe.track_id)

    await vectordb_repository.add(enriched_track_with_vibe)

    assert await vectordb_repository.track_exists(enriched_track_with_vibe.track_id)
