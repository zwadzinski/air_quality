import time
import board
import adafruit_bitbangio as bitbangio

# Create the software I2C bus on the alternate pins.
i2c_sw = bitbangio.I2C(board.D17, board.D27)

# Wait until the bus is available
while not i2c_sw.try_lock():
    pass

devices = i2c_sw.scan()
print("Software I2C devices found:", [hex(device) for device in devices])
i2c_sw.unlock()