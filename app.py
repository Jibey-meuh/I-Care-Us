import streamlit as st
import requests
import folium

from streamlit_folium import st_folium

st.set_page_config(
    page_title="I-Care-Us",
    page_icon="🛟",
    layout="wide"
)

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

st.title("🛟 I-Care-Us")
st.caption(
    "Travel safer. Anywhere."
)

# --------------------------------------------------
# SESSION
# --------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("Recherche")

    location = st.text_input(
        "Ville, pays ou coordonnées GPS"
    )

    st.subheader("Afficher")

    hospitals = st.checkbox("🏥 Hôpitaux", value=True)
    police = st.checkbox("🚓 Police", value=True)
    pharmacies = st.checkbox("💊 Pharmacies")
    supermarkets = st.checkbox("🛒 Supermarchés")
    accommodation = st.checkbox("🏠 Hébergements")
    embassy = st.checkbox("🇫🇷 Ambassade / Consulat")
    travel_advice = st.checkbox("⚠ Conseils voyageurs")

    search_btn = st.button(
        "Rechercher",
        use_container_width=True
    )

# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def geocode(query):

    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "I-Care-Us"
    }

    response = requests.get(
        NOMINATIM_URL,
        params=params,
        headers=headers,
        timeout=20
    )

    data = response.json()

    if not data:
        return None

    return {
        "lat": float(data[0]["lat"]),
        "lon": float(data[0]["lon"]),
        "display_name": data[0]["display_name"]
    }


def create_map(lat, lon):

    fmap = folium.Map(
        location=[lat, lon],
        zoom_start=13
    )

    folium.Marker(
        [lat, lon],
        tooltip="Position recherchée",
        icon=folium.Icon(color="red")
    ).add_to(fmap)

    return fmap

# --------------------------------------------------
# MAIN
# --------------------------------------------------

col1, col2 = st.columns([2, 1])

with col1:

    if search_btn and location:

        with st.spinner("Recherche en cours..."):

            result = geocode(location)

        if result:

            lat = result["lat"]
            lon = result["lon"]

            st.success(result["display_name"])

            if result["display_name"] not in st.session_state.history:
                st.session_state.history.insert(
                    0,
                    result["display_name"]
                )

            fmap = create_map(lat, lon)

            st_folium(
                fmap,
                width=None,
                height=650
            )

        else:
            st.error("Lieu introuvable.")

    else:

        default_map = folium.Map(
            location=[48.8566, 2.3522],
            zoom_start=5
        )

        st_folium(
            default_map,
            width=None,
            height=650
        )

with col2:

    st.subheader("Résumé")

    if search_btn and location:

        st.info(
            """
            Résumé IA bientôt disponible.

            Version future :
            - Analyse sécurité
            - Conseils voyageurs
            - Alertes locales
            - Ambassade française
            - Services d'urgence
            """
        )

    st.subheader("Historique")

    if st.session_state.history:

        for item in st.session_state.history[:10]:
            st.write("•", item)

    else:
        st.write("Aucune recherche")

    st.subheader("Modules activés")

    modules = []

    if hospitals:
        modules.append("🏥 Hôpitaux")

    if police:
        modules.append("🚓 Police")

    if pharmacies:
        modules.append("💊 Pharmacies")

    if supermarkets:
        modules.append("🛒 Supermarchés")

    if accommodation:
        modules.append("🏠 Hébergements")

    if embassy:
        modules.append("🇫🇷 Ambassade")

    if travel_advice:
        modules.append("⚠ Conseils voyageurs")

    for module in modules:
        st.write(module)

st.divider()

st.caption(
    "I-Care-Us • Open-source Travel Emergency Assistant"
)
