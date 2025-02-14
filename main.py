import time
from sensors import read_pmsa003_i2c
from functions import interpret_air_quality, display_particle_counts

def main():
    print("Starting Air Quality Monitor...\n")
    while True:
        aqdata = read_pmsa003_i2c()
        if isinstance(aqdata, dict) and "error" not in aqdata:
            print("===================================")
            print("Air Quality Reading:")
            print(interpret_air_quality(aqdata))
            print("\nOther Measurements:")
            print(display_particle_counts(aqdata))
            print("===================================\n")
        else:
            print("Error reading sensor data:", aqdata)
        # Wait for 5 seconds before the next reading.
        time.sleep(5)

if __name__ == "__main__":
    main()