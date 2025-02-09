import streamlit as streamlit
import time
import adafruit_sgp40
import board
import busio


# Function to read from the SGP40 VOC sensor
def read_sgp40():
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        sgp40 = adafruit_sgp40.SGP40(i2c)
        
        # Let sensor warm up or perform a measurement slightly delayed
        time.sleep(0.1)  
        # Measure raw value. Depending on your sensor's calibration, you might use another method
        voc_raw = sgp40.measure_raw()
        return voc_raw
    except Exception as e:
        return f"Error reading SGP40: {e}"


# Function to read from the PMSA003 particulate matter sensor
# Using the pms5003 library which is compatible with many PMS sensors

def read_pmsa003():
    try:
        # Initialize UART interface. Adjust TX/RX pins as necessary for your wiring.
        uart = busio.UART(board.TX, board.RX, baudrate=9600)
        from pms5003 import PMS5003
        pms_sensor = PMS5003(uart, pin_reset=None, pin_sleep=None)
        
        # Read sensor data, which typically includes pm_ug/m3 values for several particle sizes
        data = pms_sensor.read()
        return data
    except Exception as e:
        return f"Error reading PMSA003: {e}"


# Main Streamlit app
streamlit.title("Air Quality Monitor")
streamlit.write("Monitoring data from PMSA003 and SGP40 sensors")

# Optionally add an auto-refresh component here if desired
if streamlit.button("Refresh Sensor Readings"):
    with streamlit.spinner('Reading sensors...'):
        pmsa_reading = read_pmsa003()
        sgp40_reading = read_sgp40()
        time.sleep(0.5)  # simulate processing delay
    
    streamlit.subheader("PMSA003 Sensor Data")
    streamlit.json(pmsa_reading)  

    streamlit.subheader("SGP40 Sensor Data (VOC Index)")
    streamlit.write(sgp40_reading)

# You can add additional auto-refresh using st.experimental_rerun or a custom component if needed

streamlit.write("_Note: Ensure the sensors are connected properly and the required libraries are installed (pip install pms5003 adafruit-circuitpython-sgp40 streamlit)._") 