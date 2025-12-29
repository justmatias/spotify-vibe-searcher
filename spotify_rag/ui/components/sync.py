"""Library sync component for Streamlit UI."""

import streamlit as st

from spotify_rag.domain import EnrichedTrack, SyncProgress
from spotify_rag.injections import container


def render_sync_library_section(access_token: str, track_limit: int) -> None:
    """Render the sync library button and handle the sync process.

    Args:
        access_token: Spotify access token for authentication.
        track_limit: Maximum number of tracks to sync.
    """
    if st.button("📥 Sync Library", use_container_width=True):
        # Configure container with access token
        container.infrastructure.config.spotify.access_token.from_value(access_token)

        # Get service from container
        sync_service = container.services.library_sync_service()

        # Create progress containers
        progress_bar = st.progress(0)
        status_text = st.empty()
        results_container = st.container()

        enriched_tracks: list[EnrichedTrack] = []

        # Process library sync
        for item in sync_service.sync_library(limit=track_limit):
            if isinstance(item, SyncProgress):
                # Update progress
                progress = item.current / item.total
                progress_bar.progress(progress)
                status_text.text(
                    f"🎵 Processing {item.current}/{item.total}: "
                    f"{item.song_title} - {item.artist_name}"
                )
            elif isinstance(item, EnrichedTrack):
                # Store enriched track
                enriched_tracks.append(item)

        # Complete
        progress_bar.progress(1.0)
        status_text.success(f"✅ Synced {len(enriched_tracks)} tracks!")

        # Display summary
        _render_sync_summary(results_container, enriched_tracks)


def _render_sync_summary(
    container: st.delta_generator.DeltaGenerator,
    enriched_tracks: list[EnrichedTrack],
) -> None:
    """Render the sync summary with metrics and track list.

    Args:
        container: Streamlit container to render into.
        enriched_tracks: List of enriched tracks to display.
    """
    with container:
        st.markdown("### 📊 Sync Summary")
        tracks_with_lyrics = sum(1 for t in enriched_tracks if t.has_lyrics)
        st.metric(
            "Tracks with Lyrics",
            f"{tracks_with_lyrics}/{len(enriched_tracks)}",
        )

        # Show sample tracks
        with st.expander("🎵 View Synced Tracks"):
            for enriched in enriched_tracks[:5]:
                track = enriched.track.track
                st.markdown(f"**{track.name}** - {track.artist_names}")
                if enriched.has_lyrics:
                    st.caption(f"✅ Lyrics found ({len(enriched.lyrics)} chars)")
                else:
                    st.caption("❌ No lyrics found")
