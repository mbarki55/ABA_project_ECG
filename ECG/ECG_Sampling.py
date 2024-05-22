import serial
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.ticker import MultipleLocator



serial_port = 'COM3'
baud_rate = 115200
# ECG param
# data_to_send = b'\x55\xAA\x04\x01\x01\xF9'
# NIBP 
# data_to_send = b'\x55\xAA\x04\x02\x01\xF8'
# ECG wave
data_to_send = b'\x55\xAA\x04\xFB\x01\xFF'
data_table = []

x_values = []
ecg_values = []
# st_values = []

fig, ax1 = plt.subplots()
# fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 12))

sampling_rate = 600  # in Hz




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
                    # ECG wave
                    if(len(data_table) > 0 and len(data_table) >3 ):
                        if(data_table[3]== '01'):
                            # print('ecg',data_table)
                            if (len(data_table) > 4):
                                decimal_value_wave = int(data_table[4], 16)
                                print("ECG wave I:", decimal_value_wave)

                                ecg_values.append(decimal_value_wave)
                                # x_values.append(time.time())
                                time_values = np.arange(len(ecg_values)) / sampling_rate
                                

                                ax1.clear()
                                # ax1.plot(x_values, ecg_values, label='I')
                                ax1.plot(time_values, ecg_values, label='I')

                                plt.legend()
                                # x_values = x_values[-240:]
                                time_values = time_values[-550:]
                                ecg_values = ecg_values[-550:]


                                ax1.set_xlabel('Time (s)')
                                ax1.set_xlim(0,1)  

                                ax1.xaxis.set_major_locator(MultipleLocator(0.2))
                                ax1.xaxis.set_minor_locator(MultipleLocator(0.04))
                                ax1.xaxis.grid(True, which='minor', linestyle='--', linewidth=0.5)

                                ax1.set_ylabel('Amplitude')
                                ax1.set_ylim(0, 300)

                                # ax1.yaxis.set_major_locator(MultipleLocator(25))
                                # ax1.yaxis.set_minor_locator(MultipleLocator(5))
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



