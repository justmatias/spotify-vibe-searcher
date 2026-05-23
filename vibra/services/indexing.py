from pydantic import BaseModel, ConfigDict

from vibra.domain import EnrichedTrack, VectorStore


class IndexingService(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    store: VectorStore

    async def is_indexed(self, track_id: str) -> bool:
        return await self.store.track_exists(track_id)

    async def index(self, enriched: EnrichedTrack) -> None:
        await self.store.add(enriched)
