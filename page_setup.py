import streamlit as st

def setup_page():
    st.set_page_config(initial_sidebar_state="collapsed")

    st.markdown(
        """
        <style>
            [data-testid="stSidebarContent"] {
                display: none
            }
            [data-testid="collapsedControl"] {
                display: none
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
