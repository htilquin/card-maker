import streamlit as st
from PIL import Image, ImageFont, ImageDraw

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

# BASECARD = Image.open("docs/images/basic-template.png")
# WIDTH, HEIGHT = BASECARD.size

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
libertine_font_24 = ImageFont.truetype(
    "docs/font/LinuxLibertine/LinLibertine_RB.ttf", 24
)
offset = 80

FONT_CARD_NAME = ravise_45_font
FONT_SKILL = ravise_50_font
FONT_TOKEN = ravise_45_font
FONT_CARD_TYPE = bogart_font
FONT_CARD_TEXT = ravise_34_font
FONT_CARD_LEGEND = libertine_font_28
FONT_CARD_APPEAR = libertine_font_24

ressource_dict = {
    "Courage": "arm",
    "Courage +": "arm-plus",
    "Botte": "boot",
    "Botte +": "boot-plus",
    "Compétence": "skill",
}

symbol_pics = {
    "PO - grand": "coin-big",
    "PO - petit": "coin-mini",
    "Botte - grand": "boot-big",
    "Botte - grand x2": "boot-big-2",
    "Botte - petit": "boot-mini",
    "Competence - grand": "comp-big",
    "Competence - petit": "comp-mini",
    "Coeur - grand": "heart-big",
    "Coeur - petit": "heart-mini",
    "Bras - petit": "strong-mini",
    "Bras - petit x3": "strong-mini-3",
    "Point Victoire - petit": "vict-big",
}


class Card:
    BASECARD = Image.open("docs/images/basic-template.png")
    WIDTH, HEIGHT = BASECARD.size

    illustration_path = "docs/images/basic_illustration.PNG"
    size = 100
    horizon = 0
    vertical = 0
    bandeau_couleur = "Gris"
    card_name = "Carte"
    card_subtitle = False
    subtitle_text = "Compagnon"
    force = False
    force_level = 0
    person_corner = False
    points_victoire = False
    value_pts_victoire = 0
    cost = False
    cost_value = 0
    acquire = False
    ressource_1 = False
    first_ressource = None
    value_skill = 0
    ressource_2 = False
    second_ressource = None
    ressource_3 = False
    third_ressource = None
    use_first_symbol = False
    first_symbol = None
    first_symbol_position = (0, 0)
    first_symbol_text = None
    use_second_symbol = False
    second_symbol = None
    second_symbol_position = (0, 0)
    second_symbol_text = None
    use_third_symbol = False
    third_symbol = None
    third_symbol_position = (0, 0)
    third_symbol_text = None
    appear = False
    text_appear = ""
    danger = False
    text_danger = ""
    horde = False
    main_text = ""
    subtext = ""

    def to_dict(self):
        return {
            "illustration_path": self.illustration_path,
            "size": self.size,
            "horizon": self.horizon,
            "vertical": self.vertical,
            "bandeau_couleur": self.bandeau_couleur,
            "card_name": self.card_name,
            "card_subtitle": self.card_subtitle,
            "subtitle_text": self.subtitle_text,
            "force": self.force,
            "force_level": self.force_level,
            "person_corner": self.person_corner,
            "points_victoire": self.points_victoire,
            "value_pts_victoire": self.value_pts_victoire,
            "cost": self.cost,
            "cost_value": self.cost_value,
            "acquire": self.acquire,
            "ressource_1": self.ressource_1,
            "first_ressource": self.first_ressource,
            "value_skill": self.value_skill,
            "ressource_2": self.ressource_2,
            "second_ressource": self.second_ressource,
            "ressource_3": self.ressource_3,
            "third_ressource": self.third_ressource,
            "use_first_symbol": self.use_first_symbol,
            "first_symbol": self.first_symbol,
            "first_symbol_position": self.first_symbol_position,
            "first_symbol_text": self.first_symbol_text,
            "use_second_symbol": self.use_second_symbol,
            "second_symbol": self.second_symbol,
            "second_symbol_position": self.second_symbol_position,
            "second_symbol_text": self.second_symbol_text,
            "use_third_symbol": self.use_third_symbol,
            "third_symbol": self.third_symbol,
            "third_symbol_position": self.third_symbol_position,
            "third_symbol_text": self.third_symbol_text,
            "appear": self.appear,
            "text_appear": self.text_appear,
            "danger": self.danger,
            "text_danger": self.text_danger,
            "horde": self.horde,
            "main_text": self.main_text,
            "subtext": self.subtext,
        }

    def from_dict(self, data):
        self.illustration_path = data.get("illustration_path")
        self.size = data.get("size")
        self.horizon = data.get("horizon")
        self.vertical = data.get("vertical")
        self.bandeau_couleur = data.get("bandeau_couleur")
        self.card_name = data.get("card_name")
        self.card_subtitle = data.get("card_subtitle")
        self.subtitle_text = data.get("subtitle_text")
        self.force = data.get("force")
        self.force_level = data.get("force_level")
        self.person_corner = data.get("person_corner")
        self.points_victoire = data.get("points_victoire")
        self.value_pts_victoire = data.get("value_pts_victoire")
        self.cost = data.get("cost")
        self.cost_value = data.get("cost_value")
        self.acquire = data.get("acquire")
        self.ressource_1 = data.get("ressource_1")
        self.first_ressource = data.get("first_ressource")
        self.value_skill = data.get("value_skill")
        self.ressource_2 = data.get("ressource_2")
        self.second_ressource = data.get("second_ressource")
        self.ressource_3 = data.get("ressource_3")
        self.third_ressource = data.get("third_ressource")
        self.use_first_symbol = data.get("use_first_symbol")
        self.first_symbol = data.get("first_symbol")
        self.first_symbol_position = data.get("first_symbol_position")
        self.first_symbol_text = data.get("first_symbol_text")
        self.use_second_symbol = data.get("use_second_symbol")
        self.second_symbol = data.get("second_symbol")
        self.second_symbol_position = data.get("second_symbol_position")
        self.second_symbol_text = data.get("second_symbol_text")
        self.use_third_symbol = data.get("use_third_symbol")
        self.third_symbol = data.get("third_symbol")
        self.third_symbol_position = data.get("third_symbol_position")
        self.third_symbol_text = data.get("third_symbol_text")
        self.appear = data.get("appear")
        self.text_appear = data.get("text_appear")
        self.danger = data.get("danger")
        self.text_danger = data.get("text_danger")
        self.horde = data.get("horde")
        self.main_text = data.get("main_text")
        self.subtext = data.get("subtext")


def get_resized_dimensions(card_spec):
    illustration = Image.open(card_spec.illustration_path)
    x, y = illustration.size
    ratio = y / x

    new_x = int((card_spec.WIDTH - offset) / 100 * card_spec.size)
    new_y = int((card_spec.WIDTH - offset) / 100 * ratio * card_spec.size)

    return new_x, new_y


def resize_illustration(card_spec):
    illustration = Image.open(card_spec.illustration_path)
    size = card_spec.size
    x, y = illustration.size
    ratio = y / x

    resized_illustration = illustration.resize(
        (
            int((card_spec.WIDTH - offset) / 100 * size),
            int((card_spec.WIDTH - offset) / 100 * ratio * size),
        ),
        Image.LANCZOS,
    )
    return resized_illustration


def make_card(card_spec: Card):
    if card_spec.acquire:
        card_spec.BASECARD = Image.open("docs/images/acquire.png")

    card = card_spec.BASECARD.copy()
    draw = ImageDraw.Draw(card)

    resized_illustration = resize_illustration(card_spec)
    horizon = card_spec.horizon
    vertical = card_spec.vertical
    card.paste(resized_illustration, (-horizon + offset // 2, -vertical + offset // 2))
    card.paste(card_spec.BASECARD, (0, 0), card_spec.BASECARD)

    bandeau = Image.open(f"docs/images/bandeaux/{card_spec.bandeau_couleur}.png")
    card.paste(bandeau, (0, 0), bandeau)

    card_name = card_spec.card_name
    draw.text(
        (card_spec.WIDTH / 2 - 1, 70 - 1),
        text=card_name,
        fill="black",
        font=FONT_CARD_NAME,
        anchor="mm",
    )
    draw.text(
        (card_spec.WIDTH / 2, 70),
        text=card_name,
        fill="white",
        font=FONT_CARD_NAME,
        anchor="mm",
    )

    if card_spec.card_subtitle:
        subtitle = Image.open("docs/images/sous-titre.png")
        card.paste(subtitle, (0, 0), subtitle)
        subtitle_text = card_spec.subtitle_text
        draw.text(
            (card_spec.WIDTH / 2, 114),
            text=subtitle_text,
            fill="white",
            font=FONT_CARD_TYPE,
            anchor="mm",
        )

    if card_spec.force:
        force_logo = Image.open(f"docs/images/force-{card_spec.force_level}.png")
        card.paste(force_logo, (0, 0), force_logo)
    else:
        if card_spec.person_corner:
            person_logo = Image.open("docs/images/person-corner.png")
            card.paste(person_logo, (0, 0), person_logo)

        if card_spec.points_victoire:
            green_logo = Image.open("docs/images/jeton_vert.png")
            card.paste(green_logo, (0, 0), green_logo)
            text_green_token = str(card_spec.value_pts_victoire)
            draw.text(
                (card_spec.WIDTH - 58 - 1, 58 - 1),
                text=text_green_token,
                fill=(0, 0, 0, 128),
                font=FONT_TOKEN,
                anchor="mm",
            )
            draw.text(
                (card_spec.WIDTH - 58, 58),
                text=text_green_token,
                fill="white",
                font=FONT_TOKEN,
                anchor="mm",
            )

        if card_spec.cost:
            if not card_spec.acquire:
                cost_logo = Image.open("docs/images/cost-corner.png")
                card.paste(cost_logo, (0, 0), cost_logo)
            text_cost = str(card_spec.cost_value)
            draw.text(
                (card_spec.WIDTH - 50 - 1, card_spec.HEIGHT - 50 - 1),
                text=text_cost,
                fill=(0, 0, 0, 128),
                font=FONT_TOKEN,
                anchor="mm",
            )
            draw.text(
                (card_spec.WIDTH - 50, card_spec.HEIGHT - 50),
                text=text_cost,
                fill="white",
                font=FONT_TOKEN,
                anchor="mm",
            )

        if card_spec.ressource_2:
            scd_rsrc = Image.open(
                f"docs/images/ressources/n2-{ressource_dict.get(card_spec.second_ressource)}.png"
            )
            card.paste(scd_rsrc, (0, 0), scd_rsrc)

        if card_spec.ressource_3:
            third_rsrc = Image.open(
                f"docs/images/ressources/n3-{ressource_dict.get(card_spec.third_ressource)}.png"
            )
            card.paste(third_rsrc, (0, 0), third_rsrc)

        if card_spec.ressource_1:
            first_ressource = card_spec.first_ressource
            first_rsrc = Image.open(
                f"docs/images/ressources/n1-{ressource_dict.get(first_ressource)}.png"
            )
            if card_spec.value_skill == "0+":
                first_rsrc = Image.open(
                    f"docs/images/ressources/n1-{ressource_dict.get(first_ressource)}-plus.png"
                )
                card_spec.value_skill = 0
            card.paste(first_rsrc, (0, 0), first_rsrc)
            if first_ressource == "Compétence":
                text_skill = str(card_spec.value_skill)
                draw.text(
                    (72, 160),
                    text=text_skill,
                    fill=(0, 0, 0, 255),
                    font=FONT_SKILL,
                    anchor="mm",
                )

    if card_spec.appear:
        appear_image = Image.open("docs/images/apparition.png")
        card.paste(appear_image, (0, 0), appear_image)
        text_appear = card_spec.text_appear
        h = 1
        draw.text(
            (252, 594 - h / 2),
            text=text_appear,
            fill="white",
            font=FONT_CARD_APPEAR,
            spacing=1,
        )
    else:
        if card_spec.danger:
            danger_image = Image.open("docs/images/danger.png")
            card.paste(danger_image, (0, 0), danger_image)
            text_danger = card_spec.text_danger
            h = 1
            draw.text(
                (185, 594 - h / 2),
                text=text_danger,
                fill="white",
                font=FONT_CARD_APPEAR,
                spacing=1,
            )
        if card_spec.horde:
            horde_image = Image.open("docs/images/horde-parents.png")
            card.paste(horde_image, (0, 0), horde_image)

    if card_spec.use_first_symbol:
        first_symb = Image.open(
            f"docs/images/symbols/{symbol_pics.get(card_spec.first_symbol)}.png"
        )
        card.paste(first_symb, card_spec.first_symbol_position, first_symb)
        if card_spec.first_symbol_text is not None:
            text_first_symbol = str(card_spec.first_symbol_text)
            symbol_offset = (card_spec.WIDTH / 2, card_spec.HEIGHT * 0.787 + 17 )
            draw.text(
                tuple(
                    map(
                        lambda i, j: i + j,
                        card_spec.first_symbol_position,
                        symbol_offset,
                    )
                ),
                text=text_first_symbol,
                align="center",
                fill="black",
                font=FONT_CARD_TEXT,
                # spacing=12,
                anchor="mm",
            )

    if card_spec.use_second_symbol:
        scd_symb = Image.open(
            f"docs/images/symbols/{symbol_pics.get(card_spec.second_symbol)}.png"
        )
        card.paste(scd_symb, card_spec.second_symbol_position, scd_symb)

    if card_spec.use_third_symbol:
        third_symb = Image.open(
            f"docs/images/symbols/{symbol_pics.get(card_spec.third_symbol)}.png"
        )
        card.paste(third_symb, card_spec.third_symbol_position, third_symb)

    main_text = card_spec.main_text
    danger_offset = 45 if card_spec.appear or card_spec.danger else 0
    draw.text(
        (card_spec.WIDTH / 2, 680 + danger_offset),
        text=main_text,
        align="center",
        fill="black",
        font=FONT_CARD_TEXT,
        spacing=12,
        anchor="mm"
    )

    subtext = card_spec.subtext
    acquire_offset = 55 if card_spec.acquire else 0
    draw.text(
        (55, card_spec.HEIGHT - 80 - acquire_offset),
        text=subtext,
        # align="center",
        anchor="lm",
        fill="black",
        font=FONT_CARD_LEGEND,
    )

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
