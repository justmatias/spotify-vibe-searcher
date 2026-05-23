from pydantic import BaseModel, ConfigDict

from vibra.domain import SearchResults
from vibra.domain.ports import LLMProvider, VectorStore
from vibra.utils import LogLevel, log


class SearchService(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    vectordb_repository: VectorStore
    llm_client: LLMProvider

    async def search_by_vibe(self, query: str, n_results: int = 10) -> SearchResults:
        log(f"Searching for vibe: '{query}' (max {n_results} results)", LogLevel.INFO)

        refined_query = await self._refine_query(query)
        log(f"Refined query: '{refined_query}'", LogLevel.INFO)

        raw_results = await self.vectordb_repository.search(refined_query, n_results)
        search_results = raw_results.model_copy(update={"query": query})

        log(
            f"Found {search_results.total_results} matching tracks",
            LogLevel.INFO,
        )

        return search_results

    async def _refine_query(self, query: str) -> str:
        prompt = (
            "You are an expert music curator. Rewrite the following search query to be "
            "more descriptive, capturing the mood, musical style, and lyrical themes "
            "implied by the user. This description will be used for semantic search "
            "against a database of song analyses. Return ONLY the refined query text.\n\n"
            f"Original query: '{query}'"
        )
        return await self.llm_client.generate(prompt)
