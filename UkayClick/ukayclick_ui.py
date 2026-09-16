import streamlit as st


def money(value):
    return f"₱{float(value):,.2f}"


def apply_style():
    st.markdown(
        """
        <style>

        /* Main application background */
        .stApp {
            background: #355e3b;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #26382c;
        }

        [data-testid="stSidebar"] * {
            color: white !important;
        }

        /* Main headings */
        h1, h2, h3 {
            color: #ffffff !important;
        }

        /* General text */
        .stApp p,
        .stApp label {
            color: #f2f2f2;
        }

        /* Buttons */
        .stButton > button {
            background-color: #26382c;
            color: white;
            border: 1px solid #6fa77b;
        }

        .stButton > button:hover {
            background-color: #467a52;
            color: white;
        }

        /* Input boxes */
        .stTextInput input,
        .stNumberInput input {
            background-color: #26382c;
            color: white;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )