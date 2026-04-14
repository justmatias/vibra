"""
Spotify RAG - Semantic Vibe Searcher
A beautiful Streamlit UI for Spotify authentication and music discovery.
"""

import streamlit as st

from vibra.domain import SpotifyUser
from vibra.infrastructure import SpotifyAuthManager
from vibra.injections import container
from vibra.utils import Settings

from .components import (
    render_features,
    render_footer,
    render_hero_section,
    render_library_section,
    render_login_button,
    render_search_section,
    render_sidebar,
    render_sync_library_section,
)
from .config import (
    configure_page,
    initialize_session_state,
    inject_custom_css,
)


def handle_oauth_callback() -> str | None:
    """Handle OAuth callback and extract authorization code."""
    query_params = st.query_params
    return query_params.get("code")


def authenticate_with_code(auth_manager: SpotifyAuthManager, code: str) -> None:
    """Authenticate with Spotify using the authorization code."""
    with st.spinner("🔐 Authenticating with Spotify..."):
        if token_info := auth_manager.get_access_token(code):
            st.session_state.authenticated = True
            st.session_state.access_token = token_info["access_token"]

            # Get user profile using DI container
            container.infrastructure.config.spotify.access_token.from_value(
                token_info["access_token"]
            )
            client = container.infrastructure.spotify_client()
            st.session_state.user = client.current_user

            # Clear the URL parameters
            st.query_params.clear()
            st.rerun()
        else:
            st.error("❌ Authentication failed. Please try again.")


def check_cached_token(auth_manager: SpotifyAuthManager) -> None:
    """Check for and restore cached authentication token."""

    if cached_token := auth_manager.get_cached_token():
        st.session_state.authenticated = True
        st.session_state.access_token = cached_token["access_token"]

        # Get user profile using DI container
        container.infrastructure.config.spotify.access_token.from_value(
            cached_token["access_token"]
        )
        client = container.infrastructure.spotify_client()
        st.session_state.user = client.current_user


def render_authenticated_view(user: SpotifyUser) -> None:
    """Render the authenticated dashboard — full width."""
    # ── Search (always visible, on top) ────────────────────
    render_search_section()

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ── Sync ────────────────────────────────────────────────
    st.markdown("#### 📥 Sync Library")
    st.caption("⚠️ Analyzing lyrics takes time (~2-3 sec per song).")

    render_sync_library_section(
        access_token=st.session_state.access_token,
    )

    # ── Library / Knowledge Base ────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    render_library_section()


def render_unauthenticated_view(auth_manager: SpotifyAuthManager) -> None:
    """Render the view for unauthenticated users."""
    render_hero_section()
    auth_url = auth_manager.get_auth_url()
    render_login_button(auth_url)
    render_features()


def app() -> None:
    """Main application entry point."""
    configure_page()
    inject_custom_css()
    initialize_session_state()

    try:
        auth_manager = SpotifyAuthManager()
        # Ensure cache directory exists
        Settings.CACHE_PATH.mkdir(parents=True, exist_ok=True)

    except Exception as e:  # noqa: BLE001
        render_sidebar()
        render_hero_section()
        st.error(f"⚠️ Configuration Error: {e!s}")
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

    # Handle OAuth callback
    code = handle_oauth_callback()
    if code and not st.session_state.authenticated:
        authenticate_with_code(auth_manager, code)

    # Check for cached token
    if not st.session_state.authenticated:
        check_cached_token(auth_manager)

    # Render sidebar (pass user if authenticated)
    user = st.session_state.user if st.session_state.authenticated else None
    render_sidebar(user)

    # Main content
    if st.session_state.authenticated and user:
        render_authenticated_view(user)
    else:
        render_unauthenticated_view(auth_manager)

    render_footer()
