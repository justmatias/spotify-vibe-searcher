"""Track analysis service using LLM."""

from pydantic import BaseModel

from spotify_rag.domain import SavedTrack
from spotify_rag.infrastructure import LLMClient
from spotify_rag.utils import LogLevel, log


class TrackAnalysisService(BaseModel):
    llm_client: LLMClient

    def _build_analysis_prompt(self, saved_track: SavedTrack, lyrics: str) -> str:  # pylint: disable=no-self-use
        genres = []
        for artist in saved_track.track.artists:
            genres.extend(artist.genre_names)

        prompt = f"""
        Act as an expert music critic. Analyze this song:
            - **Title:** {saved_track.track.name}
            - **Artist:** {saved_track.track.artist_names}
            - **Album:** {saved_track.track.album.name}
            - **Musical Genres:** {", ".join(genres)}
            - **Popularity:** {saved_track.track.popularity}/100
            - **Lyrics Snippet:** "{lyrics}"

            **Task:**
            1. Detect the core theme of the lyrics (love, protest, grief, party, nostalgia, etc.)
            2. Analyze the emotional tone and mood of the lyrics
            3. Consider how the genre and artist style might contrast or align with the lyrical content
            4. Generate a synthetic **Vibe Description** for semantic search purposes

            **Output:** Only the descriptive sentence (max 2-3 sentences). Focus on the emotional essence and searchable characteristics.

            **Example:** "An indie folk track with melancholic lyrics about lost love and regret, delivered through poetic storytelling that evokes deep nostalgia and bittersweet reflection."

            Vibe Description:
        """

        return prompt

    def analyze_track(self, saved_track: SavedTrack, lyrics: str) -> str | None:
        try:
            prompt = self._build_analysis_prompt(saved_track, lyrics)
            vibe_description = self.llm_client.generate(prompt)
            log(
                f"Generated vibe description for: {saved_track.track.name}",
                LogLevel.INFO,
            )
            return vibe_description
        except Exception as e:
            log(f"Error analyzing track {saved_track.track.name}: {e}", LogLevel.ERROR)
            return None
