import serial
import numpy as np
import matplotlib.pyplot as plt
import time

serial_port = 'COM3'
baud_rate = 115200

data_to_send = b'\x55\xAA\x04\xFB\x01\xFF'
data_table = []

x_values = []
ecg_values = []

fig, ax1 = plt.subplots()

sampling_rate = 500  # in Hz

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
                    data_table = []  # Clear previous data
                    data_table.append(response.hex())
                elif response == b'\x55' and record:
                    record = False
                    print("Sequence received:", data_table)
                elif record:
                    data_table.append(response.hex())

                    if len(data_table) > 0 and len(data_table) > 3:
                        if data_table[3] == '01':
                            if len(data_table) > 4:
                                decimal_value_wave = int(data_table[4], 16)
                                x_values.append(time.time())
                                ecg_values.append(decimal_value_wave)

                                time_values = np.arange(len(ecg_values)) / sampling_rate
                                ax1.clear()
                                ax1.plot(time_values, ecg_values, label='ECG + ST', color='blue')

                                # Adjusting time and voltage scales
                                ax1.set_xlabel('Time (s)')
                                ax1.set_xlim(0, 10)  # Adjust as needed
                                ax1.xaxis.set_major_locator(plt.MultipleLocator(0.2))  # Major grid every 0.2 s
                                ax1.xaxis.set_minor_locator(plt.MultipleLocator(0.04))  # Minor grid every 0.04 s

                                ax1.set_ylabel('Voltage (mV)')
                                ax1.set_ylim(0, 3)  # Adjust as needed
                                ax1.yaxis.set_major_locator(plt.MultipleLocator(0.5))  # Major grid every 0.5 mV
                                ax1.yaxis.set_minor_locator(plt.MultipleLocator(0.1))  # Minor grid every 0.1 mV

                                plt.grid(True)
                                plt.legend()
                                plt.pause(0.000001)

except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
except KeyboardInterrupt:
    print("Keyboard interrupt. Exiting...")
finally:
    if ser.isOpen():
        ser.close()
        print("Serial port closed.")

plt.show()
