import requests
import streamlit as st
from functions import interpret_air_quality, display_particle_counts

# Use your custom ngrok endpoint
api_url = "https://whale-pro-marmot.ngrok-free.app/data"

try:
    response = requests.get(api_url)
    response.raise_for_status()
    sensor_data = response.json()
    st.header("Air Quality Reading")
    
    # Extract the PMSA0031 sensor data from the nested dictionary:
    pmsa_data = sensor_data.get("pmsa0031", {})
    
    # Now pass only the PMSA0031 data to your functions.
    st.write(interpret_air_quality(pmsa_data))
    st.subheader("Other Measurements")
    st.text(display_particle_counts(pmsa_data))
    
    # Optionally, display the VOC reading from the sgp40 sensor.
    st.subheader("SGP40 VOC Reading")
    sgp40_data = sensor_data.get("sgp40", {})
    st.write(f"VOC: {sgp40_data.get('voc', 'N/A')}")
    
    st.button("Refresh")
except Exception as e:
    st.error(f"Error fetching data: {e}")