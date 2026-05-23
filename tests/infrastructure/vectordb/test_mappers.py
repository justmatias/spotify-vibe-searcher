import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import EnrichedTrack, IndexedTrack, SavedTrack, SearchResults
from vibra.infrastructure.vectordb.mappers import (
    chroma_get_to_indexed_tracks,
    chroma_query_to_results,
    enriched_to_payload,
)


@pytest.fixture
def enriched_track(
    enriched_track_factory: ModelFactory[EnrichedTrack],
    saved_track_factory: ModelFactory[SavedTrack],
) -> EnrichedTrack:
    return enriched_track_factory.build(
        track=saved_track_factory.build(),
        vibe_description="Melancholic indie rock with nostalgic themes",
        lyrics="Some lyrics",
    )


def test_enriched_to_payload_sets_correct_id(enriched_track: EnrichedTrack) -> None:
    payload = enriched_to_payload(enriched_track)

    assert payload["ids"] == [enriched_track.track_id]


def test_enriched_to_payload_sets_vibe_as_document(
    enriched_track: EnrichedTrack,
) -> None:
    payload = enriched_to_payload(enriched_track)

    assert payload["documents"] == [enriched_track.vibe_description]


def test_enriched_to_payload_metadata_has_track_fields(
    enriched_track: EnrichedTrack,
) -> None:
    payload = enriched_to_payload(enriched_track)
    meta = payload["metadatas"][0]

    assert meta["track_name"] == enriched_track.track.track.name
    assert meta["artist_names"] == enriched_track.track.track.artist_names
    assert meta["album_name"] == enriched_track.track.track.album.name
    assert meta["popularity"] == enriched_track.track.track.popularity


def test_chroma_query_to_results_returns_search_results() -> None:
    raw: dict[str, list] = {
        "ids": [["track_1", "track_2"]],
        "documents": [["vibe one", "vibe two"]],
        "metadatas": [
            [
                {
                    "track_name": "Song A",
                    "artist_names": "Artist A",
                    "album_name": "Album A",
                    "popularity": 80,
                    "spotify_url": "https://spotify.com/a",
                    "genres": "rock",
                },
                {
                    "track_name": "Song B",
                    "artist_names": "Artist B",
                    "album_name": "Album B",
                    "popularity": 60,
                    "spotify_url": "https://spotify.com/b",
                    "genres": "pop",
                },
            ]
        ],
        "distances": [[0.1, 0.3]],
    }

    results = chroma_query_to_results("test query", raw)

    assert isinstance(results, SearchResults)
    assert results.query == "test query"
    assert results.total_results == 2
    assert results.results[0].track_id == "track_1"
    assert results.results[0].vibe_description == "vibe one"
    assert results.results[0].distance == pytest.approx(0.1)
    assert results.results[1].track_id == "track_2"


def test_chroma_query_to_results_similarity_score_in_range() -> None:
    raw: dict[str, list] = {
        "ids": [["t1"]],
        "documents": [["vibe"]],
        "metadatas": [
            [
                {
                    "track_name": "S",
                    "artist_names": "A",
                    "album_name": "Al",
                    "popularity": 50,
                    "spotify_url": "",
                    "genres": "",
                }
            ]
        ],
        "distances": [[0.25]],
    }
    results = chroma_query_to_results("q", raw)

    assert 0.0 <= results.results[0].similarity_score <= 1.0


def test_chroma_query_to_results_empty_returns_no_results() -> None:
    raw: dict[str, list] = {
        "ids": [[]],
        "documents": [[]],
        "metadatas": [[]],
        "distances": [[]],
    }

    results = chroma_query_to_results("empty query", raw)

    assert results.total_results == 0
    assert not results.has_results


def test_chroma_get_to_indexed_tracks_returns_typed_list() -> None:
    raw: dict[str, list] = {
        "ids": ["track_1"],
        "documents": ["vibe description here"],
        "metadatas": [
            {
                "track_name": "Song",
                "artist_names": "Artist",
                "album_name": "Album",
                "popularity": 70,
                "spotify_url": "https://spotify.com/t",
            },
        ],
    }

    tracks = chroma_get_to_indexed_tracks(raw)

    assert len(tracks) == 1
    assert isinstance(tracks[0], IndexedTrack)
    assert tracks[0].id == "track_1"
    assert tracks[0].track_name == "Song"
    assert tracks[0].vibe_description == "vibe description here"
    assert tracks[0].popularity == 70


def test_chroma_get_to_indexed_tracks_empty_returns_empty_list() -> None:
    raw: dict[str, list] = {"ids": [], "metadatas": [], "documents": []}

    tracks = chroma_get_to_indexed_tracks(raw)

    assert tracks == []
