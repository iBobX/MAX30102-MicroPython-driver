# main.py
from machine import sleep
from utime import ticks_diff, ticks_ms

from max30102 import MAX30102

if __name__ == '__main__':
    # Sensor instance. If left empty, loads default ESP32 I2C configuration
    sensor = MAX30102()
    # Alternatively (for other boards):
    # sensor = MAX30102(i2cHexAddress = 0x57)
    # sensor = MAX30102(i2cHexAddress = 0x57, i2c = i2cInstance)

    # The default sensor configuration is:
    # Led mode: 2 (RED + IR)
    # ADC range: 16384
    # Sample rate: 400 Hz
    # Led power: maximum (50.0mA - Presence detection of ~12 inch)
    # Averaged samples: 8
    # pulse width: 411

    # It's possible to set up the sensor at once with the setup_sensor() method.
    # If no parameters are supplied, the default config is loaded.
    print("Setting up sensor with default configuration.", '\n')
    sensor.setup_sensor()

    # It is also possible to tune the configuration parameters one by one.
    # Set the sample rate to 800: 800 samples/s are collected by the sensor
    sensor.set_sample_rate(800)
    # Set the number of samples to be averaged per each reading
    sensor.set_fifo_average(8)

    sleep(1)

    # The readTemperature() method allows to extract the die temperature in °C    
    print("Reading temperature in °C.", '\n')
    print(sensor.read_temperature())

    # Select whether to compute the acquisition frequency or not
    compute_frequency = True

    print("Starting data acquisition from RED & IR registers...", '\n')
    sleep(1)

    t_start = ticks_ms()  # Starting time of the acquisition
    samples_n = 0  # Number of samples that has been collected

    while True:
        # The check() method has to be continuously polled, to check if
        # there are new readings into the sensor's FIFO queue. When new
        # readings are available, this function will put them into the storage.
        sensor.check()

        # Check if the storage contains available samples
        if sensor.available():
            # Access the storage FIFO and gather the readings (integers)
            red_reading = sensor.pop_red_from_storage()
            ir_reading = sensor.pop_ir_from_storage()

            # Print the acquired data (so that it can be plotted with a Serial Plotter)
            print(red_reading, ",", ir_reading)

            # We can compute the real frequency at which we receive data
            if compute_frequency:
                samples_n = samples_n + 1
                if ticks_diff(ticks_ms(), t_start) > 999:
                    f_HZ = samples_n / 1
                    samples_n = 0
                    t_start = ticks_ms()
                    print("acquisition frequency = ", f_HZ)
