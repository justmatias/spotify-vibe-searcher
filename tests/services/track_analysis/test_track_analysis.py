import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import SavedTrack, SpotifyArtist, SpotifyTrack
from vibra.infrastructure import FakeLLMClient
from vibra.services import TrackAnalysisService


@pytest.mark.asyncio
async def test_analyze_track_returns_vibe_description(
    track_analysis_service: TrackAnalysisService,
    sample_saved_track: SavedTrack,
    sample_lyrics: str,
    llm_client: FakeLLMClient,
) -> None:
    result = await track_analysis_service.analyze_track(sample_saved_track, sample_lyrics)

    assert result == llm_client.response
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_analyze_track_builds_prompt_with_track_metadata(
    track_analysis_service: TrackAnalysisService,
    sample_saved_track: SavedTrack,
    simple_lyrics: str,
) -> None:
    prompt = track_analysis_service._build_analysis_prompt(  # pylint: disable=protected-access
        sample_saved_track, simple_lyrics
    )

    assert sample_saved_track.track.name in prompt
    assert sample_saved_track.track.album.name in prompt
    assert simple_lyrics in prompt
    assert "Vibe Description" in prompt


@pytest.mark.asyncio
async def test_analyze_track_returns_none_on_llm_error(
    sample_saved_track: SavedTrack,
    simple_lyrics: str,
) -> None:
    class ErrorLLMClient:
        async def generate(self, prompt: str) -> str:  # pylint: disable=no-self-use
            raise RuntimeError("LLM unavailable")

    service = TrackAnalysisService(llm_client=ErrorLLMClient())
    result = await service.analyze_track(sample_saved_track, simple_lyrics)

    assert result is None


@pytest.mark.asyncio
async def test_analyze_track_includes_genre_in_prompt(
    track_analysis_service: TrackAnalysisService,
    spotify_artist_factory: ModelFactory[SpotifyArtist],
    spotify_track_factory: ModelFactory[SpotifyTrack],
    saved_track_factory: ModelFactory[SavedTrack],
    simple_lyrics: str,
) -> None:
    artist = spotify_artist_factory.build(genres=["jazz", "soul"])
    track = spotify_track_factory.build(artists=[artist])
    saved_track = saved_track_factory.build(track=track)

    prompt = track_analysis_service._build_analysis_prompt(saved_track, simple_lyrics)  # pylint: disable=protected-access

    assert "jazz" in prompt or "soul" in prompt
