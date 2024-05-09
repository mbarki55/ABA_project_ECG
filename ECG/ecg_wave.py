import serial
import matplotlib.pyplot as plt

import numpy as np
import time

serial_port = 'COM3'
baud_rate = 115200
# ECG param
data_to_send = b'\x55\xAA\x04\x01\x01\xF9'
# NIBP 
# data_to_send = b'\x55\xAA\x04\x02\x01\xF8'
data_table = []


x_values = []
y_decimal_value = []

fig, ax = plt.subplots()

# fs = 250
# t = np.linspace(0, 1, fs, endpoint=False)
# x = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 50 * t)
# print(t)  


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
                    
                    if(len(data_table) > 0 and len(data_table) >3 ):
                        # if(data_table[3]== '01'):
                        #     # print('ecg',data_table)
                        #     if (len(data_table) > 4):
                        #         decimal_value = int(data_table[4], 16)
                        #         print("I found", data_table)
                         if(data_table[2]== '09'):
                            # print('ecg',data_table)
                            if (len(data_table) > 4):
                                decimal_value = int(data_table[4], 16)
                                binary_value = bin(decimal_value)[2:]

                                print("I found", binary_value)

                    #             x_values.append(time.time())
                    #             y_decimal_value.append(decimal_value)

                    #             x_values = x_values[-100:]
                    #             y_decimal_value = y_decimal_value[-100:]
                                        
                    #             ax.clear() 
                    #             ax.plot(x_values, y_decimal_value)
                                
                    #             ax.set_xlabel('Time')  
                    #             ax.set_ylabel('Value') 
                    #             ax.set_title('Real-time Plot')
                    #             plt.ylim(0, 300)  
                                
                    #             plt.pause(0.1)

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
