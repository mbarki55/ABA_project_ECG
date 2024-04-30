# import serial

# port = 'COM3'  
# baud_rate = 115200  

# ser = serial.Serial(port, baud_rate, timeout=1)

# def read_write_data():
#     ser.write(b'\x55\xAA\x04\x03\x01\xF7')
#     try:
#         response = ser.read()
#         print("Received response in hexadecimal:", response.hex())
#         if b"\x55\xaa" in response:
#             print("Valid response received.")
#         else:
#             print("Invalid response format:", response.hex())
#     except serial.SerialTimeoutException:
#         print("Timeout occurred while waiting for response.")

# read_write_data()

import serial

def send_data_and_receive_response():
    port_name = "COM3"
    baud_rate = 115200
    data_to_send = b'\x55\xAA\x04\x03\x01\xF7'

    with serial.Serial(port_name, baud_rate, timeout=1) as ser:
        ser.write(data_to_send)
        return ser.readline().hex()
    
send_data_and_receive_response()
