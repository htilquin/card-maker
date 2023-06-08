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
card_spec.card_name = st.sidebar.text_input("Nom de la  carte", value="Carte")
card_spec.card_subtitle = st.sidebar.checkbox("Catégorie de la carte", value=False)
card_spec.subtitle_text = (
    "/"
    if not card_spec.card_subtitle
    else st.sidebar.text_input("Texte sous-titre", value="Compagnon")
)

card_spec.force = st.sidebar.checkbox("Force du monstre", value=False)
if card_spec.force:
    card_spec.force_level = st.sidebar.slider(
        "Force", min_value=1, max_value=4, value=1
    )

else:
    card_spec.person_corner = st.sidebar.checkbox("Coin 'personnage'", value=False)
    card_spec.points_victoire = st.sidebar.checkbox("Points de victoire", value=False)
    if card_spec.points_victoire:
        card_spec.value_pts_victoire = st.sidebar.select_slider(
            "Nombre de points de victoire",
            options=[1, 2, 3, 4, 5, 6, 7, 8, "?"],
            value=1,
        )
    card_spec.cost = st.sidebar.checkbox("Ajouter un coût", value=False)
    if card_spec.cost:
        card_spec.cost_value = st.sidebar.slider(
            "Coût", min_value=1, max_value=8, value=1
        )

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

card_spec.appear = st.sidebar.checkbox("Apparition", value=False)
if card_spec.appear:
    card_spec.text_appear = st.sidebar.text_area("Texte apparition")
else:
    card_spec.danger = st.sidebar.checkbox("Danger", value=False)
    if card_spec.danger:
        card_spec.text_danger = st.sidebar.text_area("Texte danger")
    card_spec.horde = st.sidebar.checkbox("Horde", value=False)

card_spec.main_text = st.sidebar.text_area(
    "Texte principal de la carte", value="Votre texte ICI"
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

        new_x, new_y = get_resized_dimensions(
            card_spec.illustration_path, card_spec.size
        )
        if card_spec.size > 100:
            card_spec.horizon = st.slider(
                "Déplacer photo horizontalement",
                min_value=0,
                max_value=max(new_x - WIDTH + offset, 1),
                value=0,
            )
        if new_y > int(0.69 * HEIGHT) - offset:
            card_spec.vertical = st.slider(
                "Déplacer photo verticalement",
                min_value=0,
                max_value=max(new_y - int(0.69 * HEIGHT) + offset, 1),
                value=0,
            )

    card = make_card(card_spec)
    st.image(card)
    buf = BytesIO()
    card.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(label="Télécharger la carte", data=byte_im, file_name="card.png")


with tab2:
    dict_of_spec = card_spec.to_dict()
    st.write(dict_of_spec)
    st.download_button("Download the specs", str(dict_of_spec))

with tab3:
    uploaded_spec = st.file_uploader(
        "Sélectionner le fichier contenant les specs (liste de dictionnaires)",
        type=["txt"],
    )

    if uploaded_spec:
        the_specs = json.loads(uploaded_spec.read())

        # for specs in the_specs["cards"]:
        #     card_from_spec = Card()
        #     card_from_spec.from_dict(specs)
        #     card_done = make_card(card_from_spec)
        #     st.image(card_done)

        with BytesIO() as buffer:
            with zipfile.ZipFile(buffer, "w") as zip:
                # for specs in the_specs["cards"]:
                for specs in the_specs:
                    card_from_spec = Card()
                    card_from_spec.from_dict(specs)
                    card_done = make_card(card_from_spec)
                    buf = BytesIO()
                    card_done.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    # st.image(card_done)
                    zip.writestr(f"{card_from_spec.card_name}.png", byte_im)

            buffer.seek(0)

            btn = st.download_button(
                label="Download ZIP", data=buffer, file_name="file.zip"
            )
