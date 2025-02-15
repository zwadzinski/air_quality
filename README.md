# Air Quality Monitoring System

This project is an air quality monitoring system running on a Raspberry Pi. It reads sensor data from two devices:

- **PMSA003 Sensor**: Measures particulate matter (PM) concentrations (e.g., PM2.5, PM10, etc.) using hardware I2C.
- **SGP40 Sensor**: Measures VOC (volatile organic compounds) levels using software I2C (BitBangI2C).

The system is built using **FastAPI** to handle sensor data aggregation and **Streamlit** to display the data in a web dashboard.

---

## How It Works

1. **FastAPI Server (`fastapi_server.py`):**
   - The server defines a `/data` endpoint.
   - It calls two functions from `sensors.py`:
     - `read_pmsa003_i2c()`: Reads air quality data from the PMSA003 sensor.
     - `read_sgp40_i2c()`: Retrieves the VOC measurement from the SGP40 sensor (which internally calls `read_sgp40_sw()`).
   - Results from both sensors are combined into a JSON response with keys `pmsa0031` and `sgp40`.

2. **Sensor Code (`sensors.py`):**
   - **PMSA003 Sensor:**
     - Uses the hardware I2C interface from the `busio` module and the `adafruit_pm25` library.
   - **SGP40 Sensor:**
     - Uses a software I2C bus created with `adafruit_bitbangio`.
     - The `read_sgp40_sw()` function reads raw VOC values using the `adafruit_sgp40` library.
     - The `read_sgp40_i2c()` function wraps the raw VOC value in a dictionary before it is sent to the API.
     
3. **Streamlit Apps:**
   - **Local Version (`streamlit_app.py`):**
     - Continuously polls the FastAPI endpoint to display live sensor readings.
   - **Cloud Version (`cloud/streamlit_app.py`):**
     - Uses a public ngrok endpoint to access the API.
     - Additionally, it leverages helper functions (e.g., `interpret_air_quality()` and `display_particle_counts()`) to format the PMSA003 sensor data.

---

## Setup and Deployment

1. **SSH into the Raspberry Pi:**  
   ```
   ssh airquality@airquality.local
   (Password: wifi hint)
   ```

2. **Activate the Virtual Environment:**  
   ```
   source venv/bin/activate
   ```

3. **Running the FastAPI Server:**  
   On the Raspberry Pi, start the FastAPI server using uvicorn:
   ```
   uvicorn fastapi_server:app --host 0.0.0.0 --port=8000 --reload
   ```

4. **Expose the API via ngrok:**  
   On the Raspberry Pi, run:
   ```
   ngrok http --hostname=whale-pro-marmot.ngrok-free.app 8000
   ```

5. **Running the Streamlit App:**  
   From a local machine or cloud server, launch the app:
   - Local version:
     ```
     streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
     ```
   - Cloud version (if using the ngrok endpoint):
     ```
     streamlit run cloud/streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
     ```

---

## Libraries and Tools

- **FastAPI**: Fast, asynchronous web framework for building APIs.
- **Uvicorn**: ASGI server used to run the FastAPI application.
- **Streamlit**: Framework for creating interactive dashboards and web apps.
- **adafruit_pm25**: Library to interface with the PMSA003 air quality sensor.
- **adafruit_sgp40**: Library to interface with the SGP40 VOC sensor.
- **busio**: For hardware I2C communication.
- **bitbangio**: For creating a software I2C bus when hardware I2C is not available or for alternate configurations.
- **ngrok**: Tool for exposing local servers to the public internet.

---

## Notes

- Ensure your sensors are connected to the correct GPIO pins on your Raspberry Pi.
- After making changes to the code (especially in `sensors.py`), restart the FastAPI server so that updates are applied.
- The Streamlit apps continuously query the API endpoint, so modify the refresh interval (currently 5 seconds) as necessary for your setup.

Happy Monitoring! 