import streamlit as st
from utils_app import *


st.set_page_config(
    page_title="Card Maker",
    page_icon="🃏",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "About": """### Card Maker 
    \nTemplate for cards for our family game.
    \n ---
    """
    },
)

st.sidebar.markdown("# Options !")
st.sidebar.markdown("## Image")
illustration = st.sidebar.file_uploader(
    "Sélectionner une photo ou une image qui servira d'illustration",
    type=["png", "jpg", "jpeg"],
)

st.markdown("## Card Maker !")
st.markdown("Petit outil pour faire des cartes à jouer personnalisées.")

card = make_card(illustration)

st.image(card)
