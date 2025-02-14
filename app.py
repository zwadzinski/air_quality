#import streamlit as streamlit
import time
import adafruit_sgp40
import board
import busio
from adafruit_pm25.i2c import PM25_I2C

#rpi login:
# username: airquality
# password: pumpkins
# venv: source venv/bin/activate


# Function to read from the PMSA003 particulate matter sensor
# Using the pms5003 library which is compatible with many PMS sensors

def read_pmsa003_i2c():
    """
    Reads data from the PM2.5 sensor over I2C.
    Returns a dictionary of sensor readings or an error string.
    """
    try:
        # Initialize I2C interface at 100KHz (recommended by Adafruit)
        i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
        reset_pin = None  # Change this if you've connected a GPIO to the RESET pin
        pm25 = PM25_I2C(i2c, reset_pin)
        
        # The sensor returns a dictionary with keys like 'pm25 standard', 'pm10 standard', etc.
        aqdata = pm25.read()
        return aqdata
    except Exception as e:
        return f"Error reading PMSA003: {e}"

def interpret_air_quality(aqdata):
    """
    Interprets the air quality based on the PM2.5 concentration (in µg/m³).
    Uses general EPA breakpoints to provide a human-friendly quality rating.
    """
    pm25 = aqdata.get("pm25 standard", None)
    if pm25 is None:
        return "PM2.5 data not available."

    # EPA PM2.5 Breakpoints (µg/m³)
    # Good: 0.0 - 12.0
    # Moderate: 12.1 - 35.4
    # Unhealthy for Sensitive Groups: 35.5 - 55.4
    # Unhealthy: 55.5 - 150.4
    # Very Unhealthy: 150.5 - 250.4
    # Hazardous: > 250.4
    if pm25 <= 12.0:
        quality = "Good"
    elif pm25 <= 35.4:
        quality = "Moderate"
    elif pm25 <= 55.4:
        quality = "Unhealthy for Sensitive Groups"
    elif pm25 <= 150.4:
        quality = "Unhealthy"
    elif pm25 <= 250.4:
        quality = "Very Unhealthy"
    else:
        quality = "Hazardous"

    return f"PM2.5: {pm25} µg/m³  -->  Air Quality is {quality}."

def display_particle_counts(aqdata):
    """
    Returns a formatted string showing the number of particles at various sizes.
    """
    parts = []
    keys = [
        "particles 03um",
        "particles 05um",
        "particles 10um",
        "particles 25um",
        "particles 50um",
        "particles 100um"
    ]
    for key in keys:
        value = aqdata.get(key, "N/A")
        parts.append(f"{key}: {value}")
    return "\n".join(parts)

def main():
    print("Starting Air Quality Monitor...\n")
    while True:
        aqdata = read_pmsa003_i2c()
        if isinstance(aqdata, dict):
            print("===================================")
            print("Air Quality Reading:")
            # Output a summary message based on PM2.5
            print(interpret_air_quality(aqdata))
            print("\nOther Measurements:")
            # Output additional particle counts
            print(display_particle_counts(aqdata))
            print("===================================\n")
        else:
            # If there was an error reading the sensor, display it.
            print(aqdata)
        # Wait for 5 seconds before taking another reading.
        time.sleep(5)

if __name__ == "__main__":
    main()

# Main Streamlit app
# streamlit.title("Air Quality Monitor")
# streamlit.write("Monitoring data from PMSA003 and SGP40 sensors")

# Optionally add an auto-refresh component here if desired

# if streamlit.button("Refresh Sensor Readings"):
#     with streamlit.spinner('Reading sensors...'):
#         pmsa_reading = read_pmsa003()
#         sgp40_reading = read_sgp40()
#         time.sleep(0.5)  # simulate processing delay
    
#     streamlit.subheader("PMSA003 Sensor Data")
#     streamlit.json(pmsa_reading)  

#     streamlit.subheader("SGP40 Sensor Data (VOC Index)")
#     streamlit.write(sgp40_reading)

# # You can add additional auto-refresh using st.experimental_rerun or a custom component if needed

# streamlit.write("_Note: Ensure the sensors are connected properly and the required libraries are installed (pip install pms5003 adafruit-circuitpython-sgp40 streamlit)._") 