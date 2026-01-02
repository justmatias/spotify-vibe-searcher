import pandas as pd
import streamlit as st

from spotify_rag.injections import container


def render_library_section() -> None:
    """Render the library section showing indexed tracks."""
    st.markdown("### 📚 Knowledge Base")
    st.caption("Explore the tracks currently indexed in your local vector database.")

    repository = container.infrastructure.vectordb_repository()
    count = repository.count_tracks()

    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("Indexed Tracks", count)

    with col2:
        if st.button("🔄 Refresh", key="refresh_library"):
            st.rerun()

    if count > 0:
        with st.expander("View All Tracks", expanded=True):
            with st.spinner("Loading tracks..."):
                data = repository.get_all_tracks()

                if not data or not data["ids"]:
                    st.info("No tracks found.")
                    return

                # Parse data into a format suitable for DataFrame
                rows = []
                ids = data["ids"]
                # metadatas and documents might be None if empty, but count > 0 so likely not.
                # chroma returns lists.
                metadatas = data["metadatas"] or []
                documents = data["documents"] or []

                for i, _ in enumerate(ids):
                    # safely get metadata and document
                    meta = metadatas[i] if i < len(metadatas) else {}
                    doc = documents[i] if i < len(documents) else ""

                    rows.append({
                        "Track": meta.get("track_name", "Unknown"),
                        "Artist": meta.get("artist_names", "Unknown"),
                        "Album": meta.get("album_name", "Unknown"),
                        "Vibe": doc,
                        "Genres": meta.get("genres", ""),
                        "Popularity": meta.get("popularity", 0),
                        "Spotify URL": meta.get("spotify_url", ""),
                    })

                df = pd.DataFrame(rows)

                st.dataframe(
                    df,
                    column_config={
                        "Spotify URL": st.column_config.LinkColumn("Link"),
                        "Vibe": st.column_config.TextColumn(
                            "Vibe Description", width="large"
                        ),
                        "Popularity": st.column_config.ProgressColumn(
                            "Popularity",
                            help="Track popularity on Spotify",
                            format="%d",
                            min_value=0,
                            max_value=100,
                        ),
                    },
                    width="stretch",
                    hide_index=True,
                )
    else:
        st.info("Your knowledge base is empty. Sync your library to add tracks!")
