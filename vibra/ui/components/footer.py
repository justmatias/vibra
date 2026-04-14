import streamlit as st


def render_footer() -> None:
    """Render the application footer."""
    st.markdown(
        """
        <div class="footer">
            <p>
                Made with 💚 for music lovers · 
                <a href="https://developer.spotify.com/">Spotify API</a> · 
                <a href="https://streamlit.io/">Streamlit</a> · 
                <a href="https://www.trychroma.com/">ChromaDB</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
