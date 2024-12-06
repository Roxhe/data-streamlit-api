import streamlit as st
import requests
from datetime import datetime

st.title("Estimer votre trajet de Taxi")

pickup_date = st.date_input("Date de prise en charge")
pickup_time = st.time_input("Heure de prise en charge")
pickup_datetime = datetime.combine(pickup_date, pickup_time).strftime("%Y-%m-%d %H:%M:%S")
st.markdown("_Exemple : 2014-07-06 19:18:00_")

pickup_longitude = st.number_input(
    "Longitude de prise en charge *",
    format="%.6f",
    key="pickup_longitude"
)
st.markdown("_Exemple : -73.950655_")


pickup_latitude = st.number_input(
    "Latitude de prise en charge *",
    format="%.6f",
    key="pickup_latitude"
)
st.markdown("_Exemple : 40.783282_")


dropoff_longitude = st.number_input(
    "Longitude de dépose *",
    format="%.6f",
    key="dropoff_longitude"
)
st.markdown("_Exemple : -73.984365_")


dropoff_latitude = st.number_input(
    "Latitude de dépose *",
    format="%.6f",
    key="dropoff_latitude"
)
st.markdown("_Exemple : 40.769802_")


passenger_count = st.number_input(
    "Nombre de passagers *",
    min_value=1,
    max_value=10,
    step=1,
    key="passenger_count"
)
st.markdown("_Exemple : 2_")


if st.button("Estimer votre trajet"):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    if not all(params.values()):
        st.error("Tous les champs marqués d'une * doivent être remplis.")
    else:
        url = 'https://taxifare.lewagon.ai/predict'
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                fare = response.json().get("fare")
                if fare is not None:
                    st.write(f"Votre trajet en taxi devrait coûter : {fare:.2f} $")
                    st.markdown("_Si vous avez utilisé les données d'exemples, le résultat devrait être de 14.71 $ ;)._")

                else:
                    st.error("Veuillez réesayer")
            else:
                st.error(f"Code erreur: {response.status_code}")
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")
