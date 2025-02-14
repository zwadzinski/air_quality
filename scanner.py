import time
import board
import adafruit_bitbangio as bitbangio
from adafruit_sgp40 import SGP40

# Create the software I2C bus on the alternate pins.
i2c_sw = bitbangio.I2C(board.D17, board.D27)

# Wait until the bus is available
while not i2c_sw.try_lock():
    pass

devices = i2c_sw.scan()
print("Software I2C devices found:", [hex(device) for device in devices])
i2c_sw.unlock()

# Create a software I2C bus on the specified GPIO pins
i2c_sw = bitbangio.I2C(board.D17, board.D27)

# Initialize the SGP40 sensor
sgp40_sw = SGP40(i2c_sw)

try:
    # Read a raw VOC value from the sensor
    voc = sgp40_sw.measure_raw()
    print("VOC Reading:", voc)
except Exception as e:
    print(f"Error reading SGP40: {e}")