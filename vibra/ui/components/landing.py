import streamlit as st


def render_hero_section() -> None:
    """Render the hero section with animated title and description."""
    st.markdown(
        """
        <div class="hero-section">
            <h1 class="hero-title">🎵 Vibra</h1>
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
    """Render the features section with animated cards."""
    st.markdown(
        """
        <div class="feature-grid">
            <div class="feature-card animate-in animate-in-delay-1">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Semantic Search</div>
                <div class="feature-description">
                    Search by vibe, mood, or scenario. Find "music for coding late at night"
                    or "upbeat morning energy."
                </div>
            </div>
            <div class="feature-card animate-in animate-in-delay-2">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI-Powered</div>
                <div class="feature-description">
                    Advanced AI understands the emotional context of your music
                    and your search queries.
                </div>
            </div>
            <div class="feature-card animate-in animate-in-delay-3">
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
