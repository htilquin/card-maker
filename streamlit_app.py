import json
import streamlit as st
from utils_app import *
from io import BytesIO
import zipfile

# st.set_page_config(
#     page_title="Card Maker",
#     page_icon="🃏",
#     layout="centered",
#     initial_sidebar_state="auto",
#     menu_items={
#         "About": """### Card Maker
#     \nTemplate for cards for our family game.
#     \n ---
#     """
#     },
# )

# st.sidebar.markdown("# Options !")
# st.sidebar.markdown("## Image")

st.markdown("## Card Maker !")
st.markdown("Petit outil pour faire des cartes à jouer personnalisées.")

card_spec = Card()

card_spec.bandeau_couleur = st.sidebar.selectbox(
    "Couleur du ruban", ("Gris", "Rouge", "Bleu", "Violet", "Jaune")
).lower()
couleur = card_spec.bandeau_couleur
card_spec.card_name = st.sidebar.text_input("Nom de la  carte", value="Carte")
if not couleur == "gris":
    if couleur in ["rouge", "violet"]:
        card_spec.card_subtitle = True
    else:
        card_spec.card_subtitle = st.sidebar.checkbox(
            "Ajouter une catégorie", value=False
        )
    if card_spec.card_subtitle:
        card_spec.subtitle_text = st.sidebar.text_input(
            "Catégorie de la carte", value="Compagnon"
        )

if couleur == "rouge":
    card_spec.force = True  # que rouge; tous les rouges
    card_spec.force_level = st.sidebar.slider(
        "Force", min_value=1, max_value=4, value=1
    )

if couleur == "bleu" and card_spec.card_subtitle:
    card_spec.person_corner = st.sidebar.checkbox(
        "Coin 'personnage'", value=False
    )  # que bleu

if couleur not in ["rouge", "gris"]:
    card_spec.cost = True  # bleu jaune violet
    card_spec.cost_value = st.sidebar.slider("Coût", min_value=1, max_value=8, value=1)

if couleur in ["bleu", "jaune"]:
    card_spec.points_victoire = st.sidebar.checkbox(
        "Points de victoire", value=False
    )  # bleu ou jaune
    if card_spec.points_victoire:
        card_spec.value_pts_victoire = st.sidebar.select_slider(
            "Nombre de points de victoire",
            options=[1, 2, 3, 4, 5, 6, 7, 8, "?"],
            value=1,
        )


if couleur not in ["rouge", "violet"]:
    card_spec.ressource_1 = st.sidebar.checkbox("Ressource 1", value=False)
    if card_spec.ressource_1:
        card_spec.first_ressource = st.sidebar.selectbox(
            "Ressource 1", ("Compétence", "Courage", "Botte")
        )
        if card_spec.first_ressource == "Compétence":
            card_spec.value_skill = st.sidebar.select_slider(
                "Points de compétence", options=["0+", 1, 2, 3, 4], value=1
            )

        card_spec.ressource_2 = st.sidebar.checkbox("Ressource 2", value=False)
        if card_spec.ressource_2:
            card_spec.second_ressource = st.sidebar.selectbox(
                "Ressource 2", ("Courage", "Courage +", "Botte")
            )

            card_spec.ressource_3 = st.sidebar.checkbox("Ressource 3", value=False)
            if card_spec.ressource_3:
                card_spec.third_ressource = st.sidebar.selectbox(
                    "Ressource 3", ("Courage", "Botte", "Botte +")
                )
else:
    card_spec.appear = st.sidebar.checkbox("Apparition", value=False)  # rouge ou violet
    if card_spec.appear:
        card_spec.text_appear = st.sidebar.text_area("Texte apparition")
    else:
        card_spec.danger = st.sidebar.checkbox("Danger", value=False)  # rouge ou violet
        if card_spec.danger:
            card_spec.text_danger = st.sidebar.text_area("Texte danger")
        card_spec.horde = st.sidebar.checkbox("Horde", value=False)  # rouge bleu violet

if couleur == "bleu":
    ## Acquisition : uniquement bleu
    card_spec.acquire = st.sidebar.checkbox("Acquisition", value=False)
    card_spec.horde = st.sidebar.checkbox("Horde", value=False)

card_spec.main_text = st.sidebar.text_area(
    "Texte principal de la carte", value="Votre texte ICI"
)

symbols_1 = [
    "PO - grand",
    "PO - petit",
    "Botte - grand",
    "Botte - grand x2",
    "Botte - petit",
    "Competence - grand",
    "Competence - petit",
    "Coeur - grand",
    "Coeur - petit",
    "Bras - petit",
    "Bras - petit x3",
    "Point Victoire - petit",
]

symbols_2 = [
    "PO - grand",
    "PO - petit",
    "Botte - petit",
    "Competence - petit",
    "Coeur - grand",
    "Coeur - petit",
    "Bras - petit",
    "Bras - petit x3",
    "Point Victoire - petit",
]

symbols_3 = [
    "PO - petit",
    "Coeur - petit",
    "Bras - petit x3",
]

symbols_text = [
    "PO - grand",
    "PO - petit",
    "Competence - grand",
    "Competence - petit",
    "Point Victoire - petit",
]

if couleur not in ["jaune", "gris"]:
    card_spec.use_first_symbol = st.sidebar.checkbox("Symbole 1", value=False)
    if card_spec.use_first_symbol:
        card_spec.first_symbol = st.sidebar.selectbox("Symbole 1", symbols_1)
        hor_1 = st.sidebar.slider(
            "Décalage position horizontale 1",
            min_value=-card_spec.WIDTH // 2,
            max_value=card_spec.WIDTH // 2,
            value=0,
            label_visibility="collapsed",
        )
        ver_1 = st.sidebar.slider(
            "Décalage position verticale 1",
            min_value=-100,
            max_value=140,
            value=0,
            label_visibility="collapsed",
        )
        card_spec.first_symbol_position = (hor_1, ver_1)
        if card_spec.first_symbol in symbols_text:
            card_spec.first_symbol_text = st.sidebar.select_slider(
                "Texte symbole 1",
                options=[1, 2, 3, 4, 5, 6, 7, 8, "?"],
                value=1,
            )

if couleur in ["violet", "bleu"] and card_spec.use_first_symbol:
    card_spec.use_second_symbol = st.sidebar.checkbox("Symbole 2", value=False)
    if card_spec.use_second_symbol:
        card_spec.second_symbol = st.sidebar.selectbox("Symbole 2", symbols_2)
        hor_2 = st.sidebar.slider(
            "Décalage position horizontale 2",
            min_value=-card_spec.WIDTH // 2,
            max_value=card_spec.WIDTH // 2,
            value=0,
            label_visibility="collapsed",
        )
        ver_2 = st.sidebar.slider(
            "Décalage position verticale 2",
            min_value=-100,
            max_value=140,
            value=0,
            label_visibility="collapsed",
        )
        card_spec.second_symbol_position = (hor_2, ver_2)
        if card_spec.second_symbol in [symbols_text]:
            card_spec.second_symbol_text = st.sidebar.select_slider(
                "Texte symbole 2",
                options=[1, 2, 3, 4, 5, 6, 7, 8, "?"],
                value=1,
            )
if couleur == "bleu" and card_spec.use_second_symbol:
    card_spec.use_third_symbol = st.sidebar.checkbox("Symbole 3", value=False)
    if card_spec.use_third_symbol:
        card_spec.third_symbol = st.sidebar.selectbox("Symbole 3", symbols_3)
        hor_3 = st.sidebar.slider(
            "Décalage position horizontale 3",
            min_value=-card_spec.WIDTH // 2,
            max_value=card_spec.WIDTH // 2,
            value=0,
            label_visibility="collapsed",
        )
        ver_3 = st.sidebar.slider(
            "Décalage position verticale 3",
            min_value=-100,
            max_value=140,
            value=0,
            label_visibility="collapsed",
        )
        card_spec.third_symbol_position = (hor_3, ver_3)
        if card_spec.third_symbol in [symbols_text]:
            card_spec.third_symbol_text = st.sidebar.select_slider(
                "Texte symbole 3",
                options=[1, 2, 3, 4, 5, 6, 7, 8, "?"],
                value=1,
            )

card_spec.subtext = st.sidebar.text_area(
    "Texte secondaire de la carte", value="« Citation facultative »"
)

tab1, tab2, tab3 = st.tabs(["Voir la Carte", "Voir les Specs", "Charger Specs"])

with tab1:
    with st.expander("Modifier la photo"):
        illustration_path = st.file_uploader(
            "Sélectionner l'illustration",
            type=["png", "jpg", "jpeg"],
        )
        if illustration_path:
            card_spec.illustration_path = illustration_path

        card_spec.size = st.slider(
            "Changer la taille de la photo", min_value=100, max_value=300, value=100
        )

        new_x, new_y = get_resized_dimensions(card_spec)
        if card_spec.size > 100:
            card_spec.horizon = st.slider(
                "Déplacer photo horizontalement",
                min_value=0,
                max_value=max(new_x - card_spec.WIDTH + offset, 1),
                value=0,
            )
        if new_y > int(0.69 * card_spec.HEIGHT) - offset:
            card_spec.vertical = st.slider(
                "Déplacer photo verticalement",
                min_value=0,
                max_value=max(new_y - int(0.69 * card_spec.HEIGHT) + offset, 1),
                value=0,
            )

    card = make_card(card_spec)
    st.image(card)
    buf = BytesIO()
    card.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Télécharger la carte",
        data=byte_im,
        file_name=f"{card_spec.card_name}.png",
    )


with tab2:
    dict_of_spec = card_spec.to_dict()
    st.write(dict_of_spec)
    st.download_button(
        "Download the specs", str(dict_of_spec), file_name=f"{card_spec.card_name}.txt"
    )

with tab3:
    uploaded_spec = st.file_uploader(
        "Sélectionner le fichier contenant les specs (liste de dictionnaires)",
        type=["txt"],
    )

    uploaded_pics = st.file_uploader(
        "Sélectionner les photos correspondantes : nom de la photo = illustration_path.",
        accept_multiple_files=True,
    )

    sorted_pics = sorted(uploaded_pics, key=lambda d: d.name)

    if uploaded_spec and uploaded_pics:
        the_specs = json.loads(uploaded_spec.read())
        sorted_specs = sorted(the_specs, key=lambda d: d["illustration_path"])

        with BytesIO() as buffer:
            with zipfile.ZipFile(buffer, "w") as zipfile:
                # for specs in the_specs["cards"]:
                for specs, photo in zip(sorted_specs, sorted_pics):
                    print(specs["illustration_path"], photo.name)
                    card_from_spec = Card()
                    card_from_spec.from_dict(specs)
                    card_done = make_card(card_from_spec)
                    buf = BytesIO()
                    card_done.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    # st.image(card_done)
                    zipfile.writestr(f"{card_from_spec.card_name}.png", byte_im)

            buffer.seek(0)

            btn = st.download_button(
                label="Download ZIP", data=buffer, file_name="file.zip"
            )
