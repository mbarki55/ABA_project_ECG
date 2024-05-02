import serial

# Define the serial port and baud rate
serial_port = 'COM3'
baud_rate = 115200

# Data to send
data_to_send = b'\x55\xAA\x04\xFE\x00\xFC'
# data_to_send = b'\x55\xAA\x04\x02\x01\xF8'
ser = serial.Serial(serial_port, baud_rate, timeout=1)
try:
    # Connect to the serial port
    if ser.isOpen():
        print(f"Connected to {serial_port} at {baud_rate} baud.")
        
        # Send data once
        ser.write(data_to_send)
        print("Sent data:", data_to_send)
        
        # Enter loop for receiving data
        while True:
            data_table=[]
            # Read response from the serial port
            response = ser.read()
            print(response)
            if(response == b"\xfe"):
                print("55 found")
                data_table.append(response)

                while True :
                    response= ser.read()
                    if (response !=b"\xfe"):
                        data_table.append(response.hex())
                    else:
                        print(data_table)
                        if data_table[3] == b"\x55":
                                print("SPO2 found")

                        break
        
    
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
except KeyboardInterrupt:
    print("Keyboard interrupt. Exiting...")
finally:
    if ser.isOpen():
        ser.close()
        print("Serial port closed.")
