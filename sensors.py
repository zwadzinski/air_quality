import time
import board
import busio
from adafruit_pm25.i2c import PM25_I2C
import adafruit_bitbangio as bitbangio
from adafruit_sgp40 import SGP40

def read_pmsa003_i2c():
    """
    Reads data from the PM2.5 sensor over hardware I2C.
    Returns a dictionary of sensor readings or an error dict.
    """
    try:
        i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
        reset_pin = None  # update if needed
        pm25 = PM25_I2C(i2c, reset_pin)
        aqdata = pm25.read()
        return aqdata
    except Exception as e:
        return {"error": str(e)}
    

# Create a software I2C bus on alternative GPIO pins using BitBangIO.
# For example, we choose GPIO17 for SDA and GPIO27 for SCL.
i2c_sw = bitbangio.I2C(board.D17, board.D27)

# Initialize the SGP40 VOC sensor on the software I2C bus.
sgp40_sw = SGP40(i2c_sw)

def read_sgp40_sw():
    try:
        # Read a raw VOC value from the sensor.
        voc = sgp40_sw.measure_raw()
        return voc
    except Exception as e:
        return f"Error reading SGP40 on software I2C: {e}"
    
if __name__ == "__main__":
    # Test reading from the SGP40 sensor
    sgp40_data = read_sgp40_sw()
    print("SGP40 Sensor Data:", sgp40_data)