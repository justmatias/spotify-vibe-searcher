from pydantic import BaseModel

from spotify_rag.domain import SearchResult, SearchResults
from spotify_rag.infrastructure import VectorDBRepository
from spotify_rag.utils import LogLevel, log


class SearchService(BaseModel):
    vectordb_repository: VectorDBRepository

    def search_by_vibe(self, query: str, n_results: int = 10) -> SearchResults:
        """Search for tracks by vibe description using semantic similarity.

        Args:
            query: Natural language query describing the desired vibe.
            n_results: Maximum number of results to return.

        Returns:
            SearchResults containing matching tracks with metadata.
        """
        log(f"Searching for vibe: '{query}' (max {n_results} results)", LogLevel.INFO)

        raw_results = self.vectordb_repository.search_by_vibe(query, n_results)
        search_results = self._transform_results(query, raw_results)

        log(
            f"Found {search_results.total_results} matching tracks",
            LogLevel.INFO,
        )

        return search_results

    def _transform_results(
        self, query: str, raw_results: dict[str, list]
    ) -> SearchResults:
        # ChromaDB returns nested lists, we need the first element
        ids = raw_results.get("ids", [[]])[0]
        documents = raw_results.get("documents", [[]])[0]
        metadatas = raw_results.get("metadatas", [[]])[0]
        distances = raw_results.get("distances", [[]])[0]

        results = [
            self._create_search_result(
                track_id=ids[i],
                vibe_description=documents[i],
                metadata=metadatas[i],
                distance=distances[i],
            )
            for i in range(len(ids))
        ]

        return SearchResults(
            query=query,
            results=results,
            total_results=len(results),
        )

    def _create_search_result(  # pylint: disable=no-self-use
        self,
        track_id: str,
        vibe_description: str,
        metadata: dict,
        distance: float,
    ) -> SearchResult:
        return SearchResult.model_validate({
            "track_id": track_id,
            "track_name": metadata.get("track_name"),
            "artist_names": metadata.get("artist_names"),
            "album_name": metadata.get("album_name"),
            "vibe_description": vibe_description,
            "distance": distance,
            "genres": metadata.get("genres"),
            "popularity": metadata.get("popularity"),
            "spotify_url": metadata.get("spotify_url"),
        })
