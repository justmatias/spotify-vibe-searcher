import streamlit as st


def render_sidebar() -> None:
    """Render the sidebar content."""
    with st.sidebar:
        st.markdown("### 🎵 Spotify Vibe Searcher")
        st.markdown("---")

        st.markdown("#### How it works")
        st.markdown(
            """
            1. **Connect** your Spotify account
            2. **Sync** your liked songs
            3. **Search** by mood or vibe
            4. **Discover** perfect matches
            """
        )

        st.markdown("---")
        st.markdown("#### Quick Links")
        st.markdown(
            "[📖 Documentation](https://github.com/justmatias/spotify-vibe-searcher)"
        )
        st.markdown(
            "[🐛 Report Issue](https://github.com/justmatias/spotify-vibe-searcher/issues)"
        )

        st.markdown("---")
        st.markdown(
            """
            <div style="font-size: 0.8rem; color: #666;">
                Built with ❤️ & 🧉
            </div>
            """,
            unsafe_allow_html=True,
        )
