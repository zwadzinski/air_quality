from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import time
import uvicorn
import threading

# Import the sensor function from your sensor module (or app.py if necessary)
from app import read_pmsa003_i2c  

app = FastAPI()

# Global variable for sensor data.
latest_data: Dict[str, Any] = {}

# Pydantic model for incoming sensor data.
class SensorData(BaseModel):
    data: Dict[str, Any]

@app.get("/data")
async def get_data():
    sensor_data = read_pmsa003_i2c()
    if isinstance(sensor_data, dict) and sensor_data.get("error"):
        raise HTTPException(status_code=500, detail=sensor_data["error"])
    # Optionally, you can perform additional checks here.
    return sensor_data

if __name__ == "__main__":
    # Start the background sensor update thread.
    threading.Thread(target=update_sensor_data, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)