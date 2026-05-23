from typing import TypedDict

from vibra.domain import EnrichedTrack, SearchResult, SearchResults


class ChromaPayload(TypedDict):
    ids: list[str]
    documents: list[str]
    metadatas: list[dict]


def enriched_to_payload(track: EnrichedTrack) -> ChromaPayload:
    spotify_track = track.track.track
    metadata = {
        "track_id": track.track_id,
        "track_name": spotify_track.name,
        "artist_names": spotify_track.artist_names,
        "album_name": spotify_track.album.name,
        "has_lyrics": track.has_lyrics,
        "genres": spotify_track.all_genre_names,
        "popularity": spotify_track.popularity,
        "spotify_url": spotify_track.spotify_url,
    }
    return ChromaPayload(
        ids=[track.track_id],
        documents=[track.vibe_description or ""],
        metadatas=[metadata],
    )


def chroma_query_to_results(query: str, raw: dict[str, list]) -> SearchResults:
    ids = raw.get("ids", [[]])[0]
    documents = raw.get("documents", [[]])[0]
    metadatas = raw.get("metadatas", [[]])[0]
    distances = raw.get("distances", [[]])[0]

    results = [
        SearchResult.model_validate({
            "track_id": ids[i],
            "vibe_description": documents[i],
            "distance": distances[i],
            **metadatas[i],
        })
        for i in range(len(ids))
    ]
    return SearchResults(query=query, results=results, total_results=len(results))
