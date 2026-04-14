import streamlit as st

from vibra.domain import SpotifyUser
from vibra.utils import Settings

DEFAULT_AVATAR = "https://i.scdn.co/image/ab6775700000ee8555c25988a6ac314394d3fbf5"


def render_sidebar(user: SpotifyUser | None = None) -> None:
    """Render the sidebar with optional user profile and how-it-works guide."""
    with st.sidebar:
        st.markdown("### 🎵 Vibra")
        st.markdown("---")

        # Show profile + disconnect if authenticated
        if user:
            _render_sidebar_profile(user)
            st.markdown("---")

        st.markdown("#### How it works")
        st.markdown(
            """
            <div class="sidebar-step">
                <div class="step-number">1</div>
                <div class="step-text"><strong>Connect</strong> your Spotify account to get started.</div>
            </div>
            <div class="sidebar-step">
                <div class="step-number">2</div>
                <div class="step-text"><strong>Sync</strong> your liked songs so the AI can analyze them.</div>
            </div>
            <div class="sidebar-step">
                <div class="step-number">3</div>
                <div class="step-text"><strong>Search</strong> by mood, scenario, or emotion — not keywords.</div>
            </div>
            <div class="sidebar-step">
                <div class="step-number">4</div>
                <div class="step-text"><strong>Discover</strong> the perfect track buried in your library.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(
            """
            <div style="font-size: 0.8rem; color: #6a6a6a; text-align: center;">
                Built with ❤️ & 🧉
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_sidebar_profile(user: SpotifyUser) -> None:
    """Render a compact user profile inside the sidebar with disconnect button."""
    avatar_url = user.image_url or DEFAULT_AVATAR

    st.markdown(
        f"""
        <div class="profile-card">
            <img src="{avatar_url}" alt="Profile" class="profile-image">
            <div class="profile-name">{user.display_name}</div>
            <div class="profile-email">{user.email or ""}</div>
            <span class="profile-badge">{user.product or "Free"}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Disconnect button
    st.markdown('<div class="disconnect-btn">', unsafe_allow_html=True)
    if st.button("🚪 Disconnect", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.access_token = None
        st.session_state.user = None

        cache_file = Settings.CACHE_PATH / ".spotify_cache"
        if cache_file.exists():
            cache_file.unlink()

        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
