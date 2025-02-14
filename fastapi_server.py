from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import time
import uvicorn
import threading
from sensors import read_pmsa003_i2c, read_sgp40_i2c

app = FastAPI()

# Global variable for sensor data.
latest_data: Dict[str, Any] = {}

# Pydantic model for incoming sensor data.
class SensorData(BaseModel):
    data: Dict[str, Any]

@app.get("/data")
async def get_data():
    # Read data from the pmsa003 sensor.
    pmsa_data = read_pmsa003_i2c()
    if isinstance(pmsa_data, dict) and pmsa_data.get("error"):
        raise HTTPException(status_code=500, detail=pmsa_data["error"])
    
    # Read data from the sgp40 sensor.
    sgp40_data = read_sgp40_i2c()
    if isinstance(sgp40_data, dict) and sgp40_data.get("error"):
        raise HTTPException(status_code=500, detail=sgp40_data["error"])
    
    # Combine both sensor datasets
    return {"pmsa0031": pmsa_data, "sgp40": sgp40_data}

if __name__ == "__main__":
    # Start the background sensor update thread.
    threading.Thread(target=update_sensor_data, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)