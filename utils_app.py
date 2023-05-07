import streamlit as st
from PIL import Image, ImageFont, ImageDraw

BASECARD = Image.open("docs/images/basic-template.png")

WIDTH, HEIGHT = BASECARD.size
# mermaid_font = ImageFont.truetype("docs/font/Mermaid1001.ttf", 45)
ravise_34_font = ImageFont.truetype("docs/font/Ravise-Regular.ttf", 34)
ravise_45_font = ImageFont.truetype("docs/font/Ravise-Regular.ttf", 45)
ravise_50_font = ImageFont.truetype("docs/font/Ravise-Regular.ttf", 50)
bogart_font = ImageFont.truetype("docs/font/Bogart-Regular-trial.ttf", 26)
libertine_font_36 = ImageFont.truetype(
    "docs/font/LinuxLibertine/LinLibertine_RB.ttf", 36
)
libertine_font_28 = ImageFont.truetype(
    "docs/font/LinuxLibertine/LinLibertine_RI.ttf", 28
)
offset = 80

FONT_CARD_NAME = ravise_45_font
FONT_SKILL = ravise_50_font
FONT_TOKEN = ravise_45_font
FONT_CARD_TYPE = bogart_font
FONT_CARD_TEXT = ravise_34_font
FONT_CARD_LEGEND = libertine_font_28


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
    w, _ = draw.textsize(text, font=FONT_CARD_NAME)
    draw.text(
        ((WIDTH - w) / 2 - 1, 45 - 1),
        text=text,
        fill="black",
        font=FONT_CARD_NAME,
    )
    draw.text(((WIDTH - w) / 2, 45), text=text, fill="white", font=FONT_CARD_NAME)


def add_card_type(card: Image.Image, draw: ImageDraw.ImageDraw):
    card_type = st.sidebar.checkbox("Sous-titre du bandeau", value=False)
    if card_type:
        subtitle = Image.open("docs/images/sous-titre.png")
        card.paste(subtitle, (0, 0), subtitle)
        text = st.sidebar.text_input("Texte sous-titre", value="Compagnon")
        w, _ = draw.textsize(text, font=FONT_CARD_TYPE)
        draw.text(((WIDTH - w) / 2, 94), text=text, fill="white", font=FONT_CARD_TYPE)


def add_green_token(card: Image.Image, draw: ImageDraw.ImageDraw):
    green_token = st.sidebar.checkbox("Jeton vert", value=False)
    if green_token:
        green_logo = Image.open("docs/images/jeton_vert.png")
        card.paste(green_logo, (0, 0), green_logo)

        value_green_token = st.sidebar.select_slider(
            "Valeur du jeton vert", options=[1, 2, 3, 4, 5, 6, 7, 8, "?"], value=1
        )

        text_green_token = str(value_green_token)

        w, h = draw.textsize(text_green_token, font=FONT_TOKEN)
        draw.text(
            (WIDTH - w / 2 - 59 - 1, h - 1),
            text=text_green_token,
            fill=(0, 0, 0, 128),
            font=FONT_TOKEN,
        )
        draw.text(
            (WIDTH - w / 2 - 59, h),
            text=text_green_token,
            fill="white",
            font=FONT_TOKEN,
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

            w, h = draw.textsize(text_skill, font=FONT_SKILL)
            draw.text(
                (72 - w / 2, h / 2 + 120),
                text=text_skill,
                fill=(0, 0, 0, 255),
                font=FONT_SKILL,
            )


def add_cost(card: Image.Image, draw: ImageDraw.ImageDraw):
    cost = st.sidebar.checkbox("Ajouter un coût", value=False)
    if cost:
        cost_logo = Image.open("docs/images/cost-corner.png")
        card.paste(cost_logo, (0, 0), cost_logo)

        cost_value = st.sidebar.slider("Coût", min_value=1, max_value=8, value=1)

        text_cost = str(cost_value)

        w, h = draw.textsize(text_cost, font=FONT_TOKEN)
        draw.text(
            (WIDTH - w / 2 - 52 - 1, HEIGHT - h / 2 - 55),
            text=text_cost,
            fill=(0, 0, 0, 128),
            font=FONT_TOKEN,
        )
        draw.text(
            (WIDTH - w / 2 - 52, HEIGHT - h / 2 - 55),
            text=text_cost,
            fill="white",
            font=FONT_TOKEN,
        )


def add_text(draw: ImageDraw.ImageDraw):
    text = st.sidebar.text_area("Texte principal de la carte", value="Votre texte ICI")
    # lines = textwrap.wrap(text, width=40)
    w, h = draw.textsize(text, font=FONT_CARD_TEXT)
    draw.text(
        ((WIDTH - w) / 2, 680 - h / 2),
        text=text,
        align="center",
        fill="black",
        font=FONT_CARD_TEXT,
        spacing=12,
    )


def add_subtitle(draw: ImageDraw.ImageDraw):
    text = st.sidebar.text_area("Texte secondaire de la carte")
    w, h = draw.textsize(text, font=FONT_CARD_LEGEND)
    draw.text(
        (55, HEIGHT - h - 60),
        text=text,
        # align="center",
        # anchor="rm",
        fill="black",
        font=FONT_CARD_LEGEND,
    )


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

    add_text(draw)
    add_subtitle(draw)

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
