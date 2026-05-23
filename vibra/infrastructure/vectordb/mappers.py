from typing import TypedDict

from vibra.domain import EnrichedTrack, IndexedTrack, SearchResult, SearchResults


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


def chroma_get_to_indexed_tracks(raw: dict[str, list]) -> list[IndexedTrack]:
    ids: list[str] = raw.get("ids") or []
    metadatas: list[dict] = raw.get("metadatas") or [{}] * len(ids)
    documents: list[str] = raw.get("documents") or [""] * len(ids)
    return [
        IndexedTrack(
            id=ids[i],
            track_name=metadatas[i].get("track_name", ""),
            artist_names=metadatas[i].get("artist_names", ""),
            album_name=metadatas[i].get("album_name", ""),
            vibe_description=documents[i],
            popularity=metadatas[i].get("popularity", 0),
            spotify_url=metadatas[i].get("spotify_url", ""),
        )
        for i in range(len(ids))
    ]


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
