# pylint: disable=too-many-locals
import pandas as pd
import streamlit as st

from vibra.injections import container


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
    count = repository.count_tracks()

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
                all_data = repository.get_all_tracks()
                track_ids = all_data.get("ids", [])
                if track_ids:
                    repository.delete_tracks(track_ids)
                    st.success(f"✅ Deleted {len(track_ids)} tracks from database!")
                    st.rerun()

    if count > 0:
        with st.spinner("Loading tracks..."):
            data = repository.get_all_tracks()

            if not data or not data["ids"]:
                st.info("No tracks found.")
                return

            # Parse data into a format suitable for DataFrame
            rows = []
            ids = data["ids"]
            metadatas = data.get("metadatas") or []
            documents = data.get("documents") or []

        for i, _ in enumerate(ids):
            meta = metadatas[i] if i < len(metadatas) else {}
            doc = documents[i] if i < len(documents) else ""

            # Embed track name in URL fragment so LinkColumn can display it
            track_name = meta.get("track_name", "Unknown")
            spotify_url = meta.get("spotify_url", "")
            track_link = f"{spotify_url}#{track_name}" if spotify_url else track_name

            rows.append({
                "Track": track_link,
                "Artist": meta.get("artist_names", "Unknown"),
                "Album": meta.get("album_name", "Unknown"),
                "Vibe": doc,
                "Popularity": meta.get("popularity", 0),
            })

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
