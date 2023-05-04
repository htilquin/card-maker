import streamlit as st
from PIL import Image, ImageFont, ImageDraw
from image_utils import ImageText # noqa

BASECARD = Image.open("docs/images/basic-template.png")

WIDTH, LENGTH = BASECARD.size
FONT, FONTHEIGHT = ImageFont.truetype("docs/font/Ravise-Regular.ttf", 45), 45
FONT_skill, FONTHEIGHT_skill = (
    ImageFont.truetype("docs/font/Ravise-Regular.ttf", 50),
    50,
)
FONT_subtitle = ImageFont.truetype("docs/font/Bogart-Regular-trial.ttf", 24)
# FONT, FONTHEIGHT = ImageFont.truetype("docs/font/Bogart-Semibold-trial.ttf", 45), 30
offset = 80


def add_illustration(card: Image.Image, illustration):
    x, y = illustration.size
    ratio = y / x

    size = st.sidebar.slider(
        "Changer la taille de la photo", min_value=20, max_value=300, value=100
    )
    horizon = st.sidebar.slider(
        "Déplacer photo horizontalement", min_value=-400, max_value=100, value=0
    )
    vertical = st.sidebar.slider(
        "Déplacer photo verticalement", min_value=-400, max_value=100, value=0
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


def add_bandeau(card: Image.Image):
    bandeau_couleur = st.sidebar.selectbox(
        "Couleur du bandeau", ("Gris", "Rouge", "Bleu", "Violet", "Jaune")
    )
    bandeau = Image.open(f"docs/images/bandeau-{bandeau_couleur.lower()}.png")

    card.paste(bandeau, (0, 0), bandeau)


def add_person_corner(card: Image.Image):
    person_corner = st.sidebar.checkbox("Coin 'personnage'", value=False)
    if person_corner:
        person_logo = Image.open("docs/images/person-corner.png")
        card.paste(person_logo, (0, 0), person_logo)


def add_card_name(draw: ImageDraw.ImageDraw):
    text = st.sidebar.text_input("Nom de la  carte", value="Carte")
    w, _ = draw.textsize(text, font=FONT)
    draw.text(((WIDTH - w) / 2 - 1, FONTHEIGHT - 1), text=text, fill="black", font=FONT)
    draw.text(((WIDTH - w) / 2, FONTHEIGHT), text=text, fill="white", font=FONT)


def add_card_type(card: Image.Image, draw: ImageDraw.ImageDraw):
    card_type = st.sidebar.checkbox("Sous-titre du bandeau", value=False)
    if card_type:
        subtitle = Image.open("docs/images/sous-titre.png")
        card.paste(subtitle, (0, 0), subtitle)
        text = st.sidebar.text_input("Texte sous-titre", value="Compagnon")
        w, _ = draw.textsize(text, font=FONT_subtitle)
        draw.text(((WIDTH - w) / 2, 94), text=text, fill="white", font=FONT_subtitle)


def add_green_token(card: Image.Image, draw: ImageDraw.ImageDraw):
    green_token = st.sidebar.checkbox("Jeton vert", value=False)
    if green_token:
        green_logo = Image.open("docs/images/jeton_vert.png")
        card.paste(green_logo, (0, 0), green_logo)

        value_green_token = st.sidebar.select_slider(
            "Valeur du jeton vert", options=[1, 2, 3, 4, 5, 6, 7, 8, "?"], value=1
        )

        text_green_token = str(value_green_token)

        w, _ = draw.textsize(text_green_token, font=FONT)
        draw.text(
            (WIDTH - w / 2 - 59 - 1, FONTHEIGHT - 10 - 1),
            text=text_green_token,
            fill=(0, 0, 0, 128),
            font=FONT,
        )
        draw.text(
            (WIDTH - w / 2 - 59, FONTHEIGHT - 10),
            text=text_green_token,
            fill="white",
            font=FONT,
        )


def add_left_items(card: Image.Image, draw: ImageDraw.ImageDraw):
    ressource_dict = {
        "Courage": "arm",
        "Courage +": "arm-plus",
        "Botte": "boot",
        "Botte +": "boot-plus",
        "Compétence": "skill",
    }

    ressource_1 = st.sidebar.checkbox("Ressource 1", value=False)
    if ressource_1:
        first_ressource = st.sidebar.selectbox(
            "Ressource 1", ("Compétence", "Courage", "Botte")
        )
        first_rsrc = Image.open(
            f"docs/images/n1-{ressource_dict.get(first_ressource)}.png"
        )

        if first_ressource == "Compétence":
            value_skill = st.sidebar.select_slider(
                "Points de compétence", options=["0+", 1, 2, 3, 4], value=1
            )

            if value_skill == "0+":
                first_rsrc = Image.open(
                    f"docs/images/n1-{ressource_dict.get(first_ressource)}-plus.png"
                )
                value_skill = 0

    ressource_2 = st.sidebar.checkbox("Ressource 2", value=False)
    if ressource_2:
        second_ressource = st.sidebar.selectbox(
            "Ressource 2", ("Courage", "Courage +", "Botte")
        )
        scd_rsrc = Image.open(
            f"docs/images/n2-{ressource_dict.get(second_ressource)}.png"
        )

        card.paste(scd_rsrc, (0, 0), scd_rsrc)

    ressource_3 = st.sidebar.checkbox("Ressource 3", value=False)
    if ressource_3:
        third_ressource = st.sidebar.selectbox(
            "Ressource 3", ("Courage", "Botte", "Botte +")
        )
        third_rsrc = Image.open(
            f"docs/images/n3-{ressource_dict.get(third_ressource)}.png"
        )

        card.paste(third_rsrc, (0, 0), third_rsrc)

    if ressource_1:
        card.paste(first_rsrc, (0, 0), first_rsrc)

        if first_ressource == "Compétence":
            text_skill = str(value_skill)

            w, _ = draw.textsize(text_skill, font=FONT_skill)
            draw.text(
                (72 - w / 2, FONTHEIGHT_skill + 90),
                text=text_skill,
                fill=(0, 0, 0, 255),
                font=FONT_skill,
            )


def add_cost(card: Image.Image, draw: ImageDraw.ImageDraw):
    cost = st.sidebar.checkbox("Ajouter un coût", value=False)
    if cost:
        cost_logo = Image.open("docs/images/cost-corner.png")
        card.paste(cost_logo, (0, 0), cost_logo)

        cost_value = st.sidebar.slider("Coût", min_value=1, max_value=8, value=1)

        text_cost = str(cost_value)

        w, _ = draw.textsize(text_cost, font=FONT)
        draw.text(
            (WIDTH - w / 2 - 53 - 1, LENGTH - FONTHEIGHT - 25),
            text=text_cost,
            fill=(0, 0, 0, 128),
            font=FONT,
        )
        draw.text(
            (WIDTH - w / 2 - 53, LENGTH - FONTHEIGHT - 25),
            text=text_cost,
            fill="white",
            font=FONT,
        )


def add_text(card: Image.Image, draw: ImageDraw.ImageDraw):
    text = st.sidebar.text_input("Texte principal de la carte", value="Votre texte ICI")
    lines = textwrap.wrap(text, width=40)
    w, h = draw.textsize(lines, font=FONT_subtitle)
    y_text = h
    draw.text(((WIDTH - w) / 2, 700 - h), text=lines, fill="black", font=FONT_subtitle)


def make_card(illustration):
    card = BASECARD.copy()
    draw = ImageDraw.Draw(card)

    if illustration is None:
        illustration = Image.open("docs/images/basic_illustration.PNG")
    else:
        illustration = Image.open(illustration)

    add_illustration(card, illustration)
    add_bandeau(card)
    add_card_name(draw)
    add_person_corner(card)
    add_green_token(card, draw)
    add_card_type(card, draw)
    add_cost(card, draw)

    add_left_items(card, draw)

    add_text(card, draw)

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
