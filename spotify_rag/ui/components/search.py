import streamlit as st

from spotify_rag.domain import SearchResults
from spotify_rag.injections import container


def render_search_section() -> None:
    if st.button("🔍 Search Vibes", use_container_width=True):
        st.session_state.show_search = True

    if st.session_state.get("show_search", False):
        st.markdown("### 🔍 Semantic Vibe Search")
        st.caption(
            "Describe the vibe you're looking for in natural language. "
            "The AI will find tracks that match your description."
        )

        query = st.text_input(
            "What vibe are you looking for?",
            placeholder="e.g., 'melancholic indie songs about lost love' or 'upbeat party anthems'",
            key="vibe_query",
        )

        col1, col2 = st.columns([3, 1])
        with col1:
            n_results = st.slider(
                "Number of results",
                min_value=5,
                max_value=20,
                value=10,
                step=5,
            )
        with col2:
            search_button = st.button(
                "Search", type="primary", use_container_width=True
            )

        if search_button and query:
            with st.spinner("🔎 Searching for matching vibes..."):
                # Get search service from container
                search_service = container.services.search_service()

                # Perform semantic search
                results = search_service.search_by_vibe(query, n_results=n_results)

                # Display results
                _render_search_results(results)


def _render_search_results(results: SearchResults) -> None:
    """Render the search results.

    Args:
        results: Search results from search service.
    """
    if not results.has_results:
        st.warning(
            "No tracks found matching your vibe. Try syncing your library first!"
        )
        return

    st.success(f"✨ Found {results.total_results} tracks matching: *'{results.query}'*")

    for idx, result in enumerate(results.results, start=1):
        with st.container():
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"**{idx}. {result.track_name}**")
                st.caption(f"🎤 {result.artist_names} • 📀 {result.album_name}")

            with col2:
                st.metric("Match", f"{result.similarity_score:.0%}")

            st.info(f"🎭 **Vibe:** {result.vibe_description}")

            # Additional metadata
            with st.expander("📊 Track Details"):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Popularity", f"{result.popularity}/100")
                with col_b:
                    st.caption(f"**Genres:** {result.genres or 'N/A'}")
                with col_c:
                    if result.spotify_url:
                        st.link_button(
                            "🎵 Open in Spotify",
                            result.spotify_url,
                            use_container_width=True,
                        )

            st.markdown("---")
