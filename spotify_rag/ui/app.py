"""
Spotify RAG - Semantic Vibe Searcher
A beautiful Streamlit UI for Spotify authentication and music discovery.
"""

from pathlib import Path

import streamlit as st

from spotify_rag.domain import SpotifyUser
from spotify_rag.infrastructure import SpotifyAuthManager, SpotifyClient
from spotify_rag.utils import Settings

CSS_FILE = Path(__file__).parent / "styles.css"
DEFAULT_AVATAR = "https://i.scdn.co/image/ab6775700000ee8555c25988a6ac314394d3fbf5"


def configure_page() -> None:
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Spotify RAG",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def inject_custom_css() -> None:
    """Inject custom CSS for premium styling."""
    css_content = CSS_FILE.read_text()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def render_hero_section() -> None:
    """Render the hero section with title and description."""
    st.markdown(
        """
        <div class="hero-section">
            <h1 class="hero-title">🎵 Spotify RAG</h1>
            <p class="hero-subtitle">
                Discover music by mood, not just metadata.
            </p>
            <p class="hero-subtitle">
                Search your liked songs semantically and find the perfect track for any moment.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_features() -> None:
    """Render the features section."""
    st.markdown(
        """
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Semantic Search</div>
                <div class="feature-description">
                    Search by vibe, mood, or scenario. Find "music for coding late at night"
                    or "upbeat morning energy."
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI-Powered</div>
                <div class="feature-description">
                    Advanced AI understands the emotional context of your music
                    and your search queries.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💚</div>
                <div class="feature-title">Your Library</div>
                <div class="feature-description">
                    Works exclusively with your liked songs. Every recommendation
                    is a song you already love.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_login_button(auth_url: str) -> None:
    """Render the Spotify login button."""
    st.markdown(
        f"""
        <div style="text-align: center; margin: 2rem 0;">
            <a href="{auth_url}" class="spotify-btn">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
                </svg>
                Connect with Spotify
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_user_profile(user: SpotifyUser) -> None:
    """Render the logged-in user's profile."""
    avatar_url = user.image_url or DEFAULT_AVATAR

    st.markdown(
        f"""
        <div class="profile-card">
            <img src="{avatar_url}" alt="Profile" class="profile-image">
            <div class="profile-name">{user.display_name}</div>
            <div class="profile-email">{user.email or "Email not available"}</div>
            <span class="profile-badge">{user.product or "Free"} Account</span>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{user.followers:,}</div>
                    <div class="stat-label">Followers</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{user.country or "N/A"}</div>
                    <div class="stat-label">Country</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">✓</div>
                    <div class="stat-label">Connected</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    """Render the sidebar content."""
    with st.sidebar:
        st.markdown("### 🎵 Spotify RAG")
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
        st.markdown("[📖 Documentation](https://github.com/matiagimenez/spotify-rag)")
        st.markdown(
            "[🐛 Report Issue](https://github.com/matiagimenez/spotify-rag/issues)"
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


def handle_oauth_callback() -> str | None:
    """Handle OAuth callback and extract authorization code."""
    query_params = st.query_params
    return query_params.get("code")


def initialize_session_state() -> None:
    """Initialize session state variables."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "user" not in st.session_state:
        st.session_state.user = None


def app() -> None:
    """Main application entry point."""
    configure_page()
    inject_custom_css()
    initialize_session_state()

    try:
        auth_manager = SpotifyAuthManager()

        # Ensure cache directory exists
        Settings.CACHE_PATH.mkdir(parents=True, exist_ok=True)

    except Exception as e:
        render_sidebar()
        render_hero_section()
        st.error(f"⚠️ Configuration Error: {str(e)}")
        st.info(
            """
            **Setup Required:**
            1. Copy `.env.example` to `.env`
            2. Add your Spotify API credentials
            3. Restart the application
            """
        )
        render_features()
        return

    render_sidebar()

    # Handle OAuth callback
    code = handle_oauth_callback()
    if code and not st.session_state.authenticated:
        with st.spinner("🔐 Authenticating with Spotify..."):
            token_info = auth_manager.get_access_token(code)
            if token_info:
                st.session_state.authenticated = True
                st.session_state.access_token = token_info["access_token"]

                # Get user profile
                client = SpotifyClient(access_token=token_info["access_token"])
                st.session_state.user = client.current_user

                # Clear the URL parameters
                st.query_params.clear()
                st.rerun()
            else:
                st.error("❌ Authentication failed. Please try again.")

    # Check for cached token
    if not st.session_state.authenticated:
        cached_token = auth_manager.get_cached_token()
        if cached_token:
            st.session_state.authenticated = True
            st.session_state.access_token = cached_token["access_token"]

            client = SpotifyClient(access_token=cached_token["access_token"])
            st.session_state.user = client.current_user

    # Main content
    if st.session_state.authenticated and st.session_state.user:
        # Logged in view
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            render_user_profile(st.session_state.user)

            st.markdown("### 🚀 What's Next?")

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📥 Sync Library", use_container_width=True):
                    st.info("🔄 Library sync coming soon!")

            with col_b:
                if st.button("🔍 Search Vibes", use_container_width=True):
                    st.info("🎵 Semantic search coming soon!")

            st.markdown("---")

            if st.button("🚪 Disconnect", use_container_width=True):
                # Clear session and cached token
                st.session_state.authenticated = False
                st.session_state.access_token = None
                st.session_state.user = None

                # Remove cached token file
                cache_file = Settings.CACHE_PATH / ".spotify_cache"
                if cache_file.exists():
                    cache_file.unlink()

                st.rerun()

    else:
        # Logged out view
        render_hero_section()
        auth_url = auth_manager.get_auth_url()
        render_login_button(auth_url)
        render_features()

    # Footer
    st.markdown(
        """
        <div class="footer">
            <p>Made with 💚 for music lovers |
            <a href="https://developer.spotify.com/">Spotify API</a> |
            <a href="https://streamlit.io/">Streamlit</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
