import serial
import matplotlib.pyplot as plt
import time
import numpy as np

serial_port = 'COM3'
baud_rate = 115200
data_to_send = b'\x55\xAA\x04\xFB\x01\xFF'  # ECG wave
data_table = []

x_values = []
y_values_wave1 = []

fig, ax1 = plt.subplots()

# Placeholder for Pan-Tompkins algorithm implementation
def pan_tompkins(ecg_signal, fs, delay, LPF_len, HPF_len, N, threshold, RR_low, RR_high):
    # Implement Pan-Tompkins algorithm here
    # Calculate r_peaks and return them
    r_peaks = np.array([10, 20, 30, 40])  # Replace with your implementation

    return np.array(r_peaks)

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
                    if len(data_table) > 0 and len(data_table) > 3:
                        if data_table[3] == '01':  # ECG wave
                            if len(data_table) > 4:
                                decimal_value_1 = int(data_table[4], 16)
                                print("ECG wave I:", decimal_value_1)

                                x_values.append(time.time())
                                y_values_wave1.append(decimal_value_1)

                                x_values = x_values[-100:]  # Limit data points for smooth plotting
                                y_values_wave1 = y_values_wave1[-100:]

                                ax1.clear()
                                ax1.plot(x_values, y_values_wave1)

                                ax1.set_xlabel('Time')
                                ax1.set_ylabel('Value')
                                ax1.set_title('Real-time Plot')
                                plt.ylim(0, 300)

                                plt.pause(0.1)

                                # Apply Pan-Tompkins algorithm to detect R-peaks
                                # Replace the placeholders with actual values
                                ecg_signal = np.array(y_values_wave1)  # ECG signal
                                fs = 250  # Sampling frequency
                                delay = 12  # Delay parameter
                                LPF_len = 15  # Low-pass filter length
                                HPF_len = 15  # High-pass filter length
                                N = 20  # Moving average filter length
                                threshold = 60  # Detection threshold
                                RR_low = 300  # Minimum RR interval (in samples)
                                RR_high = 600  # Maximum RR interval (in samples)

                                # Detect R-peaks using Pan-Tompkins algorithm
                                r_peaks = pan_tompkins(ecg_signal, fs, delay, LPF_len, HPF_len, N, threshold, RR_low, RR_high)

                                # Plot ECG wave with R-peaks marked
                                ax1.plot(x_values[r_peaks], y_values_wave1[r_peaks], 'ro')  # Mark R-peaks
                                plt.show()

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
