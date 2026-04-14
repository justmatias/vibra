from pathlib import Path

import streamlit as st

CSS_FILE = Path(__file__).parent / "styles" / "styles.css"


def configure_page() -> None:
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Vibra",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def inject_custom_css() -> None:
    """Inject custom CSS for premium styling."""
    if CSS_FILE.exists():
        css_content = CSS_FILE.read_text()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found: {CSS_FILE}")


def initialize_session_state() -> None:
    """Initialize session state variables."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "user" not in st.session_state:
        st.session_state.user = None
