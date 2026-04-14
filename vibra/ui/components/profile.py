import streamlit as st

from vibra.domain import SpotifyUser

DEFAULT_AVATAR = "https://i.scdn.co/image/ab6775700000ee8555c25988a6ac314394d3fbf5"


def render_user_profile(user: SpotifyUser) -> None:
    """Render a compact user profile card for the sidebar column."""
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
