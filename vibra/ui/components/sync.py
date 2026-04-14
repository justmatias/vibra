import streamlit as st

from vibra.domain import EnrichedTrack, SyncProgress
from vibra.injections import container


def render_sync_library_section(access_token: str) -> None:
    """Render the sync library section with inline slider and button.

    Args:
        access_token: Spotify access token for authentication.
    """
    col_slider, col_btn = st.columns([3, 1])
    with col_slider:
        track_limit = st.slider(
            "Songs to analyze",
            min_value=5,
            max_value=100,
            value=20,
            step=5,
            label_visibility="collapsed",
        )
    with col_btn:
        sync_clicked = st.button("📥 Sync Library")

    if sync_clicked:
        # Configure container with access token
        container.infrastructure.config.spotify.access_token.from_value(access_token)

        # Get service from container
        sync_service = container.services.library_sync_service()

        # Create progress containers
        progress_bar = st.progress(0)
        status_container = st.empty()
        results_container = st.container()

        enriched_tracks: list[EnrichedTrack] = []

        # Process library sync
        for item in sync_service.sync_library(limit=track_limit):
            if isinstance(item, SyncProgress):
                # Update progress
                progress = item.current / item.total
                progress_bar.progress(progress)
                status_container.markdown(
                    f"""
                    <div class="track-card" style="margin: 0;">
                        <div class="track-number">{item.current}/{item.total}</div>
                        <div class="track-info">
                            <div class="track-name">{item.song_title}</div>
                            <div class="track-artist">{item.artist_name}</div>
                        </div>
                        <div class="track-badge lyrics">Processing…</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif isinstance(item, EnrichedTrack):
                # Store enriched track
                enriched_tracks.append(item)

        # Complete
        progress_bar.progress(1.0)
        status_container.success(
            f"✅ Successfully synced **{len(enriched_tracks)}** tracks!"
        )

        # Display summary
        _render_sync_summary(results_container, enriched_tracks)


def _render_sync_summary(
    container: st.delta_generator.DeltaGenerator,
    enriched_tracks: list[EnrichedTrack],
) -> None:
    """Render the sync summary with metrics and styled track list.

    Args:
        container: Streamlit container to render into.
        enriched_tracks: List of enriched tracks to display.
    """
    with container:
        tracks_with_lyrics = sum(1 for t in enriched_tracks if t.has_lyrics)
        tracks_with_vibes = sum(1 for t in enriched_tracks if t.vibe_description)
        total = len(enriched_tracks)

        # Stats row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎵 Total Synced", total)
        with col2:
            st.metric("📝 With Lyrics", f"{tracks_with_lyrics}/{total}")
        with col3:
            st.metric("🎭 With Vibes", f"{tracks_with_vibes}/{total}")

        # Track list
        with st.expander(
            f"🎵 View Synced Tracks ({min(10, total)} shown)", expanded=True
        ):
            for i, enriched in enumerate(enriched_tracks[:10], start=1):
                track = enriched.track.track

                # Build badge HTML
                if enriched.has_lyrics:
                    badge = f'<span class="track-badge lyrics">✅ Lyrics ({len(enriched.lyrics)} chars)</span>'
                else:
                    badge = '<span class="track-badge no-lyrics">❌ No lyrics</span>'

                st.markdown(
                    f"""
                    <div class="track-card">
                        <div class="track-number">{i}</div>
                        <div class="track-info">
                            <div class="track-name">{track.name}</div>
                            <div class="track-artist">{track.artist_names}</div>
                        </div>
                        {badge}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if enriched.vibe_description:
                    st.markdown(
                        f"""
                        <div class="result-vibe" style="margin: 0 0 0.5rem 2.5rem;">
                            🎭 {enriched.vibe_description}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
