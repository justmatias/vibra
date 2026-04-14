import asyncio

import streamlit as st

from vibra.domain import SearchResults
from vibra.injections import container


def render_search_section() -> None:
    """Render the semantic search section — always visible."""
    st.markdown("#### 🔍 Vibe Search")
    st.caption("Describe a mood, feeling or scenario to find matching tracks.")

    col_input, col_n, col_btn = st.columns([5, 1, 2])
    with col_input:
        query = st.text_input(
            "What vibe are you looking for?",
            placeholder="e.g., 'melancholic indie songs about lost love'",
            key="vibe_query",
            label_visibility="collapsed",
        )
    with col_n:
        n_results = st.selectbox(
            "Results", [5, 10, 15, 20], index=1, label_visibility="collapsed"
        )
    with col_btn:
        search_button = st.button("🎯 Find My Vibe", type="primary")

    if search_button and query:
        with st.spinner("🔎 Searching for matching vibes..."):
            search_service = container.services.search_service()

            results = asyncio.run(
                search_service.search_by_vibe(query, n_results=n_results)
            )

            _render_search_results(results)


def _render_search_results(results: SearchResults) -> None:
    """Render search results with rich visual cards.

    Args:
        results: Search results from search service.
    """
    if not results.has_results:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">🎵</div>
                <div class="empty-state-title">No matches found</div>
                <div class="empty-state-text">
                    Try syncing your library first, or adjust your search query.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.success(
        f"✨ Found **{results.total_results}** tracks matching: *'{results.query}'*"
    )

    for idx, result in enumerate(results.results, start=1):
        score_pct = result.similarity_score * 100

        st.markdown(
            f"""
            <div class="search-result-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <div class="result-title">{idx}. {result.track_name}</div>
                        <div class="result-meta">🎤 {result.artist_names}</div>
                    </div>
                    <div class="result-score">⚡ {score_pct:.0f}%</div>
                </div>
                <div class="result-vibe">🎭 {result.vibe_description}</div>
                <div class="score-bar">
                    <div class="score-bar-fill" style="width: {score_pct:.0f}%"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
