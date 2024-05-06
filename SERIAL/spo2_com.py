import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

serial_port = 'COM3'
baud_rate = 115200
x_values = []
y_decimal_value = []

fig, ax = plt.subplots() 


data_to_send = b'\x55\xAA\x04\xFE\x00\xFC'
# data_to_send = b'\x55\xAA\x04\x02\x01\xF8'

def read_serial_data(i):
    data_table = []
    global x_values, y_decimal_value  
           
    
    response = ser.read()
    if response == b"\x55":
        data_table.append(response)

        while True:
            response = ser.read()
            if response != b"\x55":
                data_table.append(response)
            else:
                break
        
        if (len(data_table) >= 6 and data_table[3] == b"\xFE"):
           
            hex_value = data_table[4].hex()  
            decimal_value = int(hex_value, 16) 
            print("SPO2 found", decimal_value)
            
            x_values.append(time.time())
            y_decimal_value.append(decimal_value)

            x_values = x_values[-80:]
            y_decimal_value = y_decimal_value[-80:]
                    
            ax.clear() 
            ax.plot(x_values, y_decimal_value)
            
            ax.set_xlabel('Time')  
            ax.set_ylabel('Value') 
            ax.set_title('Real-time Plot')
            plt.ylim(0, 100)  
            
            plt.pause(0.1)


with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
    if ser.isOpen():
        print(f"Connected to {serial_port} at {baud_rate} baud.")
        
        ser.write(data_to_send)
        print("Sent data:", data_to_send)
        while ser.isOpen():
            read_serial_data(y_decimal_value)
        
            
            #ani = animation.FuncAnimation(fig, read_serial_data, interval=0 , cache_frame_data= False)
            
            #plt.show() 
