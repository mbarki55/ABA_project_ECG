import serial
import matplotlib.pyplot as plt
import time

serial_port = 'COM3'
baud_rate = 115200
# ECG param
#  data_to_send = b'\x55\xAA\x04\x01\x01\xF9'
# NIBP 
# data_to_send = b'\x55\xAA\x04\x02\x01\xF8'
# ECG wave
data_to_send = b'\x55\xAA\x04\xFB\x01\xFF'
data_table = []

x_values = []
y_values_wave1 = []
# y_values_wave2 = []
# y_values_wave3 = []

fig, ax1 = plt.subplots()
# fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 12))


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
                    # Ecg param 
                        # ECG status
                    # if(len(data_table) > 0 and len(data_table) >3 ):
                    #     if(data_table[3]== '02'): 
                    #         if (len(data_table) > 4):
                    #             decimal_value_Status = int(data_table[4], 16)
                    #             binary_value_Status = bin(decimal_value_Status)[2:]
                    #             print("ECG status :", binary_value_Status)

                    #         # Heart rate
                    #         if (len(data_table) > 5):
                    #             decimal_value_hR = int(data_table[5], 16)
                    #             heartRate_value = bin(decimal_value_hR)[2:]
                    #             print("Heart rate :", heartRate_value)

                    #         # ECG ST level
                    #         if (len(data_table) > 7):
                    #             decimal_value_ST = int(data_table[7], 16)
                    #             ST_value = bin(decimal_value_ST)[2:]
                    #             print("segment ST :", ST_value)
                    
                    # ECG wave
                    if(len(data_table) > 0 and len(data_table) >3 ):
                        if(data_table[3]== '01'):
                    #         # print('ecg',data_table)
                            if (len(data_table) > 4):
                                decimal_value_1 = int(data_table[4], 16)
                                print("ECG wave I:", decimal_value_1)

                                x_values.append(time.time())
                                y_values_wave1.append(decimal_value_1)

                                x_values = x_values[-50:]
                                y_values_wave1 = y_values_wave1[-50:]
                                        
                                ax1.clear() 
                                ax1.plot(x_values,y_values_wave1)
                                
                                ax1.set_xlabel('Time')  
                                ax1.set_ylabel('Value') 
                                ax1.set_title('I Real-time Plot')
                                plt.ylim(0, 300)  

                            
                                plt.ylim(0, 300)  
                                
                                plt.pause(0.1)
                

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
