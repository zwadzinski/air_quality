import streamlit as st
import requests
import time

st.title("Continuous Sensor Data")

# Create placeholders for sensor data.
pmsa_placeholder = st.empty()
sgp_placeholder = st.empty()

# Replace with the actual URL of your FastAPI server.
api_url = "http://your-fastapi-server-address:8000/data"

while True:
    try:
        response = requests.get(api_url)
        data = response.json()
        pmsa_data = data.get("pmsa0031")
        sgp40_data = data.get("sgp40")
        
        # Display the sensor readings.
        pmsa_placeholder.markdown(f"**PMSA0031 Sensor Data:**\n```\n{pmsa_data}\n```")
        sgp_placeholder.markdown(f"**SGP40 VOC Readings:**\n```\n{sgp40_data}\n```")
    except Exception as e:
        st.error(f"Error fetching sensor data: {e}")
    
    # Wait before refreshing (adjust the interval as needed).
    time.sleep(5) 