import streamlit as st
from PIL import Image, ImageFont, ImageDraw

BASECARD = Image.open("docs/images/basic-template.png")

WIDTH, LENGTH = BASECARD.size
FONT, FONTHEIGHT = ImageFont.truetype("docs/font/Ravise-Regular.ttf", 45), 45
FONT_subtitle = ImageFont.truetype("docs/font/Bogart-Regular-trial.ttf", 24)
# FONT, FONTHEIGHT = ImageFont.truetype("docs/font/Bogart-Semibold-trial.ttf", 45), 30
offset = 80


def add_illustration(card: Image, illustration):
    x, y = illustration.size
    ratio = y / x

    size = st.sidebar.slider(
        "Changer la taille de la photo", min_value=20, max_value=200, value=100
    )
    horizon = st.sidebar.slider(
        "Déplacer photo horizontalement", min_value=-200, max_value=100, value=0
    )
    vertical = st.sidebar.slider(
        "Déplacer photo verticalement", min_value=-200, max_value=100, value=0
    )

    resized_illustration = illustration.resize(
        (
            int((WIDTH - offset) * size / 100),
            int((WIDTH - offset) * ratio * size / 100),
        ),
        Image.LANCZOS,
    )

    card.paste(resized_illustration, (horizon + offset // 2, vertical + offset // 2))
    card.paste(BASECARD, (0, 0), BASECARD)


def add_bandeau(card: Image):
    bandeau_couleur = st.sidebar.selectbox(
        "Couleur du bandeau", ("Gris", "Rouge", "Bleu", "Violet")
    )
    bandeau = Image.open(f"docs/images/bandeau-{bandeau_couleur.lower()}.png")

    card.paste(bandeau, (0, 0), bandeau)


def add_person_corner(card: Image):
    person_corner = st.sidebar.checkbox("Coin 'personnage'", value=False)
    if person_corner:
        person_logo = Image.open("docs/images/person-corner.png")
        card.paste(person_logo, (0, 0), person_logo)


def add_card_name(draw: ImageDraw):
    text = st.sidebar.text_input("Nom de la  carte", value="Carte")
    w, _ = draw.textsize(text, font=FONT)
    draw.text(((WIDTH - w) / 2 - 1, FONTHEIGHT - 1), text=text, fill="black", font=FONT)
    draw.text(((WIDTH - w) / 2, FONTHEIGHT), text=text, fill="white", font=FONT)


def add_card_type(card: Image, draw: ImageDraw):
    card_type = st.sidebar.checkbox("Sous-titre du bandeau", value=False)
    if card_type:
        subtitle = Image.open("docs/images/sous-titre.png")
        card.paste(subtitle, (0, 0), subtitle)
        text = st.sidebar.text_input("Texte sous-titre", value="Compagnon")
        w, _ = draw.textsize(text, font=FONT_subtitle)
        draw.text(((WIDTH - w) / 2, 94), text=text, fill="white", font=FONT_subtitle)


def make_card(illustration):
    card = BASECARD.copy()
    draw = ImageDraw.Draw(card)

    if illustration is None:
        illustration = Image.open("docs/images/basic_illustration.PNG")
    else:
        illustration = Image.open(illustration)

    add_illustration(card, illustration)
    add_bandeau(card)
    add_person_corner(card)
    add_card_name(draw)
    add_card_type(card, draw)

    return card


footer = """<style>
a:link , a:visited{
color: red;
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: gray;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with 💖 by <a style='display: block; text-align: center;' href="https://htilquin.github.io/" target="_blank">Hélène T.</a></p>
</div>
"""
