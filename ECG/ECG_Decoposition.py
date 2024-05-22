import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

serial_port = 'COM3'
baud_rate = 115200
data_to_send = b'\x55\xAA\x04\xFB\x01\xFF'
sampling_rate = 600  # en Hz
ecg_values = []

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

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
                            ecg_values.append(decimal_value_wave)

                            # Limiter le nombre de valeurs pour afficher et analyser la FFT
                            if len(ecg_values) > 6000:  # par exemple, 10 secondes de données à 600 Hz
                                ecg_values = ecg_values[-6000:]

                            time_values = np.arange(len(ecg_values)) / sampling_rate
                            ax1.clear()
                            ax1.plot(time_values, ecg_values, label='ECG Wave')
                            ax1.set_xlabel('Time (s)')
                            ax1.set_ylabel('Amplitude')
                            ax1.set_xlim(0, 2)
                            ax1.set_ylim(0, 300)

                            time_values = time_values[-1000:]
                            ecg_values = ecg_values[-1000:]

                            ax1.xaxis.set_major_locator(MultipleLocator(0.2))
                            ax1.xaxis.set_minor_locator(MultipleLocator(1.04))
                            ax1.yaxis.set_major_locator(MultipleLocator(15))
                            ax1.yaxis.set_minor_locator(MultipleLocator(5))
                            ax1.grid(True)
                            ax1.legend()

                            if len(ecg_values) > 1:  # Vérifier qu'il y a suffisamment de données pour la FFT
                                # Calculer la FFT
                                ecg_fft = np.fft.fft(ecg_values)
                                frequencies = np.fft.fftfreq(len(ecg_values), 1/sampling_rate)
                                magnitude = np.abs(ecg_fft)

                                # Tracer les composantes décomposées
                                ax2.clear()
                                ax2.plot(frequencies[:len(frequencies)//2], magnitude[:len(magnitude)//2])
                                ax2.set_xlabel('Frequency (Hz)')
                                ax2.set_ylabel('Magnitude')
                                ax2.grid(True)
                                ax2.set_xlim(0, sampling_rate / 2)
                                ax2.set_ylim(0, max(magnitude[:len(magnitude)//2]))  # Limiter l'axe y pour une meilleure visualisation


                                frequencies = frequencies[-1000:]
                                # ecg_values = ecg_values[-600:]

                                # Tracer le signal ECG original
                                reconstructed_ecg = np.fft.ifft(ecg_fft)
                                ax1.plot(time_values, np.real(reconstructed_ecg), label='Reconstructed ECG', linestyle='--')
                                ax1.legend()

                                time_values = time_values[-1000:]
                                reconstructed_ecg = reconstructed_ecg[-1000:]

                            plt.pause(0.000001)
                        
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

plt.show()
