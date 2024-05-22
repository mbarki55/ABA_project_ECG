import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

serial_port = 'COM3'
baud_rate = 115200

# ECG wave
data_to_send = b'\x55\xAA\x04\xFB\x01\xFF'
data_table = []

ecg_values = []

fig, ax1 = plt.subplots()

sampling_rate = 250  # frames per second
plot_speed_mm_per_sec = 25  # plotting speed in mm/s

# Calculate the time per frame
time_per_frame = 1 / sampling_rate  # seconds per frame

# Calculate the millimeters per frame
mm_per_frame = plot_speed_mm_per_sec * time_per_frame  # mm per frame

try:
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
        if ser.isOpen():
            print(f"Connected to {serial_port} at {baud_rate} baud.")

            ser.write(data_to_send)
            print("Sent data:", data_to_send)

            data_table = []
            record = False
            while True:
                response = ser.read()
                if response == b'\x55':
                    record = True                   
                    if len(data_table) > 3 and data_table[3] == '01':
                        if len(data_table) > 4:
                            decimal_value_wave = int(data_table[4], 16)
                            print("ECG wave I:", decimal_value_wave)

                            ecg_values.append(decimal_value_wave)

                            # Calculate time in mm 
                            time_values = np.arange(len(ecg_values)) * time_per_frame

                            ax1.clear()
                            ax1.plot(time_values, ecg_values, label='I')

                            plt.legend()
                            time_values = time_values[-750:]
                            ecg_values = ecg_values[-750:]

                            ax1.set_xlabel('Distance (mm)')
                            ax1.set_xlim(0,3)

                            ax1.set_ylabel('Amplitude')
                            ax1.set_ylim(0, 750)
                            ax1.yaxis.set_major_locator(MultipleLocator(50))

                            ax1.yaxis.grid(True, which='minor', linestyle='--', linewidth=0.5)

                            plt.grid(True)
                            plt.legend()
                            plt.pause(0.001)

                    data_table = []  
                    data_table.append(response.hex())
                elif response == b'\x55' and record:  
                    record = False
                    print("Sequence received:", data_table)
                elif record:
                    data_table.append(response.hex())

except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
except KeyboardInterrupt:
    print("Keyboard interrupt. Exiting...")
finally:
    if ser.isOpen():
        ser.close()
        print("Serial port closed.")
