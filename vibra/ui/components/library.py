# pylint: disable=too-many-locals
import asyncio

import pandas as pd
import streamlit as st

from vibra.injections import container


@st.fragment
def render_library_section() -> None:
    """Render the library section showing indexed tracks with improved visuals."""
    st.markdown(
        """
        <div class="dashboard-card">
            <div class="dashboard-card-header">
                <span class="dashboard-card-icon">📚</span>
                <h3 class="dashboard-card-title">Knowledge Base</h3>
            </div>
            <p class="dashboard-card-description">
                Browse the tracks indexed in your local vector database — these are searchable by vibe.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    repository = container.infrastructure.vectordb_repository()
    count = asyncio.run(repository.count())

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.metric("🗄️ Indexed Tracks", count)

    with col2:
        if st.button("🔄 Refresh", key="refresh_library"):
            st.rerun()

    with col3:
        if count > 0 and st.button(
            "🗑️ Clear Database", key="clear_library", type="secondary"
        ):
            with st.spinner("Clearing database..."):
                tracks = asyncio.run(repository.list_all())
                track_ids = [t.id for t in tracks]
                if track_ids:
                    asyncio.run(repository.delete(track_ids))
                    st.success(f"✅ Deleted {len(track_ids)} tracks from database!")
                    st.rerun()

    if count > 0:
        with st.spinner("Loading tracks..."):
            tracks = asyncio.run(repository.list_all())

        if not tracks:
            st.info("No tracks found.")
            return

        rows = [
            {
                "Track": f"{t.spotify_url}#{t.track_name}" if t.spotify_url else t.track_name,
                "Artist": t.artist_names,
                "Album": t.album_name,
                "Vibe": t.vibe_description,
                "Popularity": t.popularity,
            }
            for t in tracks
        ]

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            column_config={
                "Track": st.column_config.LinkColumn(
                    "Track",
                    display_text=r".*#(.+)",
                ),
                "Vibe": st.column_config.TextColumn("Vibe Description", width="large"),
                "Popularity": st.column_config.ProgressColumn(
                    "Popularity",
                    help="Track popularity on Spotify",
                    format="%d",
                    min_value=0,
                    max_value=100,
                ),
            },
            column_order=["Track", "Artist", "Album", "Vibe", "Popularity"],
            width="stretch",
            hide_index=True,
        )
    else:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">📦</div>
                <div class="empty-state-title">Knowledge base is empty</div>
                <div class="empty-state-text">
                    Sync your library above to start indexing tracks for vibe search.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
