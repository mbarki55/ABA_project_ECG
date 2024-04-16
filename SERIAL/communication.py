import serial
import matplotlib.pyplot as plt

def send_data_and_receive_response():
    port_name = "COM3"
    baud_rate = 115200
    data_to_send = b'\x55\xAA\x04\x03\x01\xF7'
    
    with serial.Serial(port_name, baud_rate, timeout=1) as ser:
        ser.write(data_to_send)
        return ser.readline().hex()

x_values = []
y_values = []

while True:
    received_response = send_data_and_receive_response()
    if "00" in str(received_response):
        response_parts = str(received_response).split('00')
        if len(response_parts) > 1 and len(response_parts[1]) >= 2:
            value = int(response_parts[1][0:2], 16)
            print("Received response:", value)
            x_values.append(len(x_values))  
            y_values.append(value)          
        else:
            print('Invalid response format')
    else:
        print('Error')

    plt.plot(x_values, y_values)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Received Response Plot')
    plt.pause(0.05)
    plt.clf()
